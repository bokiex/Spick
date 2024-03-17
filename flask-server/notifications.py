## Microservice to work with telegram API ##
import requests
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import amqp_connection
import json
import pika
from os import environ
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/notification'  #For Mac
# for windows
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/notification'
#USE FOR DOCKER ONLY. UNCOMMENT THIS AND COMMENT OUT THE is213@localhost DATABASE URL WHEN USING DOCKER-------------------
#from os import environ
#app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#------------------------------------------------------------------------------------------
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
token = "6996801409:AAGDWkgPaCtRAqH08y9lwYJQif6ESOnQ984"

db = SQLAlchemy(app)
n_queue_name = environ.get('Notification') or "Notification"  # Notification

class Notification(db.Model):
    __tablename__ = 'notification'

    chatid = db.Column(db.String(64), primary_key=True)
    telegramtag = db.Column(db.String(64), nullable=False)

    def __init__(self, chatid, telegramtag):
        self.chatid = chatid
        self.telegramtag = telegramtag

    def json(self):
        return {"chatid": self.chatid, "telegramtag": self.telegramtag}


def receiveNotification(channel):
    try:
        channel.basic_consume(queue=n_queue_name, on_message_callback=callback, auto_ack=True)
        print('Error microservice: Consuming from queue:', n_queue_name)
        channel.start_consuming()
        
    except pika.exceptions.AMQPError as e:
        print(f"Error microservice: Failed to connect: {e}")
        
    except KeyboardInterrupt:
        print("Error microservice: Program interrupted by user.")
        
        
def callback(channel, method, properties, body):
    print("\nError microservice: Received an error by " + __file__)
    processNotification(body)
    print()
    
@app.route("/chat")
def get_all():
    chatlist = Notification.query.all()
    if len(chatlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "chats": [chat.json() for chat in chatlist]
                },
                'message': 'Successfully retrieved chat ids'
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no chat ids."
        }
    ), 404


@app.route("/chat/<string:telegramtag>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def notification(telegramtag):
    if request.method == 'GET':
        notif = Notification.query.filter_by(telegramtag=telegramtag).first()
        if notif:
            return jsonify(
                {
                    "code": 200,
                    "data": notif.json(),
                    'message': 'Notification details found'
                }
            )
        return jsonify(
            {
                "code": 404,
                "message": "Notification details not found."
            }
        ), 404
    elif request.method == "POST":
        if (Notification.query.filter_by(telegramtag=telegramtag).first()):
            return jsonify(
            {
                "code": 400,
                "data": {
                    "telegramtag": telegramtag
                },
                "message": "Notification details already exists."
            }
        ), 400

        data = request.get_json()
        print(data['chatid'])
        notif = Notification(data['chatid'], telegramtag)

        try:
            db.session.add(notif)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "chatid": data['chatid'],
                        "telegramtag": telegramtag
                    },
                    "message": "An error occurred adding your notification details to database."
                }
            ), 500

        return jsonify(
            {
                "code": 201,
                "data": notif.json(),
                'message': 'Notification details added.'
            }
        ), 201

def processNotification(event):
    countnotif = 0
    data = request.get_json()
    notiflist = data['invitees']
    for user in notiflist:
        if (Notification.query.filter_by(telegramtag=user).first()):
            notif = Notification.query.filter_by(telegramtag=user).first()
            notifinfo = notif.json()
            chatid = notifinfo["chatid"]
            chatmsg = "{host} has invited you to an event! Check it out on Spick now!"
            sendurl = "https://api.telegram.org/bot" + token + \
                "/sendMessage" + "?chat_id=" + chatid + "&text=" + chatmsg
            r = requests.get(sendurl)
            countnotif += 1
    if countnotif == 0:
        return jsonify(
            {
                "code": 404,
                "message": "Data sent does not match any records in database. Notification was unsuccessful. No notifs sent."
            }
        ), 404
    else:
        successmsg = f"Notification was successful. {str(countnotif)} notifications were sent."
        return jsonify(
            {
                "code": 200,
                "message": successmsg
            }
        ), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0",  port=5000, debug=True)
    print("Error microservice: Getting Connection")
    connection = amqp_connection.create_connection()
    print("Error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)