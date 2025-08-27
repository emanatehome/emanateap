from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return {"message": "Hello from Emanate API!"}

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    if data.get("username") == "admin" and data.get("password") == "password":
        return {"token": "demo_token_123"}
    return {"error": "Invalid credentials"}, 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    return {"message": "This is login endpoint"}
