from flask import Flask, render_template, request, session, jsonify
from matplotlib.colors import CSS4_COLORS
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import mysql.connector
from datetime import datetime

# Fetch configuration from environment variables
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()
DEFAULT_COLOR = os.getenv('DEFAULT_COLOR', 'red')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'flaskdb')

print(f"LOG_LEVEL: {LOG_LEVEL}")
print(f"DEFAULT_COLOR: {DEFAULT_COLOR}")

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to use session

# Create 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file with daily rotation
log_handler = TimedRotatingFileHandler('logs/app.log', when='midnight', interval=1, backupCount=7)
log_handler.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

# Add the handler to the root logger
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(log_handler.level)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Ensure the database table exists
def initialize_database():
    try:
        print("Table creation started")
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                entry_time DATETIME NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()
        logger.info("Database initialized successfully")
    except mysql.connector.Error as e:
        logger.critical(f"Database initialization failed: {e}", exc_info=True)
        print(f"Database initialization failed: {e}", exc_info=True)
        raise

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Log the incoming request
        logger.info("Handling request: %s %s", request.method, request.url)

        # Set default color if not already set in session
        if "color" not in session:
            logger.info("Session color not set. Using DEFAULT_COLOR: %s", DEFAULT_COLOR)
            session["color"] = DEFAULT_COLOR

        if request.method == 'POST':
            input_name = request.form.get('name', '').strip()
            input_color = request.form.get('color', '').strip()

            # Validate and store color in session
            if input_color and is_valid_color(input_color):
                session["color"] = input_color
                logger.info("Valid color entered. Session color updated to: %s", input_color)
            else:
                logger.warning("Invalid color entered: %s", input_color)

            # Store name in the database
            if input_name:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO user_entries (name, entry_time) VALUES (%s, %s)",
                    (input_name, datetime.now())
                )
                connection.commit()
                cursor.close()
                connection.close()
                logger.info("Stored name in database: %s", input_name)
            else:
                logger.warning("No name entered to store in the database")

        # Render the template with the current color
        logger.info("Rendering template with current color: %s", session["color"])
        return render_template('index.html', color=session["color"])

    except Exception as e:
        logger.exception(f"An error occurred while processing the request: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

def is_valid_color(color_name):
    try:
        """Check if a given color name is valid."""
        return color_name.lower() in CSS4_COLORS
    except Exception as e:
        logger.exception(f"Error in is_valid_color function: {e}")
        return False

if __name__ == '__main__':
    try:
        print("inside main, starting db initialisation")
        initialize_database()  # Ensure database and table exist
        debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
        app.run(host='0.0.0.0', port=5000, debug=debug_mode)
    except Exception as e:
        logger.critical("Failed to start Flask app", exc_info=True)
