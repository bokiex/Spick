from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base

def generate_random_event_id():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase, k=6))

class Event(Base):
    __tablename__ = 'event'
    event_id = Column(String(6), primary_key=True, default=generate_random_event_id)
    event_name = Column(String(64), nullable=False)
    event_desc = Column(String(256), nullable=True)
    range_start = Column(TIMESTAMP, nullable=True)
    range_end = Column(TIMESTAMP, nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    time_out = Column(TIMESTAMP, nullable=True)
    event_location = Column(String(64), nullable=True)
    user_id = Column(Integer, nullable=False)
    reservation_name = Column(String(64), nullable=True)
    reservation_address = Column(String(64), nullable=True)
    recommendation = relationship("Recommendation", back_populates="event")
    image = relationship("Image", back_populates="event")

class Invitee(Base):
    __tablename__ = 'invitee'
    event_id = Column(String(6), primary_key=True, nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(64), nullable=True)

class Recommendation(Base):
    __tablename__ = 'recommendation'
    recommendation_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    recommendation_name = Column(String(64), nullable=False)
    recommendation_address = Column(String(64), nullable=False)
    event_id = Column(String(6), ForeignKey('event.event_id'), nullable=False)

    event = relationship("Event", back_populates="recommendation")

class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    image_name = Column(String(255), nullable=False)
    image_path = Column(String(1024), nullable=False)
    event_id = Column(String(6), ForeignKey('event.event_id'), nullable=False)

    event = relationship("Event", back_populates="image")
