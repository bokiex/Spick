from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base

class Recommendation(Base):
    __tablename__ = 'recommendation'
    recommendation_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, nullable=False)
    recommendation_name = Column(String(64), nullable=False)
    recommendation_address = Column(String(64), nullable=False)
    