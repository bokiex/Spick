from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: str
    telegram_id: str | None = None
    telegramtag: str
