#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<username>:<password>@localhost:3306/user_schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserSchedule(db.Model):
    __tablename__ = 'user_schedule'

    id = db.Column(db.Integer, primary_key=True)
    eventID = db.Column(db.Integer, nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    def json(self):
        return {
            "id": self.id,
            "eventID": self.eventID,
            "userID": self.userID,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "reason": self.reason
        }

@app.route("/user_schedule", methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_user_schedule():
    if request.method == "GET":
        schedules = UserSchedule.query.all()
        if not schedules:
            return jsonify({"message": "No schedules found."}), 404
        return jsonify({"schedules": [schedule.json() for schedule in schedules]}), 200
    
    elif request.method == "POST":
        req = request.get_json()
        schedule = UserSchedule(
            eventID=req['eventID'],
            userID=req['userID'],
            start_time=req['start_time'],
            end_time=req['end_time'],
            reason=req.get('reason')
        )
        db.session.add(schedule)
        db.session.commit()
        return jsonify(schedule.json()), 201
    
    elif request.method == "PUT":
        req = request.get_json()
        schedule_id = req.get('id')
        if not schedule_id:
            return jsonify({"message": "ID parameter missing."}), 400
        
        schedule = UserSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({"message": "Schedule not found."}), 404
        
        # Update schedule attributes if provided in request
        if 'eventID' in req:
            schedule.eventID = req['eventID']
        if 'userID' in req:
            schedule.userID = req['userID']
        if 'start_time' in req:
            schedule.start_time = req['start_time']
        if 'end_time' in req:
            schedule.end_time = req['end_time']
        if 'reason' in req:
            schedule.reason = req['reason']
        
        db.session.commit()
        return jsonify(schedule.json()), 200
    
    elif request.method == "DELETE":
        schedule_id = request.args.get('id')
        if not schedule_id:
            return jsonify({"message": "ID parameter missing."}), 400
        
        schedule = UserSchedule.query.get(schedule_id)
        if not schedule:
            return jsonify({"message": "Schedule not found."}), 404
        
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({"message": "Schedule deleted successfully."}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)