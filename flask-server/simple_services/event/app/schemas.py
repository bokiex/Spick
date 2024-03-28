from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Invitee(BaseModel):
    event_id = str 
    user_id: int 
    status: str | None = None



class Recommendation(BaseModel):
    recommendation_name: str
    recommendation_address: str


class Event(BaseModel):
    event_id: str | None = None
    event_name: str
    event_desc: str
    datetime_start: datetime
    datetime_end: datetime
    image: str | None = None
    invitees: List[Invitee] = []
    time_out: datetime | None = None
    user_id: int
    recommendations: List[Recommendation] = []
    reservation_name: Optional[str] = None
    reservation_address: Optional[str] = None


class EventPut(BaseModel):
    event_name: Optional[str] = None
    event_desc: Optional[str] = None
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    time_out: Optional[datetime] = None
    user_id: Optional[int] = None
    recommendations: Optional[List[Recommendation]] = None
    reservation_name: str
    reservation_address: str


class EventResponse(Event):
    event_id: str


class OptimizedScheduleDay(BaseModel):
    event_id: str
    date: str
    start: datetime
    end: datetime
    attending_users: List[int]
    non_attending_users: List[int]

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]

