from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore
from supabase import create_client, Client  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore

from data_testing import prepare_data
from team_functions import get_team_stats, build_feature_vector

# Load environment variables
load_dotenv('.env.local')

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  # Use anon key for auth verification
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")

# Debug: Print environment variables (remove in production)
print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_ANON_KEY: {'*' * 10 if SUPABASE_ANON_KEY else None}")
print(f"SUPABASE_SERVICE_ROLE: {'*' * 10 if SUPABASE_SERVICE_ROLE else None}")

if not SUPABASE_URL or not SUPABASE_ANON_KEY or not SUPABASE_SERVICE_ROLE:
    raise ValueError("Missing required environment variables: SUPABASE_URL, SUPABASE_ANON_KEY, and SUPABASE_SERVICE_ROLE")

# Two clients: one for auth verification, one for admin operations
supabase_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5174", "http://localhost:5173"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

MODEL = None
SCALER = None
TEAM_STATS_DF = None


def initialize_prediction_resources():
    global MODEL, SCALER, TEAM_STATS_DF

    if MODEL is not None and SCALER is not None and TEAM_STATS_DF is not None:
        return

    X_train, _, y_train, _, _, _ = prepare_data()
    SCALER = StandardScaler()
    X_train_scaled = SCALER.fit_transform(X_train)

    MODEL = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42,
        bootstrap=True,
    )
    MODEL.fit(X_train_scaled, y_train.values.ravel())

    TEAM_STATS_DF = pd.read_csv("data/Team Stats Per 100 Poss.csv")


@app.route('/')
def home():
    return "Welcome to the NBA IQ App!"

@app.route('/api/users', methods=['POST'])  
def create_user():
    try:
        # Get profile fields from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_id = data.get("user_id")
        email = data.get("email")
        full_name = data.get("full_name")
        avatar_url = data.get("avatar_url")

        # Validate required fields
        if not user_id or not email or not full_name:
            return jsonify({"error": "Missing required fields: user_id, email, full_name"}), 400

        # Check if user already exists
        existing_user = supabase_admin.table("users").select("id").eq("id", user_id).execute()
        if existing_user.data:
            return jsonify({"message": "User already exists", "user": existing_user.data[0]}), 200

        # Insert into public.users using admin client
        response = supabase_admin.table("users").insert({
            "id": user_id,
            "full_name": full_name,
            "avatar_url": avatar_url,
            "email": email
        }).execute()

        if not response.data:
            return jsonify({"error": "Failed to create user"}), 400

        return jsonify({"message": "User created successfully", "user": response.data[0]}), 201
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile"""
    try:
        # Get and validate token
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        jwt_token = token.split(" ")[1]
        
        # Verify token
        user_response = supabase_client.auth.get_user(jwt_token)
        if not user_response.user:
            return jsonify({"error": "Invalid token"}), 401
        
        # Get user from database
        response = supabase_admin.table("users").select("*").eq("id", user_id).execute()
        
        if not response.data:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify(response.data[0]), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/predict', methods=['POST'])
def predict_matchup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        required_fields = ["home_team", "home_season", "away_team", "away_season"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        home_team = data["home_team"]
        away_team = data["away_team"]
        home_season = int(data["home_season"])
        away_season = int(data["away_season"])

        initialize_prediction_resources()

        home_stats = get_team_stats(TEAM_STATS_DF, home_team, home_season)
        away_stats = get_team_stats(TEAM_STATS_DF, away_team, away_season)
        features = build_feature_vector(home_stats, away_stats)
        features_scaled = SCALER.transform(features)

        prediction = int(MODEL.predict(features_scaled)[0])
        probabilities = MODEL.predict_proba(features_scaled)[0]
        home_win_probability = float(probabilities[1])
        away_win_probability = float(probabilities[0])
        predicted_winner = home_team if prediction == 1 else away_team

        return jsonify({
            "home_team": home_team,
            "home_season": home_season,
            "away_team": away_team,
            "away_season": away_season,
            "predicted_winner": predicted_winner,
            "home_win_probability": home_win_probability,
            "away_win_probability": away_win_probability,
            "model": "RandomForestClassifier",
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000) 