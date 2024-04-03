# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, database
from typing import List
from fastapi.middleware.cors import CORSMiddleware


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


# Dependency to get the DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#input:
# {
#   "sched_list": [
#     {
#       "schedule_id": 1,
#       "event_id": 1,
#       "user_id": 101,
#       "start_time": "2024-04-01T00:00:00",
#       "end_time": "2024-04-01T10:00:00"
#     }
#   ]
# }        
"""
Output
{
    "sched_list": [
        {
            "event_id": 1,
            "user_id": 101,
            "start_time": "2024-04-01T00:00:00",
            "end_time": "2024-04-01T10:00:00"
        }
    ]
}
"""

@app.get("/online")
def online():
    return JSONResponse(status_code=200, content={"message": "User Schedule is online."})

@app.post("/user_schedule", response_model=schemas.UserScheduleList)
def create_schedules(schedule_list: schemas.intake, db: Session = Depends(get_db)):
    created_schedules = crud.create_user_schedules(db=db, schedule_list=schedule_list.sched_list)
    return schemas.UserScheduleList(sched_list=created_schedules)

#input
# http://127.0.0.1:8000/user_schedule/1
"""
Output
[
    {
        "event_id": 1,
        "user_id": 101,
        "start_time": "2024-04-01T00:00:00",
        "end_time": "2024-04-01T10:00:00",
        "schedule_id": 1
    }
]
"""
@app.get("/user_schedule/{event_id}", response_model=List[schemas.UserScheduleInDB])
def read_user_schedules(event_id: str, db: Session = Depends(get_db)):
    schedules = crud.get_user_schedules(db, event_id=event_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="Schedules not found")
    return schedules

#Input
# {
#       "schedule_id": 4,
#       "event_id": 1,
#       "user_id": 101
# }   
"""
{
    "message": "Schedule deleted successfully."
}
"""

