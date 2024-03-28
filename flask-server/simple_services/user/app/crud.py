from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.model_dump(exclude=['password']))
    if db.query(models.User).filter(models.User.email == db_user.email).first() is not None:
        return None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user is None:
        return None
    return db_user

def get_user_by_telegram_tag(db: Session, telegram_tag: str):
    db_user = db.query(models.User).filter(models.User.telegram_tag == telegram_tag).first()
    if db_user is None:
        return None
    return db_user

def update_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user is None:
        return None
    db_user.username = user.username
    db_user.email = user.email
    db_user.password_hash = user.password_hash
    db_user.telegram_id = user.telegram_id
    db_user.telegram_tag = user.telegram_tag
    db.commit()
    db.refresh(db_user)
    return db_user