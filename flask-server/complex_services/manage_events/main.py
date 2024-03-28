import requests
import schemas
import sys
import amqp_connection
import pika
import json
import apscheduler
from fastapi import FastAPI,  File, UploadFile, Form
from fastapi.responses import JSONResponse 
from os import environ
from contextlib import asynccontextmanager
from fastapi.encoders import jsonable_encoder
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import httpx

event_ms = environ.get('EVENT_URL') or "http://localhost:3800/event"
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:5005/notification"
recommendation_ms = environ.get('RECOMMENDATION_URL') or "http://localhost:3500/recommendation"

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

    jobstore = SQLAlchemyJobStore(url='mysql+mysqlconnector://is213@localhost:8889/scheduler')
    scheduler.add_jobstore(jobstore)
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
async def create_event(event: str = Form(...), file: Optional[UploadFile] = File(default=None)):
    
    event_data = json.loads(event)
    event = schemas.Recommend(**event_data)
    
    # Get recommendation from recommendation microservice
    print("\n----- Getting recommendation list -----")
    #recommendation_result = requests.post(recommendation_ms, json=jsonable_encoder({"type": event_dict["type"], "township": event_dict["township"]}))
    recommendation_result = requests.post(recommendation_ms, json=jsonable_encoder({"type": event.type, "township": event.township}))
    

    # If search is invalid and recommendation returns no results
    if recommendation_result.status_code == 404:
        return JSONResponse(status_code=404, content={"error": "No recommendations found"})
    
    # If recommendation service is not available
    if recommendation_result.status_code not in range(200,300):
        # Publish to error queue
        message = json.dumps(recommendation_result.json())
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=message, properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content={"error": "recommendation service not available"})

    print("\n------ Recommendation list retrieved ------")
    print(recommendation_result.json())
  
    event_dict = jsonable_encoder(event)
    
    # Add recommendation to event
    event_dict["recommendation"] = recommendation_result.json()

    # Add image filename to event
    event_dict["image"] = file.filename
  
    # Send event to event microservice
    print("\n------ Sending event to event microservice ------")
    async with httpx.AsyncClient() as client:
        files = {
            "files": (file.filename, file.file, file.content_type),
        }
        event_result = await client.post(event_ms, data={"event": json.dumps(event_dict)}, files=files)
     
    # If event service is not available
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    print("\n------ Event created ------")
    event_result = event_result.json()

    # Send notification to users
    channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=json.dumps(event_result), properties=pika.BasicProperties(delivery_mode=2))
    
    print(event_result["data"]["event_id"])
    # Start scheduler for event time out
    scheduler.add_job(on_timeout, 'date', run_date=event_result["data"]["time_out"], args=[event_result["data"]["event_id"]])
    scheduler.print_jobs()
  

@app.delete("/delete_event/{event_id}")
def delete_event(event_id: int):
    event_result = requests.delete(event_ms + f"/{event_id}").json()
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="delete_event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    channel.basic_publish(exchange=exchangename, routing_key="delete_event.notification",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
    return event_result

def on_timeout(event_id: str):
    event_result = requests.get(event_ms + f"/{event_id}")
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    event_result = event_result.json()
    # Update event timeout to null
    event_result["time_out"] = None
    event_result = requests.put(event_ms + f"/{event_id}", json=jsonable_encoder(event_result))
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result
    
    # Send notification to host and invitees that event has timed out
    # Notification check if timeout == null, if it is send to host only else send to invitees
    channel.basic_publish(exchange=exchangename, routing_key="timeout.notification",body=event_result, properties=pika.BasicProperties(delivery_mode=2))