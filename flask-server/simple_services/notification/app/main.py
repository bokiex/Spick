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

    result = update_user_by_telegram_tag(telegram_id, telegram_tag)
    await bot.send_message(telegram_id, result['message'])
    
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(bot.polling())
    print("Bot started.")

    yield

    print("Stopping bot...")
    task.cancel()

app = FastAPI(lifespan=lifespan)

# Update user by telegram tag
def update_user_by_telegram_tag(telegram_id: str, telegram_tag: str):
    user = requests.get(user_ms + "telegram/" + telegram_tag)
    if int(user.status_code) > 300:
        
		#channel.basic_publish(exchange=exchangename, routing_key="update.error", body=json.dumps({"telegram_id": telegram_id, "telegram_tag": telegram_tag}))
        
        if int(user.status_code) == 500:
            return {"message": "User microservice is down. Please try again later."}
        return {"message": "User not found. Have you created an account yet?"}
    
    user = user.json()
    user["telegram_id"] = str(telegram_id)
    result = requests.put(user_ms, json=jsonable_encoder(user))
    
    if int(result.status_code) > 300:
        #channel.basic_publish(exchange=exchangename, routing_key="update.error", body=json.dumps({"telegram_id": telegram_id, "telegram_tag": telegram_tag}))
        return {"message": "An error occurred updating the user."}
    return {"message": "Your account is now tied to your telegram tag.", "user": result.json()}

@app.post("/notification")
async def send_notification(notification: dict):
    try:
        bot.send_message(notification['telegram_id'], notification['message'])
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred sending the notification.")
    return {"message": "Notification sent."}
