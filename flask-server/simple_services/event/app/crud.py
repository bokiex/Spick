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
