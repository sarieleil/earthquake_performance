from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------------------
# Main page route
# ---------------------------
@app.route("/")
def index():
    # Render the HTML upload page
    return render_template("index.html")

# ---------------------------
# Upload endpoint
# ---------------------------
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    return "File uploaded successfully"

# ---------------------------
# Process endpoint
# ---------------------------
@app.route("/process")
def process():
    # Placeholder logic - replace with actual CSV processing
    return "Processing completed successfully"

# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
