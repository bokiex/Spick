import sqlalchemy as db
import requests
import amqp_connection
import json
import threading
import asyncio
from telebot import TeleBot
from os import environ
from flask import jsonify
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

bot_token = environ.get('BOT_TOKEN') or "6996801409:AAGDWkgPaCtRAqH08y9lwYJQif6ESOnQ984"
user_ms = environ.get("USER_URL") or "http://127.0.0.1:8001/users/"  #change back to your own localhost @john
notification_ms = environ.get("NOTIFICATION_URL") or "http://localhost:8002/notification/"  #^^
bot = TeleBot(bot_token)

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
        print(notification.decode())
        notification = notification.decode().replace("\r\n", "")

        notification = json.loads(notification)
        notification_list = notification['notification_list']
        message = notification['message']
        users = requests.get(user_ms)

        if users.status_code in range(300, 599):
            return JSONResponse(status_code=users.status_code, content={"message":users.json()["detail"]})
        users = users.json()
    
        for user in users:
            
            if user['telegram_id'] == None or user['telegram_tag'] not in notification_list:
                continue
            #sendurl = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + user["telegram_id"] + "&text=" + chatmsg
            bot.send_message(user["telegram_id"], message)
            countnotif += 1
        else:
            successmsg = f"Notification successfully sent. {str(countnotif)} notifications were sent."
            JSONResponse(status_code=200, content={"message":successmsg})
            
    channel.basic_consume(queue="Notification", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    
    telegram_id = message.chat.id
    telegram_tag = message.chat.username
    msg = ""
        
    user = requests.get(user_ms + f"telegram/{telegram_tag}")
    if user.status_code in range(300, 599):
        msg = "User not found. Have you created an account yet?"
        return bot.send_message(telegram_id, msg)
    
    user = user.json()
    user["telegram_id"] = str(telegram_id)
    print(user)
    update = requests.put(user_ms + f"{user['user_id']}", json=jsonable_encoder(user))
    
    if update.status_code in range(300, 599):
        msg = "An error occurred updating the user."
    msg = "Your account is now tied to your telegram tag."
    return bot.send_message(telegram_id, msg)

if __name__ == "__main__":
    print("Starting AMQP thread")
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()

    print("Starting Telegram bot thread")
    bot.polling()
    receiver_thread.join()