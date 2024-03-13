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
    eventID = db.Column(db.Integer, nullable=False)  # Now included
    userID = db.Column(db.Integer, nullable=False)   # Now included
    weekday = db.Column(db.CHAR(2), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    def json(self):
        return {
            "scheduleID": self.scheduleID,
            "eventID": self.eventID,
            "userID": self.userID,
            "weekday": self.weekday,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "reason": self.reason
        }

@app.route("/user_schedule", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_user_schedule():
    if request.method == "GET":
        schedules = UserSchedule.query.all()
        return jsonify({"schedules": [schedule.json() for schedule in schedules]}), 200 if schedules else ({"message": "No schedules found."}, 404)
    
    elif request.method == "POST":
        req = request.get_json()
        schedule = UserSchedule(
            eventID=req['eventID'],
            userID=req['userID'],
            weekday=req['weekday'],
            start_time=datetime.fromisoformat(req['start_time']),
            end_time=datetime.fromisoformat(req['end_time']),
            reason=req.get('reason')
        )
        db.session.add(schedule)
        db.session.commit()
        return jsonify(schedule.json()), 201
    
    elif request.method == "PUT":
        req = request.get_json()
        schedule_id = req.get('scheduleID')
        if not schedule_id:
            return jsonify({"message": "ScheduleID parameter missing."}), 400
        
        schedule = UserSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({"message": "Schedule not found."}), 404
        
        schedule.eventID = req.get('eventID', schedule.eventID)  # Update if provided
        schedule.userID = req.get('userID', schedule.userID)      # Update if provided
        schedule.weekday = req.get('weekday', schedule.weekday)  # Update if provided
        schedule.start_time = datetime.fromisoformat(req.get('start_time', schedule.start_time.isoformat()))
        schedule.end_time = datetime.fromisoformat(req.get('end_time', schedule.end_time.isoformat()))
        schedule.reason = req.get('reason', schedule.reason)
        
        db.session.commit()
        return jsonify(schedule.json()), 200
    
    elif request.method == "DELETE":
        event_id = request.args.get('eventID')
        user_id = request.args.get('userID')
        schedule_id = request.args.get('scheduleID')
        
        if not event_id or not user_id or not schedule_id:
            return jsonify({"message": "eventID, userID, and scheduleID parameters are required."}), 400
        
        schedule = UserSchedule.query.filter_by(eventID=event_id, userID=user_id, scheduleID=schedule_id).first()
        if not schedule:
            return jsonify({"message": "Schedule not found."}), 404
        
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({"message": "Schedule deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
