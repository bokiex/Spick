#ALL WORKING
from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

def find_common_slots(schedules):
    schedules_by_day = defaultdict(lambda: defaultdict(list))
    for schedule in schedules:
        start = datetime.strptime(schedule['start_time'], "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(schedule['end_time'], "%Y-%m-%dT%H:%M:%S")
        schedules_by_day[start.date()][schedule['userID']].append((start, end))

    results = {}
    for day, users_schedules in schedules_by_day.items():
        time_blocks = []
        for times in users_schedules.values():
            for start, end in times:
                time_blocks.append((start, 'start'))
                time_blocks.append((end, 'end'))
        time_blocks.sort()

        common_times = []
        current_attendees = 0
        max_attendees = 0
        current_start = None

        for time, event in time_blocks:
            if event == 'start':
                current_attendees += 1
                if current_attendees > max_attendees:
                    max_attendees = current_attendees
                    current_start = time
            else:
                if current_attendees == max_attendees:
                    common_times.append((current_start, time))
                current_attendees -= 1
        
        attending_users = set()
        for user_id, times in users_schedules.items():
            for common_start, common_end in common_times:
                if any(start <= common_start and end >= common_end for start, end in times):
                    attending_users.add(user_id)
                    break

        non_attending_users = set(users_schedules.keys()) - attending_users

        # Adjust common times if there is only one attending user
        if len(attending_users) == 1:
            user_id = next(iter(attending_users))
            common_times = users_schedules[user_id]

        results[str(day)] = {
            'common_slots': [{'start': slot[0].strftime("%Y-%m-%dT%H:%M:%S"), 'end': slot[1].strftime("%Y-%m-%dT%H:%M:%S")} for slot in common_times],
            'attending_users': list(attending_users),
            'non_attending_users': list(non_attending_users)
        }

    return results

@app.route('/optimize_schedule', methods=['POST'])
def optimize_schedule():
    sched_list = request.json.get('sched_list', [])
    common_slots_by_day = find_common_slots(sched_list)
    return jsonify(common_slots_by_day)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
