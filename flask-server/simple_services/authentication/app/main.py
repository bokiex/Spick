import schemas
import requests
import amqp_connection
import sys
import json
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from os import environ
from contextlib import asynccontextmanager


connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global connection, channel
    connection = amqp_connection.create_connection()
    channel = connection.channel()
    print("channel established")
    if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
        print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
        sys.exit(0)
    yield
    connection.close()

# Initialize FastAPI app
app = FastAPI()
user_ms = environ.get("USER_URL") or "http://localhost:8889/users"

@app.post("/signup")
async def signup(user: schemas.User):
    user = requests.post(user_ms, json=jsonable_encoder(user))
    if user.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="signup.error", body=json.dumps(user))
    return jsonable_encoder({"message": "User created successfully.", "user": json.dumps(user)})

@app.post("/login")
async def login(user: schemas.User):
    user = requests.get(user_ms, json=jsonable_encoder(user))
    if user.status_code > 300:
        channel.basic_publish(exchange=exchangename, routing_key="login.error", body=json.dumps(user))
    return jsonable_encoder({"message": "User logged in successfully.", "user": json.dumps(user)})
