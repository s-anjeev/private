from flask import Blueprint, jsonify, request, make_response
from utils.limiter import limiter  # Import the limiter from extensions.py
from models.terminal import Terminal
from utils.auth import token_required

# Create the login Blueprint
terminal_bp = Blueprint('terminal', __name__)

terminal = Terminal()

# Define the Flask route to start the command execution
@terminal_bp.route('/api/terminal', methods=['POST'])
@token_required
def run_command(user_id):
    data = request.get_json()
    command = data.get('command')
    if not command:
        
        return make_response(jsonify({"error": "No command provided"}), 400)

    return terminal.execute_commands(command)

# Define another endpoint to fetch the output in chunks
@terminal_bp.route('/api/terminal/output', methods=['GET'])
@token_required
def get_command_output(user_id):
    output = terminal.get_partial_output()
    return make_response(jsonify({"output": output}), 200)