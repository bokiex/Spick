from werkzeug.security import generate_password_hash, check_password_hash

# Example user database (in a real application, use a database system like SQLite, MySQL, etc.)
users_db = {}

def signup(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate input
    if not username or not password or not email:
        return {'message': 'Missing data'}, 400

    # Check if user already exists
    if username in users_db:
        return {'message': 'User already exists'}, 409

    # Create a new user
    hashed_password = generate_password_hash(password, method='sha256')
    users_db[username] = {'password': hashed_password, 'email': email}

    return {'message': 'User created successfully'}, 201

def login(data):
    username = data.get('username')
    password = data.get('password')

    # Validate input
    if not username or not password:
        return {'message': 'Missing username or password'}, 400

    # Check if user exists
    user = users_db.get(username)
    if not user or not check_password_hash(user['password'], password):
        return {'message': 'Invalid credentials'}, 401

    return {'message': 'Logged in successfully'}, 200
