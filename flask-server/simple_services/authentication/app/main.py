import schemas
import requests
#import amqp_connection
import sys
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from os import environ
from contextlib import asynccontextmanager
from werkzeug.security import generate_password_hash, check_password_hash

connection = None
channel = None
exchangename = "generic_topic"
exchangetype = "topic"


# Initialize FastAPI app
app = FastAPI()
user_ms = environ.get("USER_URL") or "http://localhost:8000/users/"

"""
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_hash": "string",
  "telegram_id": "string",
  "telegram_tag": "string"
}
"""
@app.post("/signup")
async def signup(user: schemas.User):
    user.password_hash = generate_password_hash(user.password, method='pbkdf2:sha256')
    user_result = requests.post(user_ms, json=jsonable_encoder(user))

    if int(user_result.status_code) > 300:
        raise HTTPException(status_code=user_result.status_code, detail=user_result.json()["detail"])
        #channel.basic_publish(exchange=exchangename, routing_key="signup.error", body=json.dumps(user))
    return jsonable_encoder({"message": "User created successfully.", "user": user_result.json()})

"""
{
  "username": "string",
  "password": "string"
}
"""
@app.post("/login")
async def login(user: schemas.LoginUser):
    user_result = requests.get(user_ms + user.username)
    if int(user_result.status_code) > 300:
        raise HTTPException(status_code=user_result.status_code, detail=user_result.json()["detail"])
        #channel.basic_publish(exchange=exchangename, routing_key="login.error", body=json.dumps(user))
    user_result = user_result.json()
    if not check_password_hash(user_result["password_hash"], user.password):
        raise HTTPException(status_code=401, detail="Invalid password.")
    return jsonable_encoder({"message": "User logged in successfully.", "user": user_result})
