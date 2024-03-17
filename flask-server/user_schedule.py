#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user_schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserSchedule(db.Model):
    __tablename__ = 'user_schedule'

    scheduleID = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), nullable=False)

    def json(self):
        return {
            "scheduleID": self.scheduleID,
            "eventID": self.eventID,
            "userID": self.userID,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "reason": self.reason,
            "token": self.token
        }

@app.route("/user_schedule", methods=['GET'])
def get_user_schedule():
    # Optional: Fetch schedules for a specific token if provided, else fetch all.
    token = request.args.get('token')
    if token:
        schedules = UserSchedule.query.filter_by(token=token).all()
    else:
        schedules = UserSchedule.query.all()

    if not schedules:
        return jsonify({"message": "No schedules found."}), 404

    # Format the schedules into the desired JSON structure.
    formatted_schedules = {"schedules": [schedule.json() for schedule in schedules]}

    return jsonify(formatted_schedules), 200

@app.route("/user_schedule", methods=['POST'])
def create_user_schedule():
    req = request.get_json()
    if not all(key in req for key in ['eventID', 'userID', 'start_time', 'end_time', 'token']):
        return jsonify({"message": "Missing required fields."}), 400
    
    schedule = UserSchedule(
        eventID=req['eventID'],
        userID=req['userID'],
        start_time=datetime.fromisoformat(req['start_time']),
        end_time=datetime.fromisoformat(req['end_time']),
        reason=req.get('reason', ''),
        token=req['token']
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.json()), 201

@app.route("/user_schedule/delete", methods=['DELETE'])
def delete_user_schedule():
    token = request.args.get('token')
    userID = request.args.get('userID')
    scheduleID = request.args.get('scheduleID')

    if not all([token, userID, scheduleID]):
        return jsonify({"message": "Token, userID, and scheduleID are required."}), 400

    schedule = UserSchedule.query.filter_by(scheduleID=scheduleID, userID=userID, token=token).first()
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({"message": "Schedule deleted successfully."}), 200
    else:
        return jsonify({"message": "Schedule not found or invalid token/userID."}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
