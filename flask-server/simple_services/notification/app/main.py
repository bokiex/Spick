import logging
import sqlalchemy as db
import requests
import asyncio
from telebot.async_telebot import AsyncTeleBot
from os import environ
from flask import jsonify
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager

bot_token = environ.get('BOT_TOKEN') or "6996801409:AAGDWkgPaCtRAqH08y9lwYJQif6ESOnQ984"
user_ms = environ.get("USER_URL") or "http://localhost:3000/users/"
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:5000/notification/"
bot = AsyncTeleBot(bot_token)

@bot.message_handler(func=lambda m: True)
async def create_user(message):
    telegram_id = message.chat.id
    telegram_tag = message.chat.username
    try:
        result = update_user_by_telegram_tag(telegram_id, telegram_tag)
        data = result.json()
        await bot.send_message(telegram_id, data['message'])
    except Exception as e:        
        await bot.send_message(telegram_id, "An error occurred adding the user. Please try again later.")
    
@asynccontextmanager
async def lifespan(app: FastAPI):
# Echo functionality

    asyncio.run(bot.polling())
    yield
    asyncio.run(bot.stop_polling()) 

app = FastAPI(lifespan=lifespan)

# Update user by telegram tag
def update_user_by_telegram_tag(telegram_id: str, telegram_tag: str):
    user = requests.get(user_ms + telegram_tag)
    print(user)
    if int(user.status_code) > 300:
		#channel.basic_publish(exchange=exchangename, routing_key="update.error", body=json.dumps({"telegram_id": telegram_id, "telegram_tag": telegram_tag}))
        return {"message": "User not found. Have you created an account yet?"}
    user = user.json()
    user["telegram_id"] = telegram_id
	
    result = requests.put(user_ms + telegram_tag, json=user)
    if int(result.status_code) > 300:
        raise Exception()
    return {"message": "Your account is now tied to your telegram tag.", "user": result.json()}

@app.post("/notification")
async def send_notification(notification: dict):
    try:
        bot.send_message(notification['telegram_id'], notification['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred sending the notification.")
    return {"message": "Notification sent."}
