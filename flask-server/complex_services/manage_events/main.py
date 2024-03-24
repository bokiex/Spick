import requests
import schemas
import sys
import amqp_connection
import pika
import json
import apscheduler
from fastapi import FastAPI, Depends
from datetime import datetime
from fastapi.responses import JSONResponse
from os import environ
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from fastapi.middleware.cors import CORSMiddleware


event_ms = environ.get('EVENT_URL') or "http://localhost:3800/event"
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:5005/notification"
recommendation_ms = environ.get('RECOMMENDATION_URL') or "http://localhost:3700/recommendation"

connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, channel
    connection = amqp_connection.create_connection()
    channel = connection.channel()

    if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
        print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
        sys.exit(0)

    scheduler.configure(jobstores={'default': SQLAlchemyJobStore(url='mysql+mysqlconnector://root:root@localhost:8889/scheduler')})
    scheduler.start()

    yield
    connection.close()
    scheduler.shutdown()

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
Sample event JSON input:
{
    "event_name": "Picnic",
    "event_desc": "Picnic at Marina Bay",
    "range_start": "2021-10-01 15:00:00",
    "range_end": "2021-10-01 18:00:00",
    "time_out": "2021-09-30 23:59:59",
    "category": "Picnic",
    "township": "Marina Bay",
    "invitees": ["user2", "user3"],
    "user_id": "user1"
}

Sample event JSON output:
{
    "code": 201,
    "data": {
        "event_id": 1,
        "event_name": "Picnic",
        "event_desc": "Picnic at Marina Bay",
        "start_time": "2021-10-01 15:00:00",
        "end_time": "2021-10-01 18:00:00",
        "time_out": "2021-09-30 23:59:59",
        "category": "Picnic",
        "township": "Marina Bay",
        "invitees": [
            {
            'userID': 1
            'username': "user2",
            'email': "user2@email.com",
            'telegramtag': "@user2"
            },
            {
                'userID': 2
                'username': "user3",
                'email': "user3@email.com",
                'telegramtag': "@user3"
            }
        ],
        "user_id": "user1",
        "recommendations": [    
            {
                "recommendation_id": 1,
                "event_id": 1,
                "recommendation_name": "Pandan Reservoir Park",
                "recommendation_address": "700 W Coast Rd, Singapore 608785"
            }
        ]
    }
}
"""

@app.post("/create_event")
def create_event(event: schemas.Recommend):

    event_dict = event.dict()

    # Get recommendation from recommendation microservice

    recommendation_result = requests.post(recommendation_ms, json=jsonable_encoder({"type": event_dict["type"], "township": event_dict["township"]}))
    
    print(recommendation_result.json())
    message = json.dumps(recommendation_result.json())
    if recommendation_result.status_code not in range(200,300):

        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=message, properties=pika.BasicProperties(delivery_mode=2))
     
        return recommendation_result.json()

    # Create event through event microservice
   
    event_dict["recommendation"] = recommendation_result.json()[0:3]
  
    event_result = requests.post(event_ms, json=jsonable_encoder(event_dict))

    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=event_result.json(), properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    # Send notification to users
    channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=event_result.json(), properties=pika.BasicProperties(delivery_mode=2))
    
    # # Start scheduler for event time out
    scheduler.add_job(on_timeout, 'date', run_date=event_result.json()["data"]["time_out"], args=[event_result.json()["data"]["event_id"]])
    scheduler.print_jobs()
  

@app.delete("/delete_event/{event_id}")
def delete_event(event_id: int):
    event_result = requests.delete(event_ms + f"/{event_id}").json()
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="delete_event.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    channel.basic_publish(exchange=exchangename, routing_key="delete_event.notification",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
    return event_result

def on_timeout(event_id: int):
    event_result = requests.get(event_ms + f"/{event_id}").json()
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    # Update event timeout to null
    event_result["time_out"] = None
    event_result = requests.put(event_ms + f"/{event_id}", json=jsonable_encoder(event_result)).json()
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    # Send notification to host and invitees that event has timed out
    # Notification check if timeout == null, if it is send to host only else send to invitees
    channel.basic_publish(exchange=exchangename, routing_key="timeout.notification",body=event_result, properties=pika.BasicProperties(delivery_mode=2))