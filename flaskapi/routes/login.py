from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
from models.login import UserLogin
from utils.limiter import limiter  # Import the limiter from extensions.py

# Create the login Blueprint
login_bp = Blueprint('login', __name__)

# Apply rate limiting to specific Blueprint routes
@login_bp.route('/api/login', methods=["POST"])
@limiter.limit("2 per day")
def login():
    try:
        # Attempt to get and validate JSON data
        data = request.get_json()

        if data is None:
            raise ValueError("Request body must be valid JSON.")

        if not data:
            # Check if the JSON object is empty (e.g., {})
            raise ValueError("Empty JSON data is provided.")

        login_obj = UserLogin()
        return login_obj.user_login(data)
        
    except BadRequest:
        # Handle the case where the POST data is not valid JSON
        return jsonify({"error": "Invalid request data", "message": "Request body must be valid JSON."}), 400

    except ValueError as ve:
        # Handle cases where JSON is empty or missing
        return jsonify({"error": "Invalid JSON data", "message": str(ve)}), 400

    except Exception as e:
        # Catch any other unforeseen exceptions
        return jsonify({"error": "Server Error", "message": "An unexpected error occurred."}), 500
