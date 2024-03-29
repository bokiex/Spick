from fastapi import FastAPI, Depends, Form, UploadFile, File
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
import crud, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
import boto3
import os
from fastapi.responses import JSONResponse
import json
from dotenv import load_dotenv

load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


# Initialize FastAPI app
app = FastAPI()
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all events
@app.get("/event", response_model=list[schemas.EventResponse])
def get_events(db: Session = Depends(get_db)):
    res = crud.get_events(db)
    return jsonable_encoder(res)

# Get event by ID
@app.get("/event/{event_id}", response_model=schemas.Event)
async def get_event_by_id(event_id: str, db: Session = Depends(get_db)):
 
    res = crud.get_event_by_id(event_id, db)
    if res == []:
        return jsonable_encoder({"message": "No event found."})
    return jsonable_encoder(res)


# Update event
@app.put("/event/{event_id}")
async def update_event(event_id: str, event: schemas.EventPut, db: Session = Depends(get_db)):
  
    res = crud.update_event(event_id, event, db)
    if res == []:
        return jsonable_encoder({"message": "No event found."})
    return jsonable_encoder(res)

# Delete event
@app.delete("/event/{event_id}")
async def delete_event(event_id: str):
    res = crud.delete_event(event_id)
    if res == []:
        return jsonable_encoder({"message": "No event found."})
    return jsonable_encoder(res)

"""
{
    "event_name": "Picnic",
    "event_desc": "Picnic at GOTB",
    "start_time": "2024-01-01",
    "end_time": "2024-01-01",
    "time_out": "2024-01-01",
    "user_id": 1
}
"""
def upload_file(files: UploadFile, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    print("\n Uploading file to S3 bucket")
    print(files)
    # Upload the file
    if object_name is None:
        object_name = files.filename
        
    s3_client = boto3.client('s3', 
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    try:
     
        s3_client.upload_fileobj(files.file, "spickbucket", object_name)
        
        return JSONResponse(status_code=200, content={"message": "File uploaded successfully."})
    except:
        return JSONResponse(status_code=400, content={"message": "File upload failed."})

# Create event
@app.post("/event")
async def create_event(event: str = Form(...),  files: Optional[UploadFile] = File(default=None), db: Session = Depends(get_db)):
    
    print(event)
    print(files)
    event = json.loads(event)
    event = schemas.Event(**event)
    
    
    
    res = crud.create_event(db, event)
    upload_file(files)
    

    if res is None:
        return jsonable_encoder({"message": "An event with the same name already exists."})
    return jsonable_encoder({"data": res, "message": "Event has been created."})

"""
{
    "data": [
        {
            "user_id": 1,
            "event_id": 1,
            "status": "Y"
        },
        {
            "user_id": 3,
            "event_id": 1,
            "status": "Y"
        }
    ],
    "message": "Invitees found."
}
"""
@app.get("/event/invitee/responded/{event_id}")
def get_invitee_responded(event_id: str, db: Session = Depends(get_db)):
    res = crud.get_invitee_responded(db, event_id)
    if res == []:
        return jsonable_encoder({"message": "No invitees found."})
    return jsonable_encoder({"data": res, "message": "Invitees found."})

"""
{
    "all_invitees": [
        {
            "user_id": 1,
            "event_id": 1,
            "status": "Y"
        },
        {
            "user_id": 2,
            "event_id": 1,
            "status": null
        },
        {
            "user_id": 3,
            "event_id": 1,
            "status": "Y"
        }
    ],
    "respondents": [
        {
            "user_id": 1,
            "event_id": 1,
            "status": "Y"
        },
        {
            "user_id": 3,
            "event_id": 1,
            "status": "Y"
        }
    ],
    "invitees_left": 1,
    "message": "Invitees found."
}
"""
@app.get("/invitee/{event_id}")
def get_invitees(event_id:str, db: Session = Depends(get_db)):
    all_invitees = crud.get_invitee(db, event_id)
    if all_invitees == []:
        return jsonable_encoder({"message": "No invitees found."})
    
    respondents = crud.get_invitee_responded(db, event_id)
    if respondents == []:
        return jsonable_encoder({"message": "No invitees found."})
    
    invitees_left = len(all_invitees) - len(respondents)
    return jsonable_encoder({"all_invitees": all_invitees, "respondents": respondents, "invitees_left": invitees_left, "message": "Invitees found."})

@app.put("/invitee")
async def update_invitee(invitee: schemas.Invitee, db: Session = Depends(get_db)):
    res = crud.update_invitee(db, invitee)
    if res is None:
        return jsonable_encoder({"message": "No invitee found."})
    return jsonable_encoder({"data": res, "message": "Invitee has been updated."})


"""
{
    "event_id": 1,
    "user_id": 1
}
"""
@app.post("/invitee")
async def create_invitees(invitee: schemas.Invitee, db: Session = Depends(get_db)):
    
    res = crud.create_invitee(db, invitee)
    if res is None:
        return jsonable_encoder({"message": "User has already been invited to this event."})
    return jsonable_encoder({"data": {"user_id": res.user_id}, "message": "Invitee has been added."})



@app.post("/update_optimize")
def add_opt_schedule(optimized: schemas.OptimizedSchedules, db: Session = Depends(get_db)):
    res = crud.add_opt_schedule(db, optimized)
    if res is None:
        return jsonable_encoder({"message": "Optimized schedule has already been invited to this event."})
    return jsonable_encoder({"message": "Optimized schedule has been added."})


#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script