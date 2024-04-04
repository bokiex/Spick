from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from fastapi import File, UploadFile

class Invitee(BaseModel):
    event_id: str | None = None
    user_id: int 
    status: str | None = None

class Recommendation(BaseModel):
    recommendation_name: str
    recommendation_address: str
    recommendation_photo: str | None = None

class Event(BaseModel):
    event_name: str
    event_desc: str
    datetime_start: str
    datetime_end: str
    image: str | None = None
    invitees: List[Invitee] = []
    time_out: str | None = None
    user_id: int
    recommendations: List[Recommendation] = []
    reservation_name: Optional[str] = None
    reservation_address: Optional[str] = None

class EventPut(BaseModel):
    event_name: Optional[str] = None
    event_desc: Optional[str] = None
    datetime_start: Optional[str] = None
    datetime_end: Optional[str] = None
    image: Optional[str] = None
    invitees: Optional[List[Invitee]] = None
    time_out: Optional[str] = None
    user_id: Optional[int] = None
    recommendations: Optional[List[Recommendation]] = None
    reservation_name: Optional[str] = None      #edited by kae
    reservation_address: Optional[str] = None   #edited by kae

class EventResponse(Event):
    event_id: str

class OptimizedScheduleDay(BaseModel):
    event_id: str
    date: str
    start: datetime
    end: datetime
    attending_users: List[int] = Field(default_factory=list) 
    non_attending_users: List[int] = Field(default_factory=list) 

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]

