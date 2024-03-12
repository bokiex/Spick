from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Auth(db.Model):
    __tablename__ = 'authentication'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = Auth(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    # Initialize response structure
    response = {"message": "", "error": "", "debug":{}}
    status_code = 200

    data = request.get_json()

    # Check for missing data
    if not data or 'username' not in data or 'password' not in data:
        response['message'] = "Username and password are required."
        response['error'] = "MissingData"
        status_code = 400
        return jsonify(response), status_code

    # Attempt to retrieve the user by username
    try:
        user = Auth.query.filter_by(username=data['username']).first()
        if not user:
            response['message'] = "User not found."
            response['error'] = "UserNotFound"
            status_code = 404
        elif not user.check_password(data['password']):
            response['message'] = "Invalid password."
            response['error'] = "InvalidPassword"
            response['debug']['input_password'] = data['password']
            response['debug']['check_password_result'] = user.check_password(data['password'])
            status_code = 401
        else:
            response['message'] = "Login successful."
    except Exception as e:
        app.logger.error(f"Error during user lookup or password check: {e}")
        response['message'] = "An error occurred during login."
        response['error'] = "InternalError"
        status_code = 500

    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(debug=True)
