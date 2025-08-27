from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change this in production

# ✅ Token never expires (lifetime)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

jwt = JWTManager(app)

# In-memory "database" (replace with real DB later)
users_db = {}

@app.route("/")
def home():
    return {"message": "Hello from Emanate API!"}

# Register new user
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "Username and password required"}, 400

    if username in users_db:
        return {"error": "User already exists"}, 400

    # Save with hashed password
    users_db[username] = generate_password_hash(password)
    return {"message": f"User {username} registered successfully!"}, 201

# Login existing user
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username not in users_db or not check_password_hash(users_db[username], password):
        return {"error": "Invalid username or password"}, 401

    # Create token
    token = create_access_token(identity=username)
    return {"token": token}

# Example protected route
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {"message": f"Hello, {current_user}. This is a protected route."}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
