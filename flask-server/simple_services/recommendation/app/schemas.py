from pydantic import BaseModel
from datetime import datetime

class RecommendedLocations(BaseModel):
    recommendation_id: int
    event_id: int
    recommendation_name: str
    recommendation_address: str