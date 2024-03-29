from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):
    user_id: int
    reservation_name: str
    reservation_address: str
    created_at: Optional[datetime] = Field(None, description="No need.")

class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    reservation_name: str
    reservation_address: str