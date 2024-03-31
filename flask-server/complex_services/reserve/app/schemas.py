from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):
    user_id: int
    event_id: str
    reservation_address: str
    reservation_name: str
    datetime_start: datetime
    datetime_end: datetime
    
