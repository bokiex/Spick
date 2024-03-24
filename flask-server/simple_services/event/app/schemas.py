from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional




class Invitee(BaseModel):
    event_id: int
    user_id: int
    status: str | None = None

class Recommend(BaseModel):
    recommendation_name: str
    recommendation_address: str

class Image(BaseModel):
    
    image_name: str
    image_path: str
  

class Event(BaseModel):
    event_id: int
    event_name: str
    event_desc: str
    datetime_start: datetime
    datetime_end: datetime
    image: List[Image] = []
    recommendation: List[Recommend] = []
    reservation_name: Optional[str] = None
    reservation_address: Optional[str] = None

class EventPut(BaseModel):
    event_name: Optional[str] = None
    event_desc: Optional[str] = None
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    time_out: Optional[datetime] = None
    user_id: Optional[int] = None
    recommendation: Optional[List[Recommend]] = None
    reservation_name: str
    reservation_address: str
    
class EventResponse(Event):
   
    reservation_address: Optional[str] = None
    invitees: List[Invitee] = []
    status: str | None = None
