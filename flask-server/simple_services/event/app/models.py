from sqlalchemy import Column, Integer, TIMESTAMP, String, ForeignKey, LargeBinary, Boolean
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
    datetime_start = Column(TIMESTAMP, nullable=True)
    datetime_end = Column(TIMESTAMP, nullable=True)
    time_out = Column(TIMESTAMP, nullable=True)
    event_location = Column(String(64), nullable=True)
    user_id = Column(Integer, nullable=False)
    reservation_name = Column(String(64), nullable=True)
    reservation_address = Column(String(64), nullable=True)
    image = Column(String(1024), nullable=True)
    recommendations = relationship("Recommendation", back_populates="event",   cascade="all, delete, delete-orphan")
    invitees = relationship("Invitee", back_populates="event",   cascade="all, delete, delete-orphan")

class Invitee(Base):
    __tablename__ = 'invitee'
    event_id = Column(String(6), ForeignKey('event.event_id'), nullable=False)
    user_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String(6), nullable=True, default=False)
    event = relationship("Event", back_populates="invitees")

class Recommendation(Base):
    __tablename__ = 'recommendation'
    recommendation_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    recommendation_name = Column(String(64), nullable=False)
    recommendation_address = Column(String(64), nullable=False)
    event_id = Column(String(6), ForeignKey('event.event_id'), nullable=False)

    event = relationship("Event", back_populates="recommendations")

class Optimized(Base):
    __tablename__ = 'optimized'
    event_id = Column(String(6), primary_key=True, nullable=False)
    attendee_id = Column(Integer, primary_key=True, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)