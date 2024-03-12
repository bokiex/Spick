from flask import Flask, render_template, request, jsonify
import authentication

app = Flask(__name__)

@app.route('/members')
def members():
    return  {"members": ["member1", "member2", "member3"]}

@app.route('/')
def index():
    # Serve the login page as the index
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return authentication.signup(data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authentication.login(data)

if __name__ == '__main__':
    app.run(debug=True)