from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import AcceptInvitationSchema, ScheduleItem, DeclineInvitationSchema, TimeoutOptimizeScheduleRequest
from typing import List
import requests
from fastapi.encoders import jsonable_encoder
from flask import jsonify
import sys
import amqp_connection
import pika
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json

app = FastAPI()

# URLs for the User Schedule, Optimize Schedule services, and Event Status Update

OPTIMIZE_SCHEDULE_SERVICE_URL = "http://127.0.0.1:8001/optimize_schedule"
UPDATE_RESPONSES_URL = "http://127.0.0.1:8002/invitee"
VALUE_RETRIEVE_URL = "http://127.0.0.1:8002/invitee/"
UPDATE_OPTIMIZATION_URL = "http://127.0.0.1:8002/update_optimize"
EVENT_URL = "http://127.0.0.1:8002/event/"
USER_SCHEDULE_SERVICE_URL = "http://127.0.0.1:8003/user_schedule/"
NOTIFICATION_URL = "http://127.0.0.1:8004/notification"


connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"


origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, channel
    connection = amqp_connection.create_connection()
    channel = connection.channel()

    if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
        print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
        sys.exit(0)

    yield
    connection.close()
   

# put this logic after getting host teletag
# channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=message, properties=pika.BasicProperties(delivery_mode=2))

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
    x = check_and_trigger_optimization((opt_data))  # Ensure this function is defined or adjusted for FastAPI
    x = jsonable_encoder(x)

    return x
    
    
def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    invitees_left = data['invitees_left']
    event_id = data['event_id']
    if invitees_left == 0 :
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}{event_id}")
        if response.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="user_schedule.error",body=response, properties=pika.BasicProperties(delivery_mode=2))
            return response
        
        payload = response.json()

        opt = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=payload)
        if opt.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="optimize.error",body=opt, properties=pika.BasicProperties(delivery_mode=2))
            return opt
        
        opt = opt.json()

        opt_update = requests.post(UPDATE_OPTIMIZATION_URL, json = opt)
        if opt_update.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="update.error",body=opt_update, properties=pika.BasicProperties(delivery_mode=2))
            return opt_update

    #if full response, set the timeout to NULL 
        event_result = requests.get(f"{EVENT_URL}{event_id}")
        if event_result.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
            return event_result
        
        event_result = event_result.json()
        # Update event timeout to null
        event_result["time_out"] = None
        event_result = requests.put(f"{EVENT_URL}{event_id}", json=jsonable_encoder(event_result))
        if event_result.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
            return event_result

        host_tag = requests.get(f"{EVENT_URL}{event_id}")
        if host_tag.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=host_tag, properties=pika.BasicProperties(delivery_mode=2))
            return host_tag

        noti_payload = jsonable_encoder( {"notification_list":  [host_tag.json()["host_tag"]], "message": f"Event {event_id} Optimised." })
                                                              
        channel.basic_publish(exchange=exchangename, routing_key="update_optimization.notification",body=noti_payload, properties=pika.BasicProperties(delivery_mode=2))
        
        
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
    
    event_result = requests.get(f"{EVENT_URL}{request.event_id}")
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
        return event_result
        
    event_result = event_result.json()
    # Update event timeout to null
    event_result["time_out"] = None
    event_result = requests.put(f"{EVENT_URL}{request.event_id}", json=jsonable_encoder(event_result))
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result    
    
    return opt_response.json()

    

