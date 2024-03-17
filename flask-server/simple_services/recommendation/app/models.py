from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class Recommendation(Base):
    __tablename__ = 'recommendation'
    recommendation_id = Column(Integer, primary_key=True)
    location_name = Column(String(64), nullable=False)
    location_desc = Column(String(64), nullable=True)
    latitude = Column(String(64), nullable=True)
    longitude = Column(String(64), nullable=True)
    event_id = Column(Integer, nullable=False)