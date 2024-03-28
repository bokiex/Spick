from sqlalchemy.orm import Session, joinedload
import models, schemas




def get_events(db: Session):

    res = db.query(models.Event).options(
        joinedload(models.Event.recommendations),
        joinedload(models.Event.invitees)).all()
   
    return res



def create_event(db: Session, event: schemas.Event):

    event_data = event.dict(exclude={"recommendations", "invitees"})

 
    db_event = models.Event(**event_data)
   
    # Convert recommendation to db model
    if hasattr(event, 'recommendations') and event.recommendations:
            for rec in event.recommendations:
                db_rec = models.Recommendation(**rec.dict(), event=db_event) 
                db_event.recommendations.append(db_rec)
    
    # Convert invitees to db model
    if hasattr(event, 'invitees') and event.invitees:
            for inv in event.invitees:
                db_inv = models.Invitee(**inv.dict(), event=db_event)
                db_event.invitees.append(db_inv)

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event

def get_event_by_id(event_id: int,db: Session ):
    res = db.query(models.Event).options(
        joinedload(models.Event.recommendations),
        joinedload(models.Event.invitees)).filter(models.Event.event_id == event_id).first()

    return res

def update_event(event_id:int, event: schemas.EventPut, db: Session ):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not db_event:
        
        return None
   
    for key, value in event.dict(exclude_unset=True).items():
   
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

def get_invitee(db: Session, event_id: int):
    # get all invitees by event_id
    res = db.query(models.Invitee).filter(models.Invitee.event_id == event_id).all()
    return res

def get_invitee_responded(db: Session, event_id: int):
    return db.query(models.Invitee).filter(models.Invitee.event_id == event_id, models.Invitee.status != None).all()

def update_invitee(db: Session, invitee: schemas.Invitee):
    db_invitee = db.query(models.Invitee).filter(models.Invitee.user_id == invitee.user_id, models.Invitee.event_id == invitee.event_id).first()
    if db_invitee:
        db_invitee.status = invitee.status
        db.commit()
        db.refresh(db_invitee)
    return db_invitee

def create_invitee(db: Session, invitee: schemas.Invitee):
    if db.query(models.Invitee).filter(models.Invitee.user_id == invitee.user_id, models.Invitee.event_id == invitee.event_id).first():
        return None
    db_invitee = models.Invitee(**invitee.dict())
    db.add(db_invitee)
    db.commit()
    db.refresh(db_invitee)
    return db_invitee