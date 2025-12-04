from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

FILENAME = "notes.txt"
FILE_PATH = os.path.join(os.getcwd(), FILENAME)

# Simple HTML form for manual input
HTML_FORM = """
<!doctype html>
<html>
<head><title>Input Logger</title></head>
<body>
    <h2>Enter text to save in notes.txt</h2>
    <form method="POST" action="/">
        <input type="text" name="user_text" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_text = request.form.get("user_text", "").strip()
        if user_text:
            # Append the raw input directly to the file
            with open(FILE_PATH, "a", encoding="utf-8") as f:
                f.write(user_text + "\n")
            return f"Input saved successfully!<br><a href='/'>Go back</a>"
        else:
            return "No input provided.<br><a href='/'>Go back</a>"
    return render_template_string(HTML_FORM)

# REST API endpoint
@app.route("/api/save", methods=["POST"])
def api_save():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400
    
    user_text = data["text"].strip()
    if not user_text:
        return jsonify({"error": "Text cannot be empty"}), 400

    # Append the raw input directly to the file
    with open(FILE_PATH, "a", encoding="utf-8") as f:
        f.write(user_text + "\n")

    return jsonify({"message": "Input saved successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
