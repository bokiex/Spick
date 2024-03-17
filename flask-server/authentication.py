from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Auth(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    telegramtag = db.Column(db.String(64), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = Auth(username=data['username'], email=data['email'], telegramtag=data['telegramtag'])
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
            response['userID'] = user.userID
    except Exception as e:
        app.logger.error(f"Error during user lookup or password check: {e}")
        response['message'] = "An error occurred during login."
        response['error'] = "InternalError"
        status_code = 500

    return jsonify(response), status_code

# New /user/<int:user_id> route
@app.route('/user/<int:user_id>', methods=['GET', 'PUT'])
def user_details(user_id):
    user = Auth.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if request.method == 'GET':
        # Return user details
        user_info = {
            'userID': user.userID,
            'username': user.username,
            'email': user.email,
            'telegramtag': user.telegramtag
        }
        return jsonify(user_info), 200

    elif request.method == 'PUT':
        # Update user details
        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.telegramtag = data.get('telegramtag', user.telegramtag)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

# New /user/<int:user_id>/change_password route
@app.route('/user/<int:user_id>/change_password', methods=['PUT'])
def change_user_password(user_id):
    user = Auth.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    old_password = data.get('password')
    new_password = data.get('newPwd')
    confirm_password = data.get('confirmPwd')

    if not user.check_password(old_password):
        return jsonify({'message': 'Current password is incorrect'}), 401
    
    if new_password != confirm_password:
        return jsonify({'message': 'New passwords do not match'}), 400

    if old_password == new_password:
        return jsonify({'message': "New password can't be the same as the old password"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': 'Password updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)


# JSON File received from SignInSignUp:
# SignUp:
# {
#     "username": "username",
#     "email": "email",
#     "password": "password",
#     "telegramtag": "telegramtag"
#}

#SignIn / Login:
# {
#   "username": "username",
#   "password": "password",
#}

# JSON File received from ProfileView:
