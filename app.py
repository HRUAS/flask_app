from flask import Flask, render_template, request, session, jsonify
from matplotlib.colors import CSS4_COLORS

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed to use session

@app.route('/', methods=['GET', 'POST'])
def home():
    # Set default color to red if not already set in session
    if "color" not in session:
        session["color"] = "red"

    if request.method == 'POST':
        input_color = request.form.get('color', '').strip()
        if is_valid_color(input_color):
            session["color"] = input_color  # Update session with new color
        else:
            return jsonify({"error": "Invalid color name"}), 400

    # Pass the current color from session to the template
    return render_template('index.html', color=session["color"])

def is_valid_color(color_name):
    """Check if a given color name is valid."""
    return color_name.lower() in CSS4_COLORS

if __name__ == '__main__':
    app.run(debug=True)
