from fastapi import FastAPI, Depends
import requests
import  schemas
from os import environ
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

reservation_ms = environ.get("RESERVATION_URL") or "http://0.0.0.0:3400/reservation"
event_ms = environ.get("EVENT_URL") or "http://0.0.0.0:3600/event"

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/reserve")
def reserve(reservation: schemas.Reservation):

    reservation_details = {
        "user_id": reservation.user_id,
        "reservation_name": reservation.reservation_name,
        "reservation_address": reservation.reservation_address
    }

    res= requests.post( reservation_ms, json=reservation_details)


  
    if res.status_code not in range(200,300):
        return {"message": "reservation failed"}
    else:
        update_event = requests.put( event_ms + f"/{reservation.event_id}", json=res.json())

