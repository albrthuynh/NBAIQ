from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from supabase import create_client, Client # type: ignore
from dotenv import load_dotenv # type: ignore
import os

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

if __name__ == "__main__":
    app.run(debug=True, port=5000) 