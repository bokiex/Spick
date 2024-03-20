from fastapi import FastAPI, Depends
import requests
import  schemas

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()


event_ms = "http://0.0.0.0:3600/event"
recommendation_ms = "http://0.0.0.0:3700/recommendation"



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
