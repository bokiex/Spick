from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    telegram_id = Column(String(64), nullable=True)
    telegramtag = Column(String(64), nullable=False)

