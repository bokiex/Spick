from pydantic import BaseModel

class Attendee(BaseModel):
    user_id: int
    username: str
    email: str
    telegram_tag: str
    image: str | None = None
    status: str | None = None

class Reservation(BaseModel):
    user_id: int
    event_id: str
    reservation_address: str
    reservation_name: str
    datetime_start: str
    datetime_end: str
    attendees: list[Attendee]


    
