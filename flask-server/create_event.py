from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
import os
import sys
from datetime import datetime
from invokes import invoke_http
from os import environ

import amqp_connection
import pika
import json

app = Flask(__name__)
CORS(app)

event_url = environ.get('EVENT_URL') or "http://localhost:5000/event"
notification_url = environ.get("NOTIFICATION_URL") or "http://localhost:5005/notification"
recommendation_url = environ.get('RECOMMENDATION_URL') or "http://localhost:5100/recommendation"

exchangename = "create_event_topic"
exchangetype = "topic"

connection = amqp_connection.create_connection()
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

"""
Sample event JSON input:
{
    "event_name": "Picnic",
    "event_desc": "Picnic at Marina Bay",
    "start_time": "2021-10-01 15:00:00",
    "end_time": "2021-10-01 18:00:00",
    "time_out": "2021-09-30 23:59:59",
    "category": "Picnic",
    "township": "Marina Bay",
    "invitees": ["user2", "user3"],
    "user_id": "user1"
}

Sample event JSON output:
{
    "code": 201,
    "data": {
        "event_id": 1,
        "event_name": "Picnic",
        "event_desc": "Picnic at Marina Bay",
        "start_time": "2021-10-01 15:00:00",
        "end_time": "2021-10-01 18:00:00",
        "time_out": "2021-09-30 23:59:59",
        "category": "Picnic",
        "township": "Marina Bay",
        "invitees": [
            {
            'userID': 1
            'username': "user2",
            'email': "user2@email.com",
            'telegramtag': "@user2"
            },
            {
                'userID': 2
                'username': "user3",
                'email': "user3@email.com",
                'telegramtag': "@user3"
            }
        ],
        "user_id": "user1",
        "recommendations": [    
            {
                "recommendation_id": 1,
                "event_id": 1,
                "recommendation_name": "Pandan Reservoir Park",
                "recommendation_address": "700 W Coast Rd, Singapore 608785"
            }
        ]
    }
}
"""
@app.route("/create_event", methods=['POST'])
def create_event():
    if request.is_json:
        try:
            event = request.get_json()
            print("\nReceived event in JSON:", event)

            # 1. Send event info to event microservice
            result = processEvent(event)
            message = json.dumps(result)
            if result['code'] not in range(200, 300):
                channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=message, properties=pika.BasicProperties(delivery_mode=2))
                return result
            else:
                channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=message, properties=pika.BasicProperties(delivery_mode=2))

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "event.py internal error: " + ex_str
            }), 500
        
        try:
            recommendations = processRecommendation(event["category"], event["township"])
            message = json.dumps(recommendations)
            if recommendations['code'] not in range(200, 300):
                channel.basic_publish(exchange=exchangename, routing_key="create_event.error",body=message, properties=pika.BasicProperties(delivery_mode=2))
                return recommendations
            else:
                channel.basic_publish(exchange=exchangename, routing_key="create_event.notification",body=message, properties=pika.BasicProperties(delivery_mode=2))
        except:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "recommendation.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processEvent(event):
    createEvent = invoke_http(event_url, method='POST', json=event)
    return createEvent

def processRecommendation(category, township):
    search = {
        "type": category,
        "township": township
    }
    getRecommendation = invoke_http(recommendation_url, method='POST', json=search)
    return getRecommendation

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)