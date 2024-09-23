from flask import jsonify,make_response
from datetime import datetime,timedelta
from config.config import jwt_secret,hash_secret
import mysql.connector
import hashlib
import jwt
# import database connection
from utils.db import db_conn
# import input validation code
from utils import input_validation
import logging
from datetime import datetime


# Create a separate logger for the login system
login_logger = logging.getLogger("logs/login_system")
login_logger.setLevel(logging.INFO)

# Create a file handler for the login logs
file_handler = logging.FileHandler("logs/login_system.log")
file_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the login logger
login_logger.addHandler(file_handler)


class UserLogin:
    def __init__(self) -> None:
        # Instantiate the db_conn class
        db_connection = db_conn()

        # Access the connection and cursor
        self.conn = db_connection.conn
        self.cur = db_connection.cur
    
    def user_login(self, data):
        try:
            __email = data["email"]
            __password = data["password"]

            login_logger.info(f"Login attempt for user: {__email}")

            # validating email
            is_valid = input_validation.email_validation(__email)
            if is_valid == False:
                login_logger.info(f"Failed login attempt for user: {__email}")
                return jsonify({"error":"Login failed.","message": "Please check your email and password."}), 400

            __password_hash = self._password_hash(__password)
            
            query = "SELECT * FROM users WHERE email = %s and password_hash = %s LIMIT 1"
            params = (__email, __password_hash)
            try:
                self.cur.execute(query,params)
                result = self.cur.fetchall()
                if result:

                    # calculating expire time
                    exp_time = datetime.now() + timedelta(minutes=60)
                    exp_epoch_time = int(exp_time.timestamp())

                    user = {
                        "user_id" : result[0]["user_id"],
                        "username" : result[0]["username"],
                        "role" : result[0]["role"],
                        "exp": exp_epoch_time  # Using 'exp' for the expiration time claim
                    }

                    # create a jwt token
                    secret = jwt_secret["secret"]
                    TOKEN = jwt.encode(user, secret, algorithm="HS256")
                    # return token to user
                    response = {
                        "message":"Login successful.",
                        "token":TOKEN
                    }
                    self.conn.close()
                    login_logger.info(f"Login successful for user: {__email}")
                    return make_response(response), 200
                else:
                    self.conn.close()
                    login_logger.info(f"Failed login attempt for user: {__email}")
                    return jsonify({"error":"Login failed.","message": "Please check your email and password."}), 400
                        
            except mysql.connector.Error as err:
                self.conn.close()
                print(f"Error: {err}")
                return jsonify({"error": "An error occurred while logging in.","message": "Please try again later."}), 500
        
        except Exception as e:
            print(f"Exception: {e}")
            login_logger.info(f"Failed login attempt for user: {__email}")
            return jsonify({"error": "An error occurred while logging in.","message": "Please try again later."}), 500
        
    def _password_hash(self, password):
        # Generate a salt
        salt = hash_secret["salt"].encode('utf-8')
        
        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        salted_password = salt + password_bytes
        
        # Hash using SHA-256 (or another suitable hash function)
        hash_func = hashlib.sha256()
        hash_func.update(salted_password)
        hashed_password = hash_func.hexdigest()
        
        # Return hashed password
        return hashed_password