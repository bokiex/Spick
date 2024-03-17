from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(64), nullable=False)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    event_location = Column(String(64), nullable=True)

class RecommendedLocations(Base):
    __tablename__ = 'recommended_locations'
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String(64), nullable=False)
    location_desc = Column(String(64), nullable=True)
    latitude = Column(String(64), nullable=True)
    longitude = Column(String(64), nullable=True)
    user_id = Column(Integer, nullable=False)