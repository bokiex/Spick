from fastapi import FastAPI, Depends
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
import crud, schemas
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

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
@app.get("/event/{event_id}")
async def get_event_by_id(event_id: int):
    res = crud.get_event_by_id(event_id)
    if res == []:
        return jsonable_encoder({"message": "No event found."})
    return jsonable_encoder(res)


# Update event
@app.put("/event/{event_id}")
async def update_event(event_id: int, event: schemas.Event, db: Session = Depends(get_db)):
    res = crud.update_event(event_id, event, db)
    if res == []:
        return jsonable_encoder({"message": "No event found."})
    return jsonable_encoder(res)

# Delete event
@app.delete("/event/{event_id}")
async def delete_event(event_id: int):
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
# Create event
@app.post("/event")
async def create_event(event: schemas.Event, db: Session = Depends(get_db)):

    res = crud.create_event(db, event)
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
def get_invitee_responded(event_id: int, db: Session = Depends(get_db)):
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
@app.get("/event/invitee/{event_id}")
def get_invitees(event_id:int, db: Session = Depends(get_db)):
    all_invitees = crud.get_invitee(db, event_id)
    if all_invitees == []:
        return jsonable_encoder({"message": "No invitees found."})
    
    respondents = crud.get_invitee_responded(db, event_id)
    if respondents == []:
        return jsonable_encoder({"message": "No invitees found."})
    
    invitees_left = len(all_invitees) - len(respondents)
    return jsonable_encoder({"all_invitees": all_invitees, "respondents": respondents, "invitees_left": invitees_left, "message": "Invitees found."})

@app.put("/event/invitee")
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
@app.post("/event/invitee")
async def create_invitees(invitee: schemas.Invitee, db: Session = Depends(get_db)):
    
    res = crud.create_invitee(db, invitee)
    if res is None:
        return jsonable_encoder({"message": "User has already been invited to this event."})
    return jsonable_encoder({"data": {"user_id": res.user_id}, "message": "Invitee has been added."})

#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script









    
