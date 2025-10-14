import os
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Optional: path for uploaded or static data
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- ROUTES ----------

@app.route("/")
def index():
    """Default homepage route."""
    return "<h1>✅ Flask App Deployed Successfully on Render</h1><p>Use /process or /upload for API calls.</p>"


@app.route("/health")
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok", "environment": os.getenv("RENDER", "local")})


@app.route("/process", methods=["POST"])
def process_data():
    """
    Example POST endpoint:
    Accepts JSON with numeric data and returns the sum and mean.
    """
    try:
        data = request.get_json(force=True)
        values = data.get("values", [])

        if not isinstance(values, list) or not all(isinstance(v, (int, float)) for v in values):
            return jsonify({"error": "Invalid input. Expected JSON: {'values': [numbers]}"}), 400

        df = pd.DataFrame(values, columns=["numbers"])
        result = {
            "count": int(df["numbers"].count()),
            "sum": float(df["numbers"].sum()),
            "mean": float(df["numbers"].mean()),
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Example file upload endpoint:
    Accepts a CSV file and returns summary stats.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        summary = df.describe(include="all").to_dict()

        return jsonify({
            "message": f"File '{file.filename}' uploaded successfully.",
            "summary": summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- MAIN ENTRY POINT ----------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
