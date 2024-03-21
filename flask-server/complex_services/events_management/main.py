
import requests
import  schemas
# import sys
# import amqp_connection
# import pika
# import json
from fastapi import FastAPI, Depends
from datetime import datetime
# from invokes import invoke_http
from os import environ
# from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


event_ms = environ.get('EVENT_URL') or "http://localhost:3600/event"
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:5005/notification"
recommendation_ms = environ.get('RECOMMENDATION_URL') or "http://localhost:3700/recommendation"

# exchangename = "create_event_topic"
# exchangetype = "topic"

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global connection, channel
#     connection = amqp_connection.create_connection()
#     channel = connection.channel()
#     if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
#         print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
#         sys.exit(0)
#     yield
#     connection.close()

# Initialize FastAPI app
app = FastAPI()


"""
Sample event JSON input:
{
    "event_name": "Picnic",
    "event_desc": "Picnic at Marina Bay",
    "start_time": "2021-10-01 15:00:00",
    "end_time": "2021-10-01 18:00:00",
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


    res= requests.post( recommendation_ms, json=jsonable_encoder(event.search))
    result = res.json()[0:3]
   
   
    if res.status_code not in range(200,300):
        return {"message": "reservation failed"}
    else:
        event_dict["recommendation"] = result
    
      
        update_event = requests.post( event_ms, json=jsonable_encoder(event_dict))

        return update_event.json()
