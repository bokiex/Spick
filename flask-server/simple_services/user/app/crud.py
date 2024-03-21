from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user