from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
import bisect

app = Flask(__name__)

def calculate_available_times(schedules):
    # Organize schedules by token and date
    event_schedules = defaultdict(lambda: defaultdict(list))
    for schedule in schedules:
        token = schedule['token']
        date = datetime.strptime(schedule['start_time'], "%Y-%m-%dT%H:%M:%S").date()
        start_time = datetime.strptime(schedule['start_time'], "%Y-%m-%dT%H:%M:%S").time()
        end_time = datetime.strptime(schedule['end_time'], "%Y-%m-%dT%H:%M:%S").time()
        event_schedules[token][date].append((start_time, end_time))

    event_availability = {}
    for token, dates in event_schedules.items():
        event_availability[token] = {}
        for date, times in dates.items():
            # Sort times and merge any overlapping timeslots
            sorted_times = sorted(times)
            merged_times = [sorted_times[0]]
            for current_start, current_end in sorted_times[1:]:
                last_end = merged_times[-1][1]
                if current_start <= last_end:
                    merged_times[-1] = (merged_times[-1][0], max(last_end, current_end))
                else:
                    merged_times.append((current_start, current_end))

            # Calculate available times
            available_times = []
            if merged_times[0][0] != datetime.strptime("00:00", "%H:%M").time():
                available_times.append(("00:00", merged_times[0][0].strftime("%H:%M")))
            for i in range(len(merged_times) - 1):
                available_times.append((merged_times[i][1].strftime("%H:%M"), merged_times[i + 1][0].strftime("%H:%M")))
            if merged_times[-1][1] != datetime.strptime("23:59", "%H:%M").time():
                available_times.append((merged_times[-1][1].strftime("%H:%M"), "23:59"))

            event_availability[token][str(date)] = available_times

    return event_availability

@app.route('/optimize_schedule', methods=['POST'])
def optimize_schedule():
    schedules_data = request.json.get('schedules', [])
    available_times = calculate_available_times(schedules_data)
    return jsonify(available_times)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
