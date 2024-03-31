# models.py
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from pydantic import BaseModel

Base: DeclarativeMeta = declarative_base()

class UserSchedule(Base):
    __tablename__ = 'user_schedule'
    schedule_id = Column(Integer, index=True, primary_key=True)
    event_id = Column(String, index=True)
    user_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class ScheduleDelete(BaseModel): #dont need
    schedule_id: int
    event_id: int
    user_id: int