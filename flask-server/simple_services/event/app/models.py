from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(64), nullable=False)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    event_location = Column(String(64), nullable=True)