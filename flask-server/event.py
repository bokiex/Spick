#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/event'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = 'events'

    eventID = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(64), nullable=False)
    startTime = db.Column(db.TIMESTAMP, nullable=True)
    endTime = db.Column(db.TIMESTAMP, nullable=True)
    eventLocation = db.Column(db.String(64), nullable=True)
    
    def json(self):
        dto = {
            "eventID": self.eventID,
            "eventName": self.eventName,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "eventLocation": self.eventLocation
        }
        return dto

@app.route("/event", methods=['GET', 'POST', 'PUT', 'DELETE'])
def event():
    if request.method == "GET":
        if Event.query.all() == []:
            return jsonify({"message": "No events found."}), 404
        return jsonify({"events": [event.json() for event in Event.query.all()]}), 200
    
    elif request.method == "POST":
        req = request.get_json()
        if Event.query.filter_by(eventName=req['eventName']).first():
            return jsonify({"message": "An event with the same name already exists."}), 400
        
        event = Event(eventName=req['eventName'], eventLocation=req['eventLocation'])
        db.session.add(event)
        db.session.commit()
        return jsonify(event.json()), 201
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",  port=5000, debug=True)
    