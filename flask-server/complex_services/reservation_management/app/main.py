from fastapi import FastAPI, Depends
import requests
import  schemas

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

reservation_ms = "http://0.0.0.0:3400/reservation"
event_ms = "http://0.0.0.0:3600/event"
recommendation_ms = "http://0.0.0.0:"

@app.get("/ping")
def ping():
    return {"message": requests.get( reservation_ms ).json()}

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

