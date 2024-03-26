import logging
import sqlalchemy as db
import requests
import asyncio
import json
import pika
import amqp_connection
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
    print("Error microservice: Getting Connection")
    connection = amqp_connection.create_connection()
    print("Error microservice: Connection established successfully")
    channel = connection.channel()
    receiveNotification(channel)

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


def receiveNotification(channel):
    try:
        channel.basic_consume(queue="Notification", on_message_callback=callback, auto_ack=True)
        print('Notification microservice: Consuming from queue: Notification')
        channel.start_consuming()
        
    except pika.exceptions.AMQPError as e:
        print(f"Notification microservice: Failed to connect: {e}")
        
    except KeyboardInterrupt:
        print("Notification microservice: Program interrupted by user.")

def callback(channel, method, properties, body):
    print("\nNotification microservice: Received a notification by " + __file__)
    processNotification(body)
    print()

def processNotification(notification):
    print("Notification microservice: Sending the notifications:")
    try:
        notification = json.loads(notification)
        print("--JSON:", notification)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", notification)
    print()