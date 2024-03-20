from fastapi import FastAPI, Depends
import requests
import  schemas

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

reservation_ms = "http://0.0.0.0:3400/reservation"
event_ms = "http://0.0.0.0:3600/events"

@app.get("/ping")
def ping():
    return {"message": requests.get( reservation_ms ).json()}

@app.post("/reserve")
def reserve(reservation: schemas.Reservation):

    res= requests.post( reservation_ms, json=jsonable_encoder(reservation))

    if res.status_code not in range(200,300):
        return {"message": "reservation failed"}
    
    
    return {"message": "reserved"}

