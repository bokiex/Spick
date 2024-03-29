from sqlalchemy import Column, Integer, TIMESTAMP, String, Float
from database import Base

class Reservation(Base):
    __tablename__ = "reservation"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False)
    reservation_name = Column(String(64), nullable=False)
    reservation_start_time = Column(TIMESTAMP, nullable=False)
    reservation_end_time = Column(TIMESTAMP, nullable=False)
    reservation_address = Column(String(64), nullable=False)
 