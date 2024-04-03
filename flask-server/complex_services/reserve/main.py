from fastapi import FastAPI, Depends, HTTPException
import requests
import  schemas
import amqp_connection
import pika
import sys
from fastapi.responses import JSONResponse
from os import environ
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json


reservation_ms = environ.get("RESERVATION_MS_URL") 
event_ms = environ.get("EVENT_MS_URL")
manage_event_ms = environ.get("MANAGE_EVENT_MS_URL") 
connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, channel
    connection = amqp_connection.create_connection()
    channel = connection.channel()

    if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
        print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
        sys.exit(0)

    yield
    connection.close()

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

@app.post("/reserve")
def reserve(reservation: schemas.Reservation):
    # check if reservation name contains fail
    if "fail" in reservation.reservation_name:
        return JSONResponse(status_code=400, content={"message":"Simulated failure of reservation creation"})
    
    reservation_details = {
        "user_id": reservation.user_id,
        "reservation_name": reservation.reservation_name,
        "reservation_start_time": str(reservation.datetime_start),
        "reservation_end_time": str(reservation.datetime_end),
        "reservation_address": reservation.reservation_address
    }

    res = requests.post(reservation_ms, json=reservation_details)
    if res.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="reservation.error", body=json.dumps(res.json()))
        return JSONResponse(status_code=400, content={"message":res.json()})

    res = res.json()['reservation']
    
    event_details = {
        "reservation_name": res["reservation_name"],
        "reservation_address": res["reservation_address"],
        "datetime_start": res["reservation_start_time"],
        "datetime_end": res["reservation_end_time"],
    }    
    update_event = requests.put(event_ms + f"event/{reservation.event_id}", json=event_details)
    if update_event.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="event.error", body=json.dumps(update_event.json()))
        return JSONResponse(status_code=400, content={"message":update_event.json()})
    
    event = requests.get(manage_event_ms + f"event/{reservation.event_id}")
    if event.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="manage_event.error", body=json.dumps(event.json()))
        return JSONResponse(status_code=400, content={"message":event.json()})
    
    event = event.json()
    print(event)

    # convert datetime into date and time 
    reservation.datetime_start = reservation.datetime_start.strftime("%m-%d %H:%M:%S")
    notification = {
        "notification_list": [i["telegram_tag"] for i in event["invitees"]],
        "message": f"{reservation.reservation_name} at {reservation.reservation_address} has been reserved at {reservation.datetime_start}. See you there!"
    }
    channel.basic_publish(exchange=exchangename, routing_key="reservation.notification", body=json.dumps(notification))
    return JSONResponse(status_code=201, content={"message": "Reservation created successfully."})

