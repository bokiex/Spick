from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):
    reservation_id: int
    user_id: int
    location_lat: float
    location_long: float
    created_at: datetime | None = None
