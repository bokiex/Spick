import telebot
import logging
import os
import sqlalchemy as db
import requests
from dotenv import load_dotenv
from flask import jsonify
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
notification_url = os.getenv('NOTIFICATION_URL') or "http://localhost:5000/chat/"
engine = db.create_engine('mysql+mysqlconnector://root@localhost:3306/notification') # For Windows
#engine = db.create_engine('mysql+mysqlconnector://is213@host.docker.internal:3306/notification')
connection = engine.connect()
metadata = db.MetaData()
notification = db.Table('notification', metadata, autoload_with=engine)
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Echo functionality
@bot.message_handler(func=lambda m: True)
def create_user(message):
	userid = message.chat.id
	username = message.chat.username
	try:
		result = requests.post(f"{notification_url}@{str(username)}", json={"chatid": str(userid), "telegramtag": username}) 
		data = result.json()
		bot.send_message(userid, data['message'])
	except Exception as e:        
		bot.reply_to(message, "An error occurred adding the user. Please try again later.")
		return jsonify({"message": "An error occurred adding the user."}), 500
	

bot.infinity_polling()