from pydantic import BaseModel
from typing import Optional
from typing import List

class Recommend(BaseModel):
    user_id: int
    event_name: str
    event_desc: str
    image: str
    datetime_start: str
    datetime_end: str
    type: str
    township: str
    time_out: str
    invitees: list

class Event(BaseModel):
    user_id: int
    start_time: str
    end_time: str
    recommendations: list

class Invitee(BaseModel):
    user_id: int
    username: str
    email: str
    telegram_tag: str
    image: str | None = None
    status: str | None = None

class Recommendation(BaseModel):
    recommendation_name: str
    recommendation_address: str
    recommendation_photo: str | None = None

class EventResponse(BaseModel):
    user_id: int
    event_id: int
    event_name: str
    event_desc: str
    datetime_start: str
    datetime_end: str
    time_out: str | None = None
    image: str | None = None
    recommendations: List[Recommendation] = []
    invitees: List[Invitee] = []
    reservation_name: str | None = None
    reservation_address: str | None = None

      
   
    
    
    

