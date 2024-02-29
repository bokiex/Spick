import telebot
import logging
import os
import sqlalchemy as db
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

engine = db.create_engine('mysql+mysqlconnector://root@localhost:3306/notification') # For Windows
#engine = db.create_engine('mysql+mysqlconnector://is213@host.docker.internal:3306/notification')
connection = engine.connect()
metadata = db.MetaData()
notification = db.Table('notification', metadata, autoload_with=engine)
bot = telebot.TeleBot(bot_token, parse_mode=None)

# Echo functionality
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	print(message.text)
	bot.reply_to(message, message.text)

bot.infinity_polling()