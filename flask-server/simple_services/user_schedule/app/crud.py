# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_user_schedules(db: Session, event_id: int):
    return db.query(models.UserSchedule).filter(models.UserSchedule.event_id == event_id).all()

# crud.py adjustment for create_user_schedules
def create_user_schedules(db: Session, schedule_list: schemas.UserScheduleList):
    created_schedules = []
    for schedule_data in schedule_list.sched_list:
        db_schedule = models.UserSchedule(**schedule_data.dict())
        db.add(db_schedule)
    db.commit()

    # Assuming db_schedules is a list of SQLAlchemy model instances
    db_schedules = db.query(models.UserSchedule).all()
    # Convert each SQLAlchemy model instance to a dictionary and then to a Pydantic model
    created_schedules = [schemas.UserScheduleCreate(**db_schedule.__dict__) for db_schedule in db_schedules]
    return schemas.UserScheduleList(sched_list=created_schedules)



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
        return None

