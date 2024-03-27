from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import AcceptInvitationSchema, ScheduleItem, DeclineInvitationSchema, TimeoutOptimizeScheduleRequest
from typing import List
import requests
from fastapi.encoders import jsonable_encoder
from flask import jsonify

app = FastAPI()

# URLs for the User Schedule, Optimize Schedule services, and Event Status Update
USER_SCHEDULE_SERVICE_URL = "http://127.0.0.1:8003/user_schedule/"
OPTIMIZE_SCHEDULE_SERVICE_URL = "http://127.0.0.1:8001/optimize_schedule"
UPDATE_RESPONSES_URL = "http://127.0.0.1:8002/invitee"
VALUE_RETRIEVE_URL = "http://127.0.0.1:8002/invitee/"
UPDATE_OPTIMIZATION_URL = "http://127.0.0.1:8002/update_optimize"

#Input
# {   
#   "event_id": "123123",
#   "user_id": 101,
#   "sched_list": [
#     {
#       "schedule_id": 1,
#       "event_id": "123123",
#       "user_id": 101,
#       "start_time": "2024-04-01T00:00:00",
#       "end_time": "2024-04-01T10:00:00"
#     }
#   ]
# }     
"""
{
    "schedules": [
        {
            "event_id: "123123",
            "date": "2024-04-01",
            "start": "2024-04-01T00:00:00",
            "end": "2024-04-01T10:00:00",
            "attending_users": [
                101
            ],
            "non_attending_users": []
        }
    ]
}
"""
@app.post("/rsvp/accept")
def accept_invitation(request: AcceptInvitationSchema):
    # Directly setting status to "Y" since this is an acceptance
    update_payload = {
        "event_id": request.event_id,
        "user_id": request.user_id,
        "status": "Y"
    }

    status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
    if status_response.status_code > 300:
        raise HTTPException(status_code=status_response.status_code, detail=status_response)
    
    schedule_response = requests.post(USER_SCHEDULE_SERVICE_URL, json= jsonable_encoder({"sched_list": request.sched_list}))
    if schedule_response.status_code > 300:
        raise HTTPException(status_code=schedule_response.status_code, detail=schedule_response)
    
    retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{request.event_id}")
    if retrieve_response.status_code > 300:
        raise HTTPException(status_code=retrieve_response.status_code, detail=retrieve_response)
    opt_data = retrieve_response.json()  # Process opt_data as needed
    opt_data["event_id"] = request.event_id
    # Now you can process opt_data as needed
    # e.g., check_and_trigger_optimization(opt_data)
    x = check_and_trigger_optimization(jsonable_encoder(opt_data))
    x = jsonable_encoder(x)
    return x
    


#Input
# {   
#   "event_id": "123123",
#   "user_id": 102
# }
"""
{
    "schedules": [
        {   
            "event_id: "123123",
            "date": "2024-04-01",
            "start": "2024-04-01T00:00:00",
            "end": "2024-04-01T10:00:00",
            "attending_users": [
                101
            ],
            "non_attending_users": []
        }
    ]
}
"""
@app.put("/rsvp/decline")
def decline_invitation(request: DeclineInvitationSchema):
    update_payload = {
        "event_id": request.event_id,
        "user_id": request.user_id,
        "status": "N"  # Setting status to "N" for decline
    }

    status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
    if status_response.status_code >300:
        raise HTTPException(status_code=status_response.status_code, detail=status_response)
    retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{request.event_id}")
    if retrieve_response.status_code >300:
        raise HTTPException(status_code=retrieve_response.status_code, detail=retrieve_response)
    opt_data = retrieve_response.json()
    opt_data["event_id"] = request.event_id
    # Assuming check_and_trigger_optimization exists and works as expected
    x = check_and_trigger_optimization(jsonable_encoder(opt_data))  # Ensure this function is defined or adjusted for FastAPI
    x = jsonable_encoder(x)

    return x
    
    
def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    invitees_left = data['invitees_left']
    event_id = data['event_id']
    if invitees_left == 0 :
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}{event_id}")
        print(response)
        if response.status_code >300:
            raise HTTPException(status_code=response.status_code, detail=response)
        payload = response.json()
        opt = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=payload)
        if opt.status_code >300:
            raise HTTPException(status_code=opt.status_code, detail=opt)
        opt = opt.json()
        opt_update = requests.post(UPDATE_OPTIMIZATION_URL, json = opt)
        if opt_update.status_code >300:
            raise HTTPException(status_code=opt_update.status_code, detail="failed to update event db")
        
        # event_response = requests.get(f"{GET_EVENT_URL}{event_id}")
        # if event_response.status_code >300:
        #     raise HTTPException(status_code=event_response.status_code, detail=event_response)
        return jsonable_encoder(opt)
    else:
        # Condition where total_invitees != current_responses
        return jsonable_encoder({"message": "Optimization not triggered, condition not met."})

#Input
# {
#     "event_id": "123123"
# }
"""
{
    "schedules": [
        {   
            "event_id: "123123",
            "date": "2024-04-01",
            "start": "2024-04-01T00:00:00",
            "end": "2024-04-01T10:00:00",
            "attending_users": [
                101
            ],
            "non_attending_users": []
        }
    ]
}
"""
@app.post("/rsvp/optimize")
def optimize_schedule(request: TimeoutOptimizeScheduleRequest):
    if not request.event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}{request.event_id}")
    if response.status_code > 300:
        raise HTTPException(status_code=response.status_code, detail=response)
    schedule_data = response.json()
    opt_response = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=schedule_data)
    if opt_response.status_code >300 :
        raise HTTPException(status_code=opt_response.status_code, detail=opt_response)
    opt_update = requests.post(UPDATE_OPTIMIZATION_URL, json = opt_response.json())
    if opt_update.status_code >300:
        raise HTTPException(status_code=opt_update.status_code, detail="failed to update event db")
    return opt_response.json()    
    
    

    

