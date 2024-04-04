import requests
import amqp_connection
import json
import threading
from os import environ
from telebot import TeleBot
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

bot_token = environ.get('TELEGRAM_BOT_API_KEY')
user_ms = f"http://{environ.get("USER_MS")}:{environ.get("USER_MS_PORT")}/users/"
bot = TeleBot(bot_token)
n_queue_name = environ.get('NOTIFICATION_QUEUE_NAME') or "Notification"
def receiver():
    connection = amqp_connection.create_connection()
    channel = connection.channel()
    channel.queue_declare(queue=n_queue_name, durable=True)

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
            return users.json()
        users = users.json()
    
        for user in users:
            
            if user['telegram_id'] == None or user['telegram_tag'] not in notification_list:
                continue
            #sendurl = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + user["telegram_id"] + "&text=" + chatmsg
            bot.send_message(user["telegram_id"], message)
            countnotif += 1
        if countnotif == 0:
            print("No users found to send notifications to.")
        else:
            successmsg = f"Notification successfully sent. {str(countnotif)} notifications were sent."
            print(successmsg)
            
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
    update = requests.put(user_ms + f"telegram/{user['user_id']}", json=user)
    
    if update.status_code in range(300, 599):
        msg = "An error occurred updating the user."
    else:
        msg = "Your account is now tied to your telegram tag."
    return bot.send_message(telegram_id, msg)

if __name__ == "__main__":
    print("Starting AMQP thread")
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()

    print("Starting Telegram bot thread")
    bot.polling()
    receiver_thread.join()