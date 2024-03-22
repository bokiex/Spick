from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

def find_overlapping_times(schedules):
    # Organize schedules by day for processing
    schedules_by_day = defaultdict(list)
    for schedule in schedules:
        start = datetime.strptime(schedule['start_time'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(schedule['end_time'], "%Y-%m-%dT%H:%M:%S")
        schedules_by_day[start.date()].append((start, end, schedule['userID']))
    
    optimized_schedules = {}

    for day, day_schedules in schedules_by_day.items():
        # Sort by start time, then by end time
        day_schedules.sort(key=lambda x: (x[0], x[1]))

        # Finding overlapping times
        time_blocks = []
        for schedule in day_schedules:
            start, end, user_id = schedule
            time_blocks.append((start, 'start', user_id))
            time_blocks.append((end, 'end', user_id))
        time_blocks.sort()

        attendees = defaultdict(int)
        current_attendees = set()
        best_overlap = 0
        best_times = None
        for time, event, user_id in time_blocks:
            if event == 'start':
                current_attendees.add(user_id)
                if len(current_attendees) > best_overlap:
                    best_overlap = len(current_attendees)
                    best_times = (time, None)  # Update start time of best overlap
            else:
                if len(current_attendees) == best_overlap and best_times[1] is None:
                    best_times = (best_times[0], time)  # Update end time of best overlap
                current_attendees.remove(user_id)

        if best_times:
            # Identifying users who can attend the best overlapping time
            attending_users = set()
            non_attending_users = set()
            for start, end, user_id in day_schedules:
                if start <= best_times[0] and end >= best_times[1]:
                    attending_users.add(user_id)
                else:
                    non_attending_users.add(user_id)

            optimized_schedules[str(day)] = {
                'common_slot': {
                    'start': best_times[0].strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': best_times[1].strftime("%Y-%m-%dT%H:%M:%S") if best_times[1] else None,
                },
                'attending_users': list(attending_users),
                'non_attending_users': list(non_attending_users),
            }

    return optimized_schedules

@app.route('/optimize_schedule', methods=['POST'])
def optimize_schedule():
    sched_list = request.json.get('sched_list', [])
    common_slots_by_day = find_overlapping_times(sched_list)
    return jsonify(common_slots_by_day)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
