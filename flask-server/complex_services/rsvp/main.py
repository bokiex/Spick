from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import AcceptInvitationSchema, ScheduleItem, DeclineInvitationSchema, TimeoutOptimizeScheduleRequest
from typing import List
import requests
from fastapi.encoders import jsonable_encoder
import sys
import amqp_connection
import pika
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json


# URLs for the User Schedule, Optimize Schedule services, and Event Status Update

optimize_ms = "http://optimizer:8106/"
event_ms = "http://event:8100/"
user_schedule_ms = "http://user_schedule:8105/"
user_ms = "http://user:8101/"


connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"

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

app = FastAPI(lifespan=lifespan)

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
   
app = FastAPI(lifespan=lifespan)

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

    status_response = requests.put(event_ms + "invitee", json=update_payload)
    if status_response.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="update_status.error",body=json.dumps(status_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    
    schedule_response = requests.post(user_schedule_ms + "user_schedule", json= jsonable_encoder({"sched_list": request.sched_list}))
    if schedule_response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="post_schedule.error",body=json.dumps(schedule_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    
    retrieve_response = requests.get(f"{event_ms}invitee/{request.event_id}")
    if retrieve_response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="retrieve_invitee.error",body=json.dumps(retrieve_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    
    opt_data = retrieve_response.json()  # Process opt_data as needed
    opt_data["event_id"] = request.event_id
    # Now you can process opt_data as needed
    # e.g., check_and_trigger_optimization(opt_data)
    x = check_and_trigger_optimization(jsonable_encoder(opt_data))
    x = jsonable_encoder(x)
    res = "Accepted Successfully"
    return res
    


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
    
    status_response = requests.put(event_ms + "invitee", json=update_payload)
    if status_response.status_code >300:
        channel.basic_publish(exchange=exchangename, routing_key="update_status.error",body=json.dumps(status_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    retrieve_response = requests.get(f"{event_ms}invitee/{request.event_id}")
    if retrieve_response.status_code >300:
        channel.basic_publish(exchange=exchangename, routing_key="retrieve_invitee.error",body=json.dumps(retrieve_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    opt_data = retrieve_response.json()
    opt_data["event_id"] = request.event_id
    # Assuming check_and_trigger_optimization exists and works as expected
    x = check_and_trigger_optimization((opt_data))  # Ensure this function is defined or adjusted for FastAPI
    x = jsonable_encoder(x)
    res = "Declined Successfully"
    return res
    
    
def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    invitees_left = data['invitees_left']
    event_id = data['event_id']
    if invitees_left == 0 :
        response = requests.get(f"{user_schedule_ms}user_schedule/{event_id}")
        if response.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="user_schedule.error",body=response, properties=pika.BasicProperties(delivery_mode=2))
            return response
        
        payload = response.json()

        opt = requests.post(optimize_ms + "optimize_schedule", json=payload)
        if opt.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="optimize.error",body=opt, properties=pika.BasicProperties(delivery_mode=2))
            return opt
        
        opt = opt.json()

        opt_update = requests.post(event_ms + "update_optimize", json = opt)
        if opt_update.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="update.error",body=opt_update, properties=pika.BasicProperties(delivery_mode=2))
            return opt_update

        #get the event table entry 
        event_details = requests.get(f"{event_ms}event/{event_id}")
        if event_details.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_details, properties=pika.BasicProperties(delivery_mode=2))
            return event_details
        
        # Update event timeout to null
        payload = {'time_out': None}

        event_result = requests.put(f"{event_ms}event/{event_id}", json=jsonable_encoder(payload))
        if event_result.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="event.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
            return event_result

        host_id = event_details.json()["user_id"]
        
        host_tag = requests.get(f"{user_ms}users/user_id/{host_id}")
        if host_tag.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="user.error",body=host_tag, properties=pika.BasicProperties(delivery_mode=2))

        host_tag = host_tag.json()["telegram_tag"]
        
        noti_payload = {"notification_list": [host_tag], "message": f"Event {event_id} Optimised." }
                                                   
        channel.basic_publish(exchange=exchangename, routing_key="update_optimization.notification",body=json.dumps(noti_payload), properties=pika.BasicProperties(delivery_mode=2))
        
        
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
        res = "invalid event_id"
        return res
    response = requests.get(f"{user_schedule_ms}user_schedule/{request.event_id}")
    if response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="get_schedule.error",body=json.dumps(response.json()), properties=pika.BasicProperties(delivery_mode=2))
    schedule_data = response.json()
    opt_response = requests.post(optimize_ms + "optimize_schedule", json=schedule_data)
    if opt_response.status_code >300 :
        channel.basic_publish(exchange=exchangename, routing_key="optimize.error",body=json.dumps(opt_response.json()), properties=pika.BasicProperties(delivery_mode=2))
    opt_update = requests.post(event_ms + "update_optimize", json = opt_response.json())
    if opt_update.status_code >300:
        channel.basic_publish(exchange=exchangename, routing_key="update_optmize.error",body=json.dumps(opt_update.json()), properties=pika.BasicProperties(delivery_mode=2))
    
    event_details = requests.get(f"{event_ms}event/{request.event_id}")
    if event_details.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_details, properties=pika.BasicProperties(delivery_mode=2))
        return event_details
        
    # Update event timeout to null
    payload = {'time_out': None}

    event_result = requests.put(f"{event_ms}event/{request.event_id}", json=jsonable_encoder(payload))
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="event.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result

    host_id = event_details.json()["user_id"]
        
    host_tag = requests.get(f"{user_ms}users/user_id/{host_id}")
    if host_tag.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="user.error",body=host_tag, properties=pika.BasicProperties(delivery_mode=2))

    host_tag = host_tag.json()["telegram_tag"]
        
    noti_payload = {"notification_list": [host_tag], "message": f"Event {request.event_id} timed-out and optimised." }
                                                   
    channel.basic_publish(exchange=exchangename, routing_key="update_optimization.notification",body=json.dumps(noti_payload), properties=pika.BasicProperties(delivery_mode=2))
        
    
    return opt_response.json()

    

