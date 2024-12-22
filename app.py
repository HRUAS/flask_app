from flask import Flask, render_template, request, session, jsonify
from matplotlib.colors import CSS4_COLORS
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Fetch configuration from environment variables
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()
DEFAULT_COLOR = os.getenv('DEFAULT_COLOR', 'red')

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to use session

# Create 'logs' directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging to file with daily rotation, store logs in 'logs' folder
log_handler = TimedRotatingFileHandler('logs/app.log', when='midnight', interval=1, backupCount=7)
log_handler.setLevel(getattr(logging, LOG_LEVEL, logging.DEBUG))  # Use LOG_LEVEL from ConfigMap
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

# Add the handler to the root logger
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(log_handler.level)  # Set root logger level

logger.debug(f"DEFAULT_COLOR: {DEFAULT_COLOR}")
logger.debug(f"LOG_LEVEL: {LOG_LEVEL}")

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        # Log the incoming request
        logger.info("Handling request: %s %s", request.method, request.url)

        # Set default color if not already set in session
        if "color" not in session:
            logger.info("Session color not set. Using DEFAULT_COLOR from ConfigMap: %s", DEFAULT_COLOR)
            session["color"] = DEFAULT_COLOR

        if request.method == 'POST':
            input_color = request.form.get('color', '').strip()
            logger.info("Received color input: %s", input_color)

            if is_valid_color(input_color):
                session["color"] = input_color  # Update session with new color
                logger.info("Valid color entered. Session color updated to: %s", input_color)
            else:
                logger.error("Invalid color name entered: %s", input_color)
                return jsonify({"error": "Invalid color name"}), 400

        # Pass the current color from session to the template
        logger.info("Rendering template with current color: %s", session["color"])
        return render_template('index.html', color=session["color"])
    
    except Exception as e:
        # Log the exception with stack trace
        logger.exception(f"An error occurred while processing the request: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred"}), 500

def is_valid_color(color_name):
    try:
        """Check if a given color name is valid."""
        if color_name.lower() in CSS4_COLORS:
            return True
        else:
            return False
    except Exception as e:
        # Log any errors in the color validation function
        logger.exception(f"Error in is_valid_color function: {e}", exc_info=True)
        return False

if __name__ == '__main__':
    try:
        debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
        app.run(debug=debug_mode)
    except Exception as e:
        # Log any errors when starting the Flask app
        logger.critical("Failed to start Flask app", exc_info=True)
