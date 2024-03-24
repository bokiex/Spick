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

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def update_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user is None:
        return None
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db_user.telegram_id = user.telegram_id
    db_user.telegram_tag = user.telegram_tag
    db.commit()
    db.refresh(db_user)
    return db_user