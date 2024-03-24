#user_schedule returns all schedule linked to token if token provided GET
#optimize_schedule returns common timeslots when schedule provided via POST

#!/usr/bin/env python3

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URLs for the User Schedule, Optimize Schedule services, and Event Status Update
USER_SCHEDULE_SERVICE_URL = "http://localhost:5000/user_schedule"
OPTIMIZE_SCHEDULE_SERVICE_URL = "http://localhost:5001/optimize_schedule"
UPDATE_RESPONSES_URL = "http://127.0.0.1:8000/invitee"
VALUE_RETRIEVE_URL = "http://127.0.0.1:8000/invitee/"

# Sample Input for /rsvp/accept:
# {
#     "user_id": 2,
#     "token": "event123",
#     "eventID": 1,
#     "sched_list": [
#         {"eventID": 1, "user_id": 2, "start_time": "2023-12-01T09:00:00", "end_time": "2023-12-01T10:00:00", "token": "event123"}
#     ]
# }
# Sample Output for /rsvp/accept:
# {
#     "Message": "Successfully accepted and posted user's schedules.",
#     "Optimize Status": {
#         "message": "Optimization not triggered, condition not met."
#     }
# }
@app.route("/rsvp/accept", methods=['PUT', 'POST', 'GET'])
def accept_invitation():
    req_data = request.get_json()
    
    # Constructing the payload for the FastAPI service
    update_payload = {
        "event_id": req_data.get('eventID'),  # Make sure the field names match the FastAPI's expected schema
        "user_id": req_data.get('user_id'),    # You might need to adjust field names to match the schema exactly
        "status": "Y"  # Directly setting status to "Y"
    }
    
    try:
        # Sending a PUT request to the FastAPI service to update the invitee
        status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
        
        if status_response.status_code < 400:
            # Assuming successful update, proceed to post the schedules to your service
            schedule_response = requests.post(USER_SCHEDULE_SERVICE_URL, json={"sched_list": req_data.get('sched_list', [])})
            if schedule_response.status_code in [200, 201]:
                retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{req_data.get('eventID')}")
                if retrieve_response.status_code == 200:
                    opt_data = retrieve_response.json()  # Convert the response to JSON
                    opt_data["eventID"] = req_data.get('eventID')
                    # Now you can process opt_data as needed
                    # e.g., check_and_trigger_optimization(opt_data)
                    x = check_and_trigger_optimization(opt_data)
                    x = x.get_json()
                    return jsonify({"Message": "Successfully accepted and posted user's schedules.", "Optimize Status":x})
                else:
                    return jsonify({"error": "Unable to retrieve value from event service."})
            else:
                return jsonify({"error": "Failed to post schedules."}), schedule_response.status_code
        else:
            return jsonify({"error": "Failed to update status to accepted."}), status_response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the service.", "detail": str(e)}), 502



# Sample Input for /rsvp/decline:
# {
#     "user_id": 123,
#     "token": "event123"
# }
# Sample Output for /rsvp/decline:
# {
#     "Message": "User status set to declined.",
#     "Optimize Status": {
#         "message": "Schedule optimized successfully.",
#         "result": {
#             "2023-12-01": {
#                 "attending_users": [
#                     2
#                 ],
#                 "common_slot": {
#                     "end": "2023-12-01T10:00:00",
#                     "start": "2023-12-01T09:00:00"
#                 },
#                 "non_attending_users": []
#             }
#         }
#     }
# }
@app.route("/rsvp/decline", methods=['PUT'])
def decline_invitation():
    req_data = request.get_json()
    update_payload = {
        "event_id": req_data.get('eventID'),  # Ensure these match the FastAPI schema
        "user_id": req_data.get('user_id'),    # Adjust if necessary to match the schema
        "status": "N"  # Setting status to "N" for decline
    }
    try:
        # Sending a PUT request to update the status to "N" (declined)
        status_response = requests.put(UPDATE_RESPONSES_URL, json=update_payload)
        if status_response.status_code < 400:
            # If update is successful, proceed to possibly trigger optimization
            retrieve_response = requests.get(f"{VALUE_RETRIEVE_URL}{req_data.get('eventID')}")
            if retrieve_response.status_code == 200:
                opt_data = retrieve_response.json()  # Convert the response to JSON
                opt_data["eventID"] = req_data.get('eventID')
                # Now you can process opt_data as needed
                # e.g., check_and_trigger_optimization(opt_data)
                x = check_and_trigger_optimization(opt_data)
                x = x.get_json()
                return jsonify({"Message": "User status set to declined.", "Optimize Status":x})
            return jsonify({"message": "Updated to decline successfully.", "Optimize Status":"Unable to reach optimize service."})
        else:
            return jsonify({"error": "Failed to update status to declined."}), status_response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the service.", "detail": str(e)}), 502



def check_and_trigger_optimization(data):
    # Assuming the total_invitees and current_responses are fetched from the event status update response or elsewhere
    total_invitees = len(data.get('all_invitees'))
    current_responses = len(data.get('respondents'))
    token = data.get('eventID')
    if total_invitees == current_responses:
        try:
            response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}?eventID={token}")
            if response.status_code == 200:
                payload = response.json()
                try:
                    opt = requests.post(OPTIMIZE_SCHEDULE_SERVICE_URL, json=payload)
                    if opt.status_code < 400:
                        opt = opt.json()
                        return jsonify({"message": "Schedule optimized successfully.", "result":opt}) 
                    else:
                        return jsonify({"error": "Failed to optimize schedule."}) 
                except requests.RequestException as e:
                    return jsonify({"error": "Error connecting to Optimize Schedule service.", "detail": str(e)})
            else:
                return jsonify({"error": "Failed to retrieve schedule."}) 
        except requests.RequestException as e:
            return jsonify({"error": "Error connecting to User Schedule service.", "detail": str(e)})
    else:
        # Condition where total_invitees != current_responses
        return jsonify({"message": "Optimization not triggered, condition not met."})



# Input
# /rsvp/user_schedules?token=event123
            
#Output
#{
#   "schedules": [
#     {
#       "scheduleID": 1,
#       "eventID": 1,
#       "user_id": 123,
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
    token = request.args.get('eventID')
    if not token:
        return jsonify({"error": "Token query parameter is required."}), 400
    try:
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}?eventID={token}")
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Failed to connect to the User Schedule service.", "detail": str(e)}), 502
    
# Input
# {
#   "token": "event123",
#   "user_id": 123,
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
    token = req_data.get("eventID")  # Assuming the token is part of the request JSON

    if not token:
        return jsonify({"error": "eventID is required."}), 400

    try:
        # Fetch schedules from User Schedule service using the token
        response = requests.get(f"{USER_SCHEDULE_SERVICE_URL}?eventID={token}")
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
