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
                return jsonify({
                    "eventID": req_data.get('token'),  # Assuming token is used as eventID
                    "userID": req_data.get('userID'),
                    "status": 'Y'  # 'Y' to indicate acceptance
                }), 200
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
            return jsonify({
                "eventID": req_data.get('token'),  # Assuming token is used as eventID
                "userID": req_data.get('userID'),
                "status": 'N'  # 'N' to indicate decline
            }), 200
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
            response = requests.get(USER_SCHEDULE_SERVICE_URL, params={"token": token})
            if response.status_code == 200:
                payload = response.json()
                print("Retrieved schedule successfully.")
                try:
                    
                    opt = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=payload)
                    if opt.status_code ==200:
                        print("Schedule optimized successfully.")
                    else:
                        print("Failed to optimize schedule.")
                except requests.RequestException as e:
                    print("Error connecting to Optimize Schedule service:", e)
            else:
                print("Failed to retrieve schedule.")
        except requests.RequestException as e:
            print("Error connecting to User Schedule service:", e)



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
#     "2024-04-01": {
#         "attending_users": [
#             101,
#             102,
#             103
#         ],
#         "common_slots": [
#             {
#                 "end": "2024-04-01T10:00:00",
#                 "start": "2024-04-01T08:00:00"
#             }
#         ],
#         "non_attending_users": []
#     },
#     "2024-04-02": {
#         "attending_users": [
#             101,
#             102,
#             103
#         ],
#         "common_slots": [
#             {
#                 "end": "2024-04-02T09:30:00",
#                 "start": "2024-04-02T09:00:00"
#             }
#         ],
#         "non_attending_users": []
#     }
# }        
@app.route("/rsvp/optimize", methods=['POST'])
def optimize_schedule():
    req_data = request.get_json()
    token = req_data.get("token")  # Assuming the token is part of the request JSON

    if not token:
        return jsonify({"error": "Token is required."}), 400

    try:
        # Fetch schedules from User Schedule service using the token
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}?token={token}")
        if response.status_code == 200:
            schedule_data = response.json()  # Extract JSON data from the response

            try:
                # Post the fetched schedules to the Optimize Schedule service
                opt_response = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=schedule_data)  # Use extracted JSON data
                if opt_response.status_code == 200:
                    return jsonify({"message": "Optimization successful", "optimized_timeslots": opt_response.json()}), 200
                else:
                    return jsonify({"error": "Failed to optimize schedule."}), opt_response.status_code
            except requests.RequestException as e:
                return jsonify({"error": "Failed to connect to the Optimize Schedule service.", "detail": str(e)}), 502
        else:
            return jsonify({"error": "Failed to retrieve schedules from User Schedule service."}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the User Schedule service.", "detail": str(e)}), 502



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)
