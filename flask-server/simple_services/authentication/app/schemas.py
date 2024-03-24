from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    username: str
    email: str
    password: str
    password_hash: str | None = None
    telegram_id: str | None = None
    telegram_tag: str

class LoginUser(BaseModel):
    username: str
    password: str