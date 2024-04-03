from fastapi import FastAPI
from sqlalchemy.orm import Session
from schemas import AcceptInvitationSchema, ScheduleItem, DeclineInvitationSchema, TimeoutOptimizeScheduleRequest
from typing import List
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import sys
import amqp_connection
import pika
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
from dotenv import load_dotenv
from os import environ
import logging

# URLs for the User Schedule, Optimize Schedule services, and Event Status Update
load_dotenv()

optimize_ms = f"http://{environ.get("OPTIMIZER_MS")}:{environ.get("OPTIMIZER_MS_PORT")}/"
event_ms = f"http://{environ.get("EVENT_MS")}:{environ.get("EVENT_MS_PORT")}/"
user_schedule_ms = f"http://{environ.get("USER_SCHEDULE_MS")}:{environ.get("USER_SCHEDULE_MS_PORT")}/"
user_ms = f"http://{environ.get("USER_MS")}:{environ.get("USER_MS_PORT")}/"

connection = None
channel = None
exchangename = environ.get("EXCHANGE_NAME") #"generic_topic"
exchangetype = environ.get("EXCHANGE_TYPE") #"topic"

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


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


@app.post("/rsvp/accept")
def accept_invitation(request: AcceptInvitationSchema):
    print(event_ms)
    print(user_ms)
    print(user_schedule_ms)
    # Directly setting status to "Y" since this is an acceptance
    update_payload = {
        "event_id": request.event_id,
        "user_id": request.user_id,
        "status": "Y"
    } 

    status_response = requests.put(event_ms + "invitee", json=update_payload)
    if status_response.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="update_status.error",body=json.dumps(status_response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return status_response
    
    schedule_response = requests.post(user_schedule_ms + "user_schedule", json= jsonable_encoder({"sched_list": request.sched_list}))
    if schedule_response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="post_schedule.error",body=json.dumps(schedule_response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return schedule_response.json()
    
    print("\n\n ------ getting invitee from event ms ------ \n\n")
    retrieve_response = requests.get(f"{event_ms}invitee/{request.event_id}")
    if retrieve_response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="retrieve_invitee.error",body=json.dumps(retrieve_response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return retrieve_response.json()
    
    opt_data = retrieve_response.json()  # Process opt_data as needed
    opt_data["event_id"] = request.event_id
    # Now you can process opt_data as needed
    # e.g., check_and_trigger_optimization(opt_data)
    x = check_and_trigger_optimization(jsonable_encoder(opt_data))
    x = jsonable_encoder(x)
    res = "Accepted Successfully"
    return res
    

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
        return status_response.json()
    retrieve_response = requests.get(f"{event_ms}invitee/{request.event_id}")
    if retrieve_response.status_code >300:
        channel.basic_publish(exchange=exchangename, routing_key="retrieve_invitee.error",body=json.dumps(retrieve_response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return retrieve_response.json()
    opt_data = retrieve_response.json()
    opt_data["event_id"] = request.event_id
    # Assuming check_and_trigger_optimization exists and works as expected
    x = check_and_trigger_optimization((opt_data))  # Ensure this function is defined or adjusted for FastAPI
    return JSONResponse(status_code=x.status_code, content=x.json())
    
    
    
    
def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    print("\n\n-----------Optimisation has been triggered-----------\n\n")
    invitees_left = data['invitees_left']
    event_id = data['event_id']
    if invitees_left == 0 :
        response = requests.get(f"{user_schedule_ms}user_schedule/{event_id}")
        if response.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="user_schedule.error",body=json.dumps(response.json()), properties=pika.BasicProperties(delivery_mode=2))
            return JSONResponse(status_code=404, content=response.json())
        
        payload = response.json()

        opt = requests.post(optimize_ms + "optimize_schedule", json=payload)
        if opt.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="optimize.error",body=json.dumps(opt.json()), properties=pika.BasicProperties(delivery_mode=2))
            return opt.json()
        
        opt = opt.json()

        opt_update = requests.post(event_ms + "update_optimize", json = opt)
        if opt_update.status_code >300:
            channel.basic_publish(exchange=exchangename, routing_key="update.error",body=json.dumps(opt_update.json()), properties=pika.BasicProperties(delivery_mode=2))
            return opt_update.json()

        #get the event table entry 
        event_details = requests.get(f"{event_ms}event/{event_id}")
        if event_details.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=json.dumps(event_details.json()), properties=pika.BasicProperties(delivery_mode=2))
            return event_details.json()
        
        # Update event timeout to null
        payload = {'time_out': None}

        event_result = requests.put(f"{event_ms}event/{event_id}", json=jsonable_encoder(payload))
        if event_result.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="event.error",body=json.dumps(event_result.json()), properties=pika.BasicProperties(delivery_mode=2))
            return event_result.json()

        host_id = event_details.json()["user_id"]
        
        host_tag = requests.get(f"{user_ms}users/user_id/{host_id}")
        if host_tag.status_code not in range(200,300):
            channel.basic_publish(exchange=exchangename, routing_key="user.error",body=json.dumps(host_tag.json()), properties=pika.BasicProperties(delivery_mode=2))
            return host_tag.json()

        host_tag = host_tag.json()["telegram_tag"]
        
        noti_payload = {"notification_list": [host_tag], "message": f"Event {event_id} Optimised." }
                                                   
        channel.basic_publish(exchange=exchangename, routing_key="update_optimization.notification",body=json.dumps(noti_payload), properties=pika.BasicProperties(delivery_mode=2))
        
        
        return jsonable_encoder(opt)
    else:
        # Condition where total_invitees != current_responses
        return jsonable_encoder({"message": "Optimization not triggered, condition not met."})
    res = "Failed to check for optimization."
    return res


@app.post("/rsvp/optimize")
def optimize_schedule(request: TimeoutOptimizeScheduleRequest):
    if not request.event_id:
        res = "invalid event_id"
        return res
    
    timeout_status = requests.get( event_ms +"event/" + request.event_id)
    if timeout_status.status_code>300:
        channel.basic_publish(exchange=exchangename, routing_key="get_event.error",body=json.dumps(timeout_status.json()), properties=pika.BasicProperties(delivery_mode=2))
        return timeout_status.json()
    
    

    if timeout_status.json()['time_out'] == None:
        res = "Event was already optimized."
        return JSONResponse(status_code=409, content=jsonable_encoder(res))

    response = requests.get(f"{user_schedule_ms}user_schedule/{request.event_id}")
    if response.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="get_schedule.error",body=json.dumps(response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return response.json()
    
    schedule_data = response.json()
    opt_response = requests.post(optimize_ms + "optimize_schedule", json=schedule_data)
    if opt_response.status_code >300 :
        channel.basic_publish(exchange=exchangename, routing_key="optimize.error",body=json.dumps(opt_response.json()), properties=pika.BasicProperties(delivery_mode=2))
        return opt_response.json()
    
    opt_update = requests.post(event_ms + "update_optimize", json = opt_response.json())
    if opt_update.status_code >300:
        channel.basic_publish(exchange=exchangename, routing_key="update_optmize.error",body=json.dumps(opt_update.json()), properties=pika.BasicProperties(delivery_mode=2))
        return opt_update.json()
    
    event_details = requests.get(f"{event_ms}event/{request.event_id}")
    if event_details.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="timeout.error",body=event_details, properties=pika.BasicProperties(delivery_mode=2))
        return event_details.json()
        
    # Update event timeout to null
    payload = {'time_out': None}

    event_result = requests.put(f"{event_ms}event/{request.event_id}", json=jsonable_encoder(payload))
    if event_result.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="event.error",body=event_result, properties=pika.BasicProperties(delivery_mode=2))
        return event_result.json()

    host_id = event_details.json()["user_id"]
        
    host_tag = requests.get(f"{user_ms}users/user_id/{host_id}")
    if host_tag.status_code not in range(200,300):
        channel.basic_publish(exchange=exchangename, routing_key="user.error",body=host_tag, properties=pika.BasicProperties(delivery_mode=2))
        return host_tag.json()

    host_tag = host_tag.json()["telegram_tag"]
        
    noti_payload = {"notification_list": [host_tag], "message": f"Event {request.event_id} timed-out and optimised." }
                                                   
    channel.basic_publish(exchange=exchangename, routing_key="update_optimization.notification",body=json.dumps(noti_payload), properties=pika.BasicProperties(delivery_mode=2))
    
    return opt_response.json()

    

