import telebot
import logging
import sqlalchemy as db
import requests
from os import environ
from flask import jsonify
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()
bot_token = environ.get('BOT_TOKEN') or "YOUR_BOT_TOKEN_HERE"
user_ms = environ.get("USER_URL") or "http://localhost:8000/users/"
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:5000/notification/"
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Echo functionality
@bot.message_handler(func=lambda m: True)
def create_user(message):
	telegram_id = message.chat.id
	telegram_tag = message.chat.username
	try:
		result = update_user_by_telegram_tag(telegram_id, telegram_tag)
		data = result.json()
		bot.send_message(telegram_id, data['message'])
	except Exception as e:        
		bot.reply_to(message, "An error occurred adding the user. Please try again later.")
		return jsonify({"message": "An error occurred adding the user."}), 500
	
bot.infinity_polling()

# Update user by telegram tag
def update_user_by_telegram_tag(telegram_id: str, telegram_tag: str):
    user = requests.get(user_ms + telegram_tag)
    if int(user.status_code) > 300:
		#channel.basic_publish(exchange=exchangename, routing_key="update.error", body=json.dumps({"telegram_id": telegram_id, "telegram_tag": telegram_tag}))
        raise Exception()
    user = user.json()
    user["telegram_id"] = telegram_id
	
    result = requests.put(user_ms + telegram_tag, json=user)
    if int(result.status_code) > 300:
        raise Exception()
    return {"message": "Your account is now tied to your telegram tag.", "user": result.json()}
