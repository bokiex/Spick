from pydantic import BaseModel, Field

class Reservation(BaseModel):
    user_id: int
    reservation_name: str
    reservation_start_time: str
    reservation_end_time: str
    reservation_address: str

class ReservationResponse(BaseModel):
    reservation_id: int
    user_id: int
    reservation_name: str
    reservation_start_time: str
    reservation_end_time: str
    reservation_address: str