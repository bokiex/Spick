from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Add your optimization logic here

def find_common_time(users_schedules):
    # Define the time range for comparison, from 9am to 9pm
    start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=12)

    # Initialize a dictionary to count the availability for each time slot
    availability_counts = {}

    # Count the availability for each time slot
    for user_schedule in users_schedules:
        user_start_time = max(user_schedule['start_time'], start_time)
        user_end_time = min(user_schedule['end_time'], end_time)

        # Iterate over each hour within the time range
        current_time = user_start_time
        while current_time <= user_end_time:
            # Increment the availability count for this time slot
            availability_counts[current_time] = availability_counts.get(current_time, 0) + 1

            # Move to the next hour
            current_time += timedelta(hours=1)

    # Calculate the percentage of users available for each time slot
    total_users = len(users_schedules)
    common_times = []
    for time_slot, count in availability_counts.items():
        # Check if the percentage of availability is greater than or equal to 60%
        if (count / total_users) * 100 >= 60:
            # Check if the duration of the time slot is at least 1 hour
            if time_slot + timedelta(hours=1) in availability_counts:
                common_times.append((time_slot, (count / total_users) * 100))

    # Sort common times by availability percentage
    common_times.sort(key=lambda x: x[1], reverse=True)

    if common_times:
        return common_times
    else:
        return "Not enough participants available."
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)