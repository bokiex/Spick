from pydantic import BaseModel
from datetime import datetime

class RecommendedLocations(BaseModel):
    event_id: int
    location_name: str
    location_desc: str
    latitude: float
    longitude: float
    user_id: int