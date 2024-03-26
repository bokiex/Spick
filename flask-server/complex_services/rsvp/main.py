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
    "Message": "Successfully accepted and posted user's schedules.",
    "Optimize Status": {
        "message": "Schedule optimized successfully.",
        "result": {
            "schedules": [
                {
                    "date": "2024-04-01",
                    "common_slot": {
                        "start": "2024-04-01T00:00:00",
                        "end": "2024-04-01T10:00:00"
                    },
                    "attending_users": [
                        101
                    ],
                    "non_attending_users": []
                }
            ]
        }
    }
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

    try:
        # Update the invitee status
        status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
        if status_response.status_code < 400:
                # Post the schedules
            schedule_response = requests.post(USER_SCHEDULE_SERVICE_URL, json= jsonable_encoder({"sched_list": request.sched_list}))
            
            if schedule_response.status_code <400:
                retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{request.event_id}")
                if retrieve_response.status_code <400:
                    opt_data = retrieve_response.json()  # Process opt_data as needed
                    opt_data["event_id"] = request.event_id
                    print(opt_data)
                    # Now you can process opt_data as needed
                    # e.g., check_and_trigger_optimization(opt_data)
                    x = check_and_trigger_optimization(jsonable_encoder(opt_data))
                    x = jsonable_encoder(x)
                    return {"Message": "Successfully accepted and posted user's schedules.", "Optimize Status": x}
                else:
                    raise HTTPException(status_code=retrieve_response.status_code, detail="Unable to retrieve value from event service.")
            else:
                raise HTTPException(status_code=schedule_response.status_code, detail="Failed to post schedules / duplicate schedules.")
        else:
            raise HTTPException(status_code=status_response.status_code, detail="Failed to update status to accepted.")

    except requests.RequestException as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Failed to connect to the service: {str(e)}")
    
#Input
# {   
#   "event_id": "123123",
#   "user_id": 102
# }
"""
{
    "Message": "User status set to declined.",
    "Optimize Status": {
        "message": "Schedule optimized successfully.",
        "result": {
            "schedules": [
                {
                    "date": "2024-04-01",
                    "common_slot": {
                        "start": "2024-04-01T00:00:00",
                        "end": "2024-04-01T10:00:00"
                    },
                    "attending_users": [
                        101
                    ],
                    "non_attending_users": []
                }
            ]
        }
    }
}
"""
@app.put("/rsvp/decline")
def decline_invitation(request: DeclineInvitationSchema):
    update_payload = {
        "event_id": request.event_id,
        "user_id": request.user_id,
        "status": "N"  # Setting status to "N" for decline
    }
    
    try:
        status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
        if status_response.status_code < 400:
            retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{request.event_id}")
            if retrieve_response.status_code == 200:
                opt_data = retrieve_response.json()
                opt_data["event_id"] = request.event_id
                # Assuming check_and_trigger_optimization exists and works as expected
                x = check_and_trigger_optimization(jsonable_encoder(opt_data))  # Ensure this function is defined or adjusted for FastAPI
                x = jsonable_encoder(x)
                return {"Message": "User status set to declined.", "Optimize Status": x}
            else:
                raise HTTPException(status_code=retrieve_response.status_code, detail="Unable to retrieve value from event service.")
        else:
            raise HTTPException(status_code=status_response.status_code, detail="Failed to update status to declined.")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to the service: {str(e)}")
    
def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    invitees_left = data['invitees_left']
    event_id = data['event_id']
    if invitees_left ==0 :
        try:
            response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}{event_id}")
            if response.status_code == 200:
                payload = response.json()
                try:
                    opt = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=payload)
                    if opt.status_code < 400:
                        opt = opt.json()
                        return jsonable_encoder({"message": "Schedule optimized successfully.", "result":opt}) 
                    else:
                        return jsonable_encoder({"error": "Failed to optimize schedule."}) 
                except requests.RequestException as e:
                    return jsonable_encoder({"error": "Error connecting to Optimize Schedule service.", "detail": str(e)})
            else:
                return jsonable_encoder({"error": "Failed to retrieve schedule / No schedules available"}) 
        except requests.RequestException as e:
            return jsonable_encoder({"error": "Error connecting to User Schedule service.", "detail": str(e)})
    else:
        # Condition where total_invitees != current_responses
        return jsonable_encoder({"message": "Optimization not triggered, condition not met."})



#Input
# {
#     "event_id": "123123"
# }
"""
{
    "message": "Optimization successful",
    "optimized_timeslots": {
        "schedules": [
            {
                "date": "2024-04-01",
                "common_slot": {
                    "start": "2024-04-01T00:00:00",
                    "end": "2024-04-01T10:00:00"
                },
                "attending_users": [
                    101
                ],
                "non_attending_users": []
            }
        ]
    }
}
"""
@app.post("/rsvp/optimize")
def optimize_schedule(request: TimeoutOptimizeScheduleRequest):
    if not request.event_id:
        raise HTTPException(status_code=400, detail="event_id is required.")

    try:
        # Fetch schedules from User Schedule service using the eventID
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}{request.event_id}")
        if response.status_code == 200:
            schedule_data = response.json()  # Extract JSON data from the response

            # Post the fetched schedules to the Optimize Schedule service
            opt_response = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=schedule_data)
            if opt_response.status_code == 200:
                return {"message": "Optimization successful", "optimized_timeslots": opt_response.json()}
            else:
                raise HTTPException(status_code=opt_response.status_code, detail="Failed to optimize schedule.")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve schedules from User Schedule service.")
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to connect to the User Schedule service: {str(e)}")
    

