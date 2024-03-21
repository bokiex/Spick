from sqlalchemy import Column, Integer, TIMESTAMP, String, Float
from database import Base

class Reservation(Base):
    __tablename__ = "reservations"
    reservation_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, nullable=False)
    address = Column(String(64), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
 