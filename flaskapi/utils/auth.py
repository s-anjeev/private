from flask import make_response, request, jsonify, abort
from functools import wraps
import jwt
import re

# Hardcoded secret key (replace with environment variable in production)
jwt_secret = "asfv6s4g65fgbfxvsk6dfg5b4f2g1b6f5g4bf591bfg5b4f2g1b6f5g4bf591b"

def decode_token(token):
    """
    Decodes the JWT token using the secret and returns the decoded payload.
    """
    try:
        # Decode the token with the provided secret and HS256 algorithm
        return jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # Token has expired
        abort(401, description="Token expired")
    except jwt.InvalidTokenError:
        # Token is invalid
        abort(401, description="Invalid token")

def extract_token(auth_header):
    """
    Extracts the token from the Authorization header and validates the format.
    """
    if auth_header:
        # Check if Authorization header matches 'Bearer <token>' format
        match = re.match(r"^Bearer\s+(\S+)$", auth_header)
        if match:
            # Return the token part of the header
            return match.group(1)
    # If the header is invalid or missing
    abort(401, description="Invalid or missing Authorization header")

def token_required(f):
    """
    A decorator to enforce token-based authentication on Flask endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get Authorization header from request
        auth_header = request.headers.get("Authorization")
        
        # Extract and validate the token from the header
        token = extract_token(auth_header)
        
        # Decode the JWT token
        decoded_token = decode_token(token)
        
        # Add email from token payload to the view function arguments
        kwargs['user_id'] = decoded_token.get("user_id")
        
        # Call the wrapped function with the provided arguments
        return f(*args, **kwargs)
    
    return decorated_function
