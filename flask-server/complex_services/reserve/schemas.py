from pydantic import BaseModel






class Reservation(BaseModel):
    user_id: int
    event_id: str
    reservation_address: str
    reservation_name: str
    datetime_start: str
    datetime_end: str
    attendees: list


    
