from sqlalchemy.orm import Session
import models, schemas

def get_recommendations(db: Session):
    return db.query(models.Recommendation).all()

def create_recommendation(db: Session, recommendation: schemas.Recommendation):
    if db.query(models.Recommendation).filter(models.Recommendation.location_name == recommendation.location_name).first() \
    and db.query(models.Recommendation).filter(models.Recommendation.event_id == recommendation.event_id).first():
        return None
    db_recommendation = models.Recommendation(**recommendation.dict())
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

def get_recommendation_by_id(db: Session, event_id: int):
    return db.query(models.Recommendation).filter(models.Recommendation.event_id == event_id).first()

def delete_recommendation(db: Session, event_id: int):
    db_recommendation = db.query(models.Recommendation).filter(models.Recommendation.event_id == event_id).all()
    for i in db_recommendation:
        db.delete(i)

    db.commit()
    return db_recommendation