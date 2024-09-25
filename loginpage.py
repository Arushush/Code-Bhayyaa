# app.py
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, initialize_app, auth
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase.json")
initialize_app(cred)

# @app.route('/')
# def home():
#     return render_template('login(html).html')

# @app.route('/signup')
# def signup_page():
#     return render_template('signup(html).html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    try:
        user = auth.get_user_by_email(email)
        # Add your own password verification logic here
        return jsonify({"status" : True ,"message": "User logged in successfully", "uid": user.uid}), 200
    except auth.UserNotFoundError as e:
        return jsonify({"status" : False , "error": str(e)})
    except Exception as e:
        return jsonify({"status" : False, "error": str(e)}), 400

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data['email']
    password = data['password']
    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({"message": "User created successfully", "uid": user.uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
