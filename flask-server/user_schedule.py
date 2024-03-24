#ALL WORKING

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user_schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserSchedule(db.Model):
    __tablename__ = 'user_schedule'
    scheduleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eventID = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(255), nullable=False)

    def json(self):
        return {
            "scheduleID": self.scheduleID,
            "eventID": self.eventID,
            "user_id": self.user_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "token": self.token
        }

"""
provide token in url
http://localhost:5000/user_schedule?token=event123
"""
@app.route("/user_schedule", methods=['GET'])
def get_user_schedule():
    # Making token mandatory for the query
    token = request.args.get('eventID')
    if not token:
        return jsonify({"message": "EventID parameter is required."}), 400

    schedules = UserSchedule.query.filter_by(eventID=token).all()

    if schedules:
        return jsonify({"sched_list": [schedule.json() for schedule in schedules]}), 200
    else:
        return jsonify({"message": "No schedules found for provided token."}), 404


"""{
  "sched_list": [
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 101,
      "start_time": "2024-04-01T00:00:00",
      "end_time": "2024-04-01T10:00:00",
      "token": "event123"
    },
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 102,
      "start_time": "2024-04-01T00:00:00",
      "end_time": "2024-04-01T23:59:00",
      "token": "event123"
    },
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 103,
      "start_time": "2024-04-01T08:00:00",
      "end_time": "2024-04-01T11:00:00",
      "token": "event123"
    },
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 101,
      "start_time": "2024-04-02T08:00:00",
      "end_time": "2024-04-02T11:00:00",
      "token": "event123"
    },
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 102,
      "start_time": "2024-04-02T09:00:00",
      "end_time": "2024-04-02T11:30:00",
      "token": "event123"
    },
    {
      "scheduleID": 1,
      "eventID": 1,
      "user_id": 103,
      "start_time": "2024-04-02T09:00:00",
      "end_time": "2024-04-02T09:30:00",
      "token": "event123"
    }
  ]
}
"""
@app.route("/user_schedule", methods=['POST'])
def create_user_schedule():
    req = request.get_json()
    sched_list = req.get('sched_list')

    if not sched_list:
        return jsonify({"message": "Missing 'sched_list' in request."}), 400

    created_schedules = []

    for sched in sched_list:
        if not all(key in sched for key in ['eventID', 'user_id', 'start_time', 'end_time', 'token']):
            return jsonify({"message": "Missing required fields in one or more schedules."}), 400

        schedule = UserSchedule(
            eventID=sched['eventID'],
            user_id=sched['user_id'],
            start_time=datetime.fromisoformat(sched['start_time']),
            end_time=datetime.fromisoformat(sched['end_time']),
            token=sched['token']
        )

        db.session.add(schedule)
        try:
            db.session.commit()
            created_schedules.append(schedule.json())
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create schedule", "detail": str(e)}), 500

    return jsonify({"created_schedules": created_schedules}), 201


"""

"""

@app.route("/user_schedule", methods=['DELETE'])
def delete_user_schedule():
    req = request.get_json()
    token = req.get('eventID')
    user_id = req.get('user_id')
    scheduleID = req.get('scheduleID')

    if not all([token, user_id, scheduleID]):
        return jsonify({"message": "Token, user_id, and scheduleID are required in the JSON payload."}), 400

    schedule = UserSchedule.query.filter_by(scheduleID=scheduleID, user_id=user_id, token=token).first()
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({"message": "Schedule deleted successfully."}), 200
    else:
        return jsonify({"message": "Schedule not found or invalid token/user_id."}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
