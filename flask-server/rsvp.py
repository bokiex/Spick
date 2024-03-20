#user_schedule returns all schedule linked to token if token provided GET
#optimize_schedule returns common timeslots when schedule provided via POST

#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URLs for the User Schedule, Optimize Schedule services, and Event Status Update
USER_SCHEDULE_SERVICE_URL = "http://localhost:5000/user_schedule"
OPTIMIZE_SCHEDULE_SERVICE_URL = "http://localhost:5001/optimize_schedule"
STATUS_UPDATE_URL = "http://localhost:5000/event"

# Sample Input for /rsvp/accept:
# {
#     "userID": 123,
#     "token": "event123",
#     "sched_list": [
#         {"eventID": 1, "userID": 123, "start_time": "2023-12-01T09:00:00", "end_time": "2023-12-01T10:00:00", "token": "event123"},
#         ...
#     ]
# }
# Sample Output for /rsvp/accept:
# {
#     "status": "accepted",
#     "message": "Acceptance processed and schedules posted successfully."
# }
@app.route("/rsvp/accept", methods=['POST'])
def accept_invitation():
    req_data = request.get_json()
    status_payload = {"status": "accepted", **req_data}
    try:
        status_response = requests.post(STATUS_UPDATE_URL, json=status_payload)
        if status_response.status_code in [200, 201]:
            schedule_response = requests.post(USER_SCHEDULE_SERVICE_URL, json={"sched_list": req_data.get('sched_list', [])})
            if schedule_response.status_code in [200, 201]:
                check_and_trigger_optimization(req_data)
                return jsonify({"status": "accepted", "message": "Acceptance processed and schedules posted successfully."}), 200
            else:
                return jsonify({"error": "Failed to post schedules."}), schedule_response.status_code
        else:
            return jsonify({"error": "Failed to update status to accepted."}), status_response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the service.", "detail": str(e)}), 502

# Sample Input for /rsvp/decline:
# {
#     "userID": 123,
#     "token": "event123"
# }
# Sample Output for /rsvp/decline:
# {
#     "status": "declined",
#     "message": "Decline processed successfully."
# }
@app.route("/rsvp/decline", methods=['POST'])
def decline_invitation():
    req_data = request.get_json()
    status_payload = {"status": "declined", **req_data}
    try:
        status_response = requests.post(STATUS_UPDATE_URL, json=status_payload)
        if status_response.status_code in [200, 201]:
            check_and_trigger_optimization(req_data)
            return jsonify({"status": "declined", "message": "Decline processed successfully."}), 200
        else:
            return jsonify({"error": "Failed to update status to declined."}), status_response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the service.", "detail": str(e)}), 502


def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    total_invitees = data.get('total_invitees')
    current_responses = data.get('current_responses')
    token = data.get('token')
    if total_invitees == current_responses:
        try:
            response = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json={"token": token})
            if response.status_code == 200:
                print("Optimization triggered successfully.")
            else:
                print("Failed to trigger optimization.")
        except requests.RequestException as e:
            print("Error connecting to Optimize Schedule service:", e)



# Input
# /rsvp/user_schedules?token=event123
            
#Output
#{
#   "schedules": [
#     {
#       "scheduleID": 1,
#       "eventID": 1,
#       "userID": 123,
#       "start_time": "2023-12-01T09:00:00",
#       "end_time": "2023-12-01T10:00:00",
#       "token": "event123"
#     },
#     ...
#   ]
# }                        
@app.route("/rsvp/user_schedules", methods=['GET'])
def get_all_schedules():
    # The token is now expected to be a query parameter in the request URL
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token query parameter is required."}), 400
    try:
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}?token={token}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the User Schedule service.", "detail": str(e)}), 502
    
# Input
# {
#   "token": "event123",
#   "userID": 123,
#   "scheduleID": 1
# }
# Output    
# {
#   "message": "Schedule deleted successfully."
# }    
@app.route("/rsvp/delete_schedule", methods=['DELETE'])
def delete_schedule():
    data = request.get_json()  # Assuming delete info comes in JSON format
    try:
        # It might be necessary to adjust this to properly pass data as query params
        response = requests.delete(USER_SCHEDULE_SERVICE_URL, json=data)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the User Schedule service.", "detail": str(e)}), 502


# Input
# {
#   "token": "event123"
# }
    
# Output
# {
#   "message": "Optimization successful",
#   "optimized_timeslots": [
#     {
#       "date": "2023-12-01",
#       "start_time": "11:00:00",
#       "end_time": "12:00:00"
#     },
#     ...
#   ]
# }        
@app.route("/rsvp/optimize", methods=['POST'])
def optimize_schedule():
    req_data = request.get_json()
    try:
        response = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=req_data)
        if response.status_code == 200:
            return jsonify({"message": "Optimization successful", "optimized_timeslots": response.json()}), 200
        else:
            return jsonify({"error": "Failed to optimize schedule."}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the Optimize Schedule service.", "detail": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)
