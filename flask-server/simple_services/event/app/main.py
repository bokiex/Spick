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
@app.get("/events", response_model=list[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    res = crud.get_events(db)
    if res == []:
        return jsonable_encoder({"message": "No events found."}), 404
    return jsonable_encoder(res)

# Get event by ID
@app.get("/events/{event_id}")
async def get_event_by_id(event_id: int):
    res = crud.get_event_by_id(event_id)
    if res == []:
        return jsonable_encoder({"message": "No event found."}), 404
    return jsonable_encoder(res)

# Update event
@app.put("/events/{event_id}")
async def update_event(event_id: int):
    res = crud.update_event(event_id)
    if res == []:
        return jsonable_encoder({"message": "No event found."}), 404
    return jsonable_encoder(res)

# Delete event
@app.delete("/events/{event_id}")
async def delete_event(event_id: int):
    res = crud.delete_event(event_id)
    if res == []:
        return jsonable_encoder({"message": "No event found."}), 404
    return jsonable_encoder(res)

# Create event
@app.post("/events", response_model=schemas.Event)
async def create_event(event: schemas.Event, db: Session = Depends(get_db)):
    res = crud.create_event(db, event)
    if res is None:
        return jsonable_encoder({"message": "An event with the same name already exists."})
    return jsonable_encoder(res)
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script









    
