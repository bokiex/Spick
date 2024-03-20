from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):

    user_id: int
    location_lat: float
    location_long: float
    created_at: Optional[datetime] = Field(None, description="No need.")

class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    location_lat: float
    location_long: float
    created_at: datetime 