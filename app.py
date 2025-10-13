from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Load CSV
DATA_PATH = os.path.join(os.path.dirname(__file__), "data/all_month.csv")
df = pd.read_csv(DATA_PATH)

@app.route("/")
def index():
    # Pass earthquake data to template
    earthquakes = df.to_dict(orient="records")
    return render_template("index.html", earthquakes=earthquakes)

if __name__ == "__main__":
    app.run(debug=True)
