import requests
import schemas
import sys
import amqp_connection
import pika
import json
import logging
import sys
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

event_db = environ.get('EVENT_MYSQL_DATABASE') or "localhost"
user_ms = environ.get('USER_MS_URL') or "http://localhost:3000/"
event_ms = environ.get('EVENT_MS_URL') or "http://localhost:8100/"
recommendation_ms = environ.get('RECOMMENDATION_MS_URL') or "http://localhost:8102/"
rsvp_ms = environ.get('RSVP_MS_URL') or "http://localhost:4000/"
connection = None
channel = None
exchangename = environ.get("EXCHANGE_NAME") or "generic_topic"
exchangetype = environ.get("EXCHANGE_TYPE") or "topic"

scheduler = BackgroundScheduler()


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, channel
    connection = amqp_connection.create_connection()
    print("Connection established")
    channel = connection.channel()
    
    if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
        print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
        sys.exit(0)
    
    scheduler.add_jobstore('sqlalchemy', url=f'mysql+mysqlconnector://root:root@{event_db}:3306/scheduler')
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



def check_get_event():
    event_result = requests.get(event_ms + "online")
    if event_result.status_code not in range(200,300):
        return False
    user_result = requests.get(user_ms + "online")
    if user_result.status_code not in range(200,300):
        return False
    return True

@app.get("/event")
def get_events():
    online = check_get_event()
    if not online:
        return JSONResponse(status_code=500, content={"error": "Service unavailable"})
    event_result = requests.get(event_ms + "event")
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result.json()
    event_result = event_result.json()

    user_result = requests.get(user_ms + "users")
    if user_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(user_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return user_result.json()
    user_result = user_result.json()

    for event in event_result:
        new_invitees = []
        for invitee in event["invitees"]:
            for user in user_result:
                new_user = {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'telegram_tag': user['telegram_tag'],
                    'image': user['image'],
                    'status': invitee['status']
                }
                if invitee['user_id'] == user['user_id']:
                    new_invitees.append(new_user)
                    break
                if user['user_id'] == event["user_id"]:
                    event["host"] = new_user
        event["invitees"] = new_invitees
    return JSONResponse(status_code=200, content=event_result)

@app.get("/event/{event_id}")
def get_event_by_id(event_id: str):
    online = check_get_event()
    if not online:
        return JSONResponse(status_code=500, content={"error": "Service unavailable"})
    event_result = requests.get(event_ms + "event/" + event_id)

    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result.json()
    event_result = event_result.json()

    user_result = requests.get(user_ms + "users")
    if user_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(user_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return user_result.json()
    user_result = user_result.json()

    new_invitees = []
    for invitee in event_result["invitees"]:
        for user in user_result:
            new_user = {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'telegram_tag': user['telegram_tag'],
                    'image': user['image'],
                    'status': invitee['status']
                }
            if invitee['user_id'] == user['user_id']:
                new_invitees.append(new_user)
                break
            if user['user_id'] == event_result["user_id"]:
                event_result["host"] = new_user
    event_result["invitees"] = new_invitees
    print(event_result)
    return JSONResponse(status_code=200, content=event_result)

def check_timeslot_get():
    event_result = requests.get(event_ms + "online")
    if event_result.status_code not in range(200,300):
        return False
    user_result = requests.get(user_ms + "online")
    if user_result.status_code not in range(200,300):
        return False
    return True

@app.get("/timeslot/{event_id}")
def get_timeslot_by_event_id(event_id: str):
    online = check_timeslot_get()
    if not online:
        return JSONResponse(status_code=500, content={"error": "Service unavailable"})
    timeslot_result = requests.get(event_ms + "get_optimize/" + event_id)
    if timeslot_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_timeslot.error",body=json.dumps(timeslot_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content=timeslot_result.json())
    
    
    
    user_result = requests.get(user_ms + "users")
    if user_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(user_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content=user_result.json())
    

    timeslot_data = timeslot_result.json()
    user_data = user_result.json()
  
    user_lookup = {user['user_id']: {
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'email': user['email'],
                    'telegram_tag': user['telegram_tag'],
                    'image': user['image']
                } for user in user_data}
    
    timeslots = []
    for timeslot in timeslot_data.get('data', []):
        new_invitees = [user_lookup.get(int(invitee_id)) for invitee_id in timeslot["invitees"] if int(invitee_id) in user_lookup]
        timeslot["invitees"] = [invitee for invitee in new_invitees if invitee is not None]
        timeslots.append(timeslot)

    
    print(json.dumps(timeslots))
    return JSONResponse(status_code=200, content=json.dumps(timeslots))
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

def check_create_event():
    event_result = requests.get(event_ms + "online")
    if event_result.status_code not in range(200,300):
        return False
    user_result = requests.get(user_ms + "online")
    if user_result.status_code not in range(200,300):
        return False
    recommendation_ms = requests.get(recommendation_ms + "online")
    if recommendation_ms.status_code not in range(200,300):
        return False
    rsvp_ms = requests.get(rsvp_ms + "online")
    if rsvp_ms.status_code not in range(200,300):
        return False
    return True

@app.post("/create_event")
def create_event(event: str = Form(...), file: Optional[UploadFile] = File(default=None)):
    online = check_create_event()
    if not online:
        return JSONResponse(status_code=500, content={"error": "Service unavailable"})
    event_data = json.loads(event)
    print(event_data)
    event = schemas.Recommend(**event_data)
    print(event)
    # Get recommendation from recommendation microservice
    print("\n----- Getting recommendation list -----")
    #recommendation_result = requests.post(recommendation_ms, json=jsonable_encoder({"type": event_dict["type"], "township": event_dict["township"]}))
    recommendation_result = requests.post(recommendation_ms + "recommendation", json=jsonable_encoder({"type": event.type, "township": event.township}))

    # If search is invalid and recommendation returns no results
    if recommendation_result.status_code == 404:
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=json.dumps(recommendation_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=404, content={"error": "No recommendations found"})
    
    # If recommendation service is not available
    if recommendation_result.status_code not in range(200,300):
        # Publish to error queue
        message = json.dumps(recommendation_result.json())
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=message, properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content={"error": "Recommendation service not available"})

    print("\n------ Recommendation list retrieved ------")
  
    event_dict = jsonable_encoder(event)
    
    # Add recommendation to event
    event_dict["recommendations"] = recommendation_result.json()

    # Add image filename to event
    event_dict["image"] = file.filename
    print(event_dict)
    # Send event to event microservice
    print("\n------ Sending event to event microservice ------")
    
    files = {
        "files": (file.filename, file.file, file.content_type),
    }
    event_result = requests.post(event_ms + "event", data={"event": json.dumps(event_dict)}, files=files)
     
    # If event service is not available
    
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content=event_result.json())
    
    print("\n------ Event created ------")
    event_result = event_result.json()
    print(event_result)
    notification = {
        "notification_list": [i["telegram_tag"] for i in event_dict["invitees"]],
        "message": f"You've been invited to an event! Check it out on Spick. Key in the event code {event_result['data']['event_id']} to view your invite!"
    }
    # Send notification to users
    channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=json.dumps(notification), properties=pika.BasicProperties(delivery_mode=2))
    
    # Start scheduler for event time out
    scheduler.add_job(on_timeout, 'date', run_date=event_result["data"]["time_out"], args=[event_result["data"]["event_id"]])
    scheduler.print_jobs()

    return JSONResponse(status_code=201, content={"message": "Event created successfully.", "data": jsonable_encoder(event_result)})
  
def on_timeout(event_id: str):

    optimize_results = requests.post(rsvp_ms + "rsvp/optimize", json = jsonable_encoder({"event_id": event_id}))

    if optimize_results.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=json.dumps(optimize_results.json()), properties=pika.BasicProperties(delivery_mode=2))
        return JSONResponse(status_code=500, content={"error": "RSVP service not available"})
    
    return JSONResponse(status_code=200, content=optimize_results.json())
    
