from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):
    user_id: int
    reservation_name: str
    reservation_start_time: datetime
    reservation_end_time: datetime
    reservation_address: str

class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    reservation_name: str
    reservation_start_time: datetime
    reservation_end_time: datetime
    reservation_address: str