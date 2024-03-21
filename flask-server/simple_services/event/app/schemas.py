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
    
class EventResponse(BaseModel):
    event_id: int
    event_name: str
    event_desc: str
    start_time: datetime
    end_time: datetime
    time_out: datetime
    user_id: int
    recommendation: List[Recommend] = []
    invitees: List[Invitee] = []
    status: str | None = None
