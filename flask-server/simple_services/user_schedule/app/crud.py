# crud.py
from sqlalchemy.orm import Session
import models, schemas
from fastapi.encoders import jsonable_encoder
from typing import List

def get_user_schedules(db: Session, event_id: str):
    return db.query(models.UserSchedule).filter(models.UserSchedule.event_id == event_id).all()

# crud.py
def create_user_schedules(db: Session, schedule_list: List[schemas.UserScheduleCreate]):
    created_schedules = []
    for schedule_data in schedule_list:
        db_schedule = models.UserSchedule(**schedule_data.dict())
        print(jsonable_encoder(db_schedule))
        db.add(db_schedule)
        db.commit()
        db.refresh(db_schedule)
        created_schedules.append(db_schedule)
    return [schemas.UserScheduleInDB(
        schedule_id=sch.schedule_id,
        event_id=sch.event_id,
        user_id=sch.user_id,
        start_time=sch.start_time,
        end_time=sch.end_time
    ) for sch in created_schedules]






