from flask import Flask, jsonify
from flask_cors import CORS
import logging
from routes.login import login_bp
from routes.home import home_bp
from routes.dashboard import dashboard_bp
from routes.terminal import terminal_bp
from utils.limiter import limiter  # Import the limiter from extensions.py

app = Flask(__name__)
CORS(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Register blueprints
app.register_blueprint(login_bp)
app.register_blueprint(home_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(terminal_bp)

# Initialize limiter with the app
limiter.init_app(app)

# Global error handler for Method Not Allowed (405)
@app.errorhandler(405)
def handle_405_error(e):
    return jsonify({"error": "Method Not Allowed"}), 405


# Global error handler for rate limit (429)
@app.errorhandler(429)
def handle_429_error(e):
    return jsonify({"error": "Too Many Requests"}), 429

# Global error handler for all other routes
@app.errorhandler(404)
def handle_404_error(e):
    return jsonify({"error": "Not Found"}), 404

# Global error handler for internal server error
@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": "Internal server error"}), 500

# Global error handler for 401 Unauthorized
@app.errorhandler(401)
def handle_401_error(e):
    return jsonify({"error": "401 Unauthorized"}), 401


if __name__ == '__main__':
    app.run(debug=True)
