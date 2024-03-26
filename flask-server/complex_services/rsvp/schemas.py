from pydantic import BaseModel
from datetime import datetime
from typing import List

# This is aligned with the structure expected by the UserSchedule service
class ScheduleItem(BaseModel):
    schedule_id: int
    event_id: str
    user_id: int
    start_time: datetime
    end_time: datetime

# Used for accepting invitations. The `sched_list` is mandatory for acceptance
class AcceptInvitationSchema(BaseModel):
    event_id: str
    user_id: int
    sched_list: List[ScheduleItem]

class DeclineInvitationSchema(BaseModel):
    event_id: str
    user_id: int
        
# Response model for successful schedule creation
class UserScheduleList(BaseModel):
    sched_list: List[ScheduleItem]

class TimeoutOptimizeScheduleRequest(BaseModel):
    event_id: str  # Assuming eventID is a string. Adjust the type if necessary.    
