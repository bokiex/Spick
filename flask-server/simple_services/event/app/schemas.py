from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional




class Invitee(BaseModel):
    event_id: int
    user_id: int
    status: str

class Recommend(BaseModel):
    recommendation_name: str
    recommendation_address: str
  

class Event(BaseModel):
    event_name: str
    event_desc: str
    start_time: datetime
    end_time: datetime
    time_out: datetime
    user_id: int
    recommendation: List[Recommend] = []
    reservation_name: Optional[str] = None
    reservation_address: Optional[str] = None

class EventPut(Event):
    event_name: Optional[str] = None
    event_desc: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    time_out: Optional[datetime] = None
    user_id: Optional[int] = None
    recommendation: Optional[List[Recommend]] = None
    reservation_name: str
    reservation_address: str
    
class EventResponse(Event):
   
    reservation_address: Optional[str] = None
    invitees: List[Invitee] = []
    status: str | None = None
