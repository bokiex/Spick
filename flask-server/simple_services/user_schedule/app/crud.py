# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_user_schedules(db: Session, event_id: str):
    return db.query(models.UserSchedule).filter(models.UserSchedule.event_id == event_id).all()

# crud.py
def create_user_schedules(db: Session, schedule_list: schemas.UserScheduleList):
    created_schedules = []
    for schedule_data in schedule_list.sched_list:
        db_schedule = models.UserSchedule(**schedule_data.dict())
        db.add(db_schedule)
        # Flush to ensure db_schedule is populated with database-generated values like schedule_id
        db.flush()
        created_schedules.append(db_schedule)
    db.commit()  # Commit after all schedules are added and flushed

    # Convert the SQLAlchemy model instances back to Pydantic models
    return [schemas.UserScheduleInDB.from_orm(schedule) for schedule in created_schedules]




def delete_user_schedule(db: Session, schedule_id: int, event_id: int, user_id: int):
    db_schedule = db.query(models.UserSchedule).filter(
        models.UserSchedule.schedule_id == schedule_id,
        models.UserSchedule.event_id == event_id,
        models.UserSchedule.user_id == user_id
    ).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return {"message": "Schedule deleted successfully."}
    else:
        return {"message": "Error."}

