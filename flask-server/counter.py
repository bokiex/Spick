# when event created, POST request to RSVP which routes POST request into counter db (token and total invitees)
# db will look like

# one table
# | token | total inv | current reponses | 

#token table
# | token | userID


## user clicks accept/decline
# each response will trigger rsvp to route to counter with the event token and user id
# counter will +1 in the current responses for the even token if the user id is unique.
# when current responses = total inv , send http to RSVP to trigger optimize for that event token


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/counter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class EventStatus(db.Model):
    __tablename__ = 'eventstatus'
    token = db.Column(db.String(255), primary_key=True)
    total_invitees = db.Column(db.Integer, nullable=False)
    current_responses = db.Column(db.Integer, default=0, nullable=False)

class Response(db.Model):
    __tablename__ = 'responses'
    responseid = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), db.ForeignKey('eventstatus.token'), nullable=False)
    userID = db.Column(db.Integer, nullable=False)
    # Removed unique=True constraint to allow multiple events per user
    __table_args__ = (db.UniqueConstraint('token', 'userID', name='_token_userID_uc'),)

@app.route('/counter', methods=['POST'])
def handle_counter():
    data = request.json
    # Check if data includes 'total_invitees' to determine action
    if 'total_invitees' in data:
        # Create Event logic
        return create_event(data)
    if 'userID' in data:
        # Add Response logic
        return add_response(data)
        
    if 'userID' not in data and 'total_invitees' not in data:
        # if both missing
        return jsonify({"error": "Please provide userID and/or total_invitees."}), 400

    
def trigger_optimization(token):
    url = "http://localhost:5100/rsvp"
    payload = {"token": token}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Optimization triggered successfully for token:", token)
            return True, "Optimization triggered successfully."
        else:
            print(f"Failed to trigger optimization for token: {token}, Status Code: {response.status_code}")
            return False, f"Failed to trigger optimization, Status Code: {response.status_code}"
    except requests.RequestException as e:
        print("HTTP Request failed:", e)
        return False, "HTTP request to trigger optimization failed."


def create_event(data):
    try:
        event = EventStatus(token=data['token'], total_invitees=data['total_invitees'])
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Event with this token already exists."}), 400

def add_response(data):
    try:
        response = Response(token=data['token'], userID=data['userID'])
        db.session.add(response)
        db.session.commit()
        # Update the current responses count for the event
        event = EventStatus.query.filter_by(token=data['token']).first()
        if event:
            event.current_responses = Response.query.filter_by(token=data['token']).count()
            db.session.commit()
            # Check if optimization should be triggered
            if event.current_responses == event.total_invitees:
                # Placeholder for optimization trigger logic
                success, message = trigger_optimization(event.token)
                if not success:
                    # Optimization trigger failed, reflect that in the response
                    return jsonify({"message": "Response recorded, but optimization trigger failed.", "error": message}), 500
            return jsonify({"message": "Response recorded successfully."}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "This user has already responded to this event."}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
