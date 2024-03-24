from fastapi import FastAPI, Depends
from database import SessionLocal
from fastapi.encoders import jsonable_encoder
import crud, schemas
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# methods

#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script