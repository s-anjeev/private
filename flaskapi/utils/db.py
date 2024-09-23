import mysql.connector
from config.config import db_config
import logging
from datetime import datetime


# Create a separate logger for the login system
login_logger = logging.getLogger("logs/db_system")
login_logger.setLevel(logging.INFO)

# Create a file handler for the login logs
file_handler = logging.FileHandler("logs/db_system.log")
file_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Add the file handler to the login logger
login_logger.addHandler(file_handler)

class db_conn:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        """Establish a database connection."""
        login_logger.info(f"Trying to connect with database: {db_config['database']}")
        try:
            self.conn = mysql.connector.connect(
                host=db_config["host"],
                user=db_config["username"],
                password=db_config["password"],
                database=db_config["database"]
            )
            self.cur = self.conn.cursor(dictionary=True)
            login_logger.info(f"Successfully connect to database: {db_config['database']}")
            print("Connection established successfully")
        except mysql.connector.Error as err:
            login_logger.info(f"Database error: {err}")
            print(f"Error: {err}")
            self.conn = None
            self.cur = None

    def close(self):
        """Close the database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Connection closed")
        login_logger.info(f"Connection successfully colsed to database: {db_config['database']}")