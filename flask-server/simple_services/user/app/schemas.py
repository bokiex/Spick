from pydantic import BaseModel
from datetime import datetime
from typing import List


class User(BaseModel):
  
    username: str
    email: str
    password_hash: str
    telegram_tag: str | None = None
    image: str | None = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str
    telegram_tag: str | None = None
    image: str | None = None
