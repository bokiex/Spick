import sqlalchemy as db
import requests
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

app = FastAPI()

def receiver():
    connection = amqp_connection.create_connection()
    channel = connection.channel()
    channel.queue_declare(queue="Notification", durable=True)

    def callback(channel, method, properties, body):
        print("\nNotification microservice: Received a notification by " + __file__)
        processNotification(body)
        print()

    def processNotification(notification):
        countnotif = 0
        print(notification)

        notification_list = notification['notification_list']
        message = notification['message']
        users = requests.get(user_ms)
        for user in users:
            if user['telegram_id'] == None or user['telegram_tag'] not in notification_list:
                continue

            
            #sendurl = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + user["telegram_id"] + "&text=" + chatmsg
            bot.send_message(user["telegram_id"], message)
            countnotif += 1
        else:
            successmsg = f"Notification was successful. {str(countnotif)} notifications were sent."
            return jsonify(
                {
                    "code": 200,
                    "message": successmsg
                }
            ), 200

    channel.basic_consume(queue="Notification", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@bot.message_handler(func=receiver())
def echo_msg(message):
    pass

