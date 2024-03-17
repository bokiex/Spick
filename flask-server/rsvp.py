#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URLs for each service
USER_SCHEDULE_SERVICE_URL = "http://localhost:5000/user_schedule"
OPTIMIZE_SCHEDULE_SERVICE_URL = "http://localhost:5001/optimize_schedule"
COUNTER_SERVICE_URL = "http://localhost:5002/counter"
TIMEOUT_SERVICE_URL = "http://localhost:5003/timeout"

@app.route("/rsvp", methods=['POST'])
def handle_rsvp():
    req_data = request.get_json()
    token = req_data['token']

    # Check if the token has expired using the Timeout Service
    timeout_response = requests.get(f"{TIMEOUT_SERVICE_URL}?token={token}")
    if timeout_response.status_code != 200 or timeout_response.json().get('expired', False):
        return jsonify({"message": "Sorry, the event is no longer accepting responses."}), 400

    # Update the Counter Service with the response
    counter_response = requests.post(COUNTER_SERVICE_URL, json={"token": token, "response": req_data['response']})
    if counter_response.status_code != 200:
        return jsonify({"error": "Failed to update counter"}), counter_response.status_code

    # If the response is "accept", save to User Schedule
    if req_data['response'] == "accept":
        schedule_response = requests.post(USER_SCHEDULE_SERVICE_URL, json={"token": token, **req_data})
        if schedule_response.status_code != 201:
            return jsonify({"error": "Failed to save schedule"}), schedule_response.status_code

    # Optionally, trigger the Optimizing Service here if certain conditions are met
    # This could depend on the Counter Service's response or other logic

    return jsonify({"message": "RSVP processed successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)
