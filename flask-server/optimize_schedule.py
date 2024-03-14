from datetime import datetime, timedelta
from collections import defaultdict
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_schedules():
    # Replace with actual fetch from your service
    schedule_service_url = 'http://localhost:5000/user_schedule'
    try:
        response = requests.get(schedule_service_url)
        if response.status_code == 200:
            return response.json()['schedules']
        else:
            print(f"Failed to fetch schedules: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

def initialize_week():
    # Initializes full availability for a week with simplification (whole day available)
    return {day: [('00:00', '23:59')] for day in ["M", "T", "W", "Th", "F", "Sa", "Su"]}

def mark_unavailable_times(week, schedules):
    for schedule in schedules:
        weekday = schedule['weekday']
        start = datetime.strptime(schedule['start_time'], "%Y-%m-%dT%H:%M:%S").time()
        end = datetime.strptime(schedule['end_time'], "%Y-%m-%dT%H:%M:%S").time()
        
        # Assuming a simplified model: only keep timeslots that don't intersect with the schedule
        if start == datetime.strptime('00:00', "%H:%M").time() and end == datetime.strptime('23:59', "%H:%M").time():
            week[weekday] = []  # The whole day is booked
        else:
            # Update available slots for the day
            new_slots = []
            for avail_start, avail_end in week[weekday]:
                avail_start_dt = datetime.strptime(avail_start, "%H:%M")
                avail_end_dt = datetime.strptime(avail_end, "%H:%M")
                start_dt = datetime.combine(avail_start_dt.date(), start)
                end_dt = datetime.combine(avail_end_dt.date(), end)

                if start_dt.time() > avail_start_dt.time():
                    new_slots.append((avail_start, start_dt.strftime("%H:%M")))
                if end_dt.time() < avail_end_dt.time():
                    new_slots.append((end_dt.strftime("%H:%M"), avail_end))
            
            week[weekday] = new_slots

    return week

def find_common_availability(schedules):
    event_schedules = defaultdict(list)
    for schedule in schedules:
        event_schedules[schedule['eventID']].append(schedule)
    
    event_availability = {}
    for event_id, schedules in event_schedules.items():
        week = initialize_week()
        week = mark_unavailable_times(week, schedules)
        event_availability[event_id] = week
    
    return event_availability

@app.route('/optimize_schedule', methods=['GET'])
def optimize_schedule():
    schedules_data = fetch_schedules()  # This should ideally be replaced with a real fetch
    available_times = find_common_availability(schedules_data)
    return jsonify(available_times)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
