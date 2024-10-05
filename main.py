from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import joblib
import numpy as np
from datetime import timedelta
app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "ed1d715c9f4d4470a2d3aa282bf40c42"# uuid
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)

# Load the Random Forest model and scaler
model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Dummy user credentials for login
users = {
    "user@example.com": "password123"
}

# Login endpoint to get JWT token
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check for missing fields
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # Validate credentials
    if users.get(username) != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    # Create access token
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

# Prediction endpoint (JWT-protected)
@app.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    data = request.json
    print(request.headers)  # Log the request headers
    print(data)  # Log the request body

    # Validate input format
    if "features" not in data or not isinstance(data["features"], list):
        return jsonify({"msg": "'features' key is missing or not a list"}), 400

    features = data["features"]

    # Check that the number of features matches the model's expectation
    if len(features) != model.n_features_in_:
        return jsonify({"msg": f"Expected {model.n_features_in_} features, got {len(features)}"}), 400

    try:
        # Convert features to numpy array and scale them
        features = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features)

        # Make prediction and calculate confidence
        prediction = model.predict(features_scaled)
        confidence = model.predict_proba(features_scaled).max()

        return jsonify({"prediction": int(prediction[0]), "confidence": confidence}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

# Health check endpoint
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "API is running"}), 200

if __name__ == "__main__":
    app.run(debug=True)
