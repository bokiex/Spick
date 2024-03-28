from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
import database
from fastapi.encoders import jsonable_encoder
import crud, schemas
import asyncio
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from telebot.async_telebot import AsyncTeleBot
from os import environ
from contextlib import asynccontextmanager

bot_token = environ.get('BOT_TOKEN') or "6996801409:AAGDWkgPaCtRAqH08y9lwYJQif6ESOnQ984"
bot = AsyncTeleBot(bot_token)

@bot.message_handler(func=lambda m: True)
async def create_user(message):
    telegram_id = message.chat.id
    telegram_tag = message.chat.username
    msg = ""
    with database.SessionManager() as db:
        telegram_tag = "@" + telegram_tag
        
        user = crud.get_user_by_telegram_tag(db, telegram_tag)
        if user is None:
            msg = "User not found. Have you created an account yet?"
        
        
        user.telegram_id = str(telegram_id)
        print(jsonable_encoder(user))
        result = crud.update_user(db, user, user.user_id)
        
        if result is None:
            msg = "An error occurred updating the user."
        msg = "Your account is now tied to your telegram tag."


    await bot.send_message(telegram_id, msg)
    
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = asyncio.create_task(bot.polling())
    print("Bot started.")
    
    yield

    print("Stopping bot...")
    bot_task.cancel()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Get all users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    result = crud.get_users(db)
    if result == []:
        raise HTTPException(status_code=404, detail="No users found.")
    return jsonable_encoder(crud.get_users(db))

# Create user
@app.post("/users")
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    result = crud.create_user(db, user)
    if not result:    
        raise HTTPException(status_code=409, detail="User already exists.")
    return result


# Get user by username
@app.get("/users/{username}", response_model=schemas.UserResponse)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    result = crud.get_user_by_username(db, username)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return jsonable_encoder(result)

# Get user by telegram tag
@app.get("/users/telegram/{telegram_tag}", response_model=schemas.UserResponse)
async def get_user_by_telegram_tag(telegram_tag: str, db: Session = Depends(get_db)):
    tag = "@" + telegram_tag
    
    result = crud.get_user_by_telegram_tag(db, tag)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return jsonable_encoder(result)

# Update user
@app.put("/users/user_id/{user_id}")
async def update_user(user: schemas.User, user_id: int, db: Session = Depends(get_db)):
    result = crud.update_user(db, user, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return result

# Get user by user_id
@app.get("/users/user_id/{user_id}", response_model=schemas.UserResponse)
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    result = crud.get_user_by_user_id(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return jsonable_encoder(result)
