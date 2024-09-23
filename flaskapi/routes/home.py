from flask import Blueprint, jsonify
from utils.auth import token_required
# creating a blueprint for home
home_bp = Blueprint('home',__name__)

@home_bp.route('/', methods=["GET"])
@token_required
def index(user_id):
    return jsonify({"message": "Access granted", "user_id": user_id})
    # return jsonify({}), 200