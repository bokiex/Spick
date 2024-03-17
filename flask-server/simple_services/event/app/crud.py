from sqlalchemy.orm import Session
import models, schemas


def get_events(db: Session):
    return db.query(models.Event).all()

def create_event(db: Session, event: schemas.Event):
    if db.query(models.Event).filter(models.Event.event_name == event.event_name).first():
            return None
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.event_id == event_id).first()

def update_event(db: Session, event_id: int, event: schemas.Event):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if db_event:
        db_event.event_name = event.event_name
        db_event.start_time = event.start_time
        db_event.end_time = event.end_time
        db_event.event_location = event.event_location
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event