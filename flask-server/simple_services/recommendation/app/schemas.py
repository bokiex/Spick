from pydantic import BaseModel
from datetime import datetime

class Recommendation(BaseModel):
    recommendation_name: str
    recommendation_address: str
    recommendation_photos : str
    recommendation_rating : str
    price_level : str


class Search(BaseModel):
    type: str
    township: str