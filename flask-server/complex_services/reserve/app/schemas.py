from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Reservation(BaseModel):

    user_id: int
    event_id: int
    reservation_address: str
    num_guests: int
    reservation_name: str
    start_time: datetime
    end_time: datetime
    
