from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(64), nullable=False)
    event_desc = Column(String(256), nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    time_out = Column(TIMESTAMP, nullable=True)
    event_location = Column(String(64), nullable=True)
    user_id = Column(Integer, nullable=False)

class Invitee(Base):
    __tablename__ = 'invitee'
    event_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(64), nullable=True)