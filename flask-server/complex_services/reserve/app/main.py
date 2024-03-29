from fastapi import FastAPI, Depends, HTTPException
import requests
import  schemas
import amqp_connection
import pika
import sys
from os import environ
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json


reservation_ms = environ.get("RESERVATION_URL") or "http://localhost:3400/reservation"
event_ms = environ.get("EVENT_URL") or "http://localhost:3600/event"

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
        return HTTPException(status_code=400, detail={"message":"Simulated failure of reservation creation"})
    
    reservation_details = {
        "user_id": reservation.user_id,
        "reservation_name": reservation.reservation_name,
        "reservation_address": reservation.reservation_address
    }

    res= requests.post(reservation_ms, json=reservation_details)
    if res.status_code not in range(200,300):
        return {"message": "reservation failed"}
    else:
        update_event = requests.put( event_ms + f"/{reservation.event_id}", json=res.json())

