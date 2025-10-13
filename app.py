from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
import time
from cache_utils import SimpleCache

app = Flask(__name__)
engine = create_engine("sqlite:///earthquakes.db")
cache = SimpleCache()

@app.route("/")
def index():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM earthquakes LIMIT 100"))
        earthquakes = [dict(row._mapping) for row in result]
    return render_template("index.html", earthquakes=earthquakes)

# ----------- Query (Part 10a) -----------
@app.route("/query_range", methods=["GET"])
def query_range():
    start = float(request.args.get("start"))
    end = float(request.args.get("end"))
    key = f"range:{start}-{end}"

    cached = cache.get(key)
    if cached:
        return jsonify({"source": "cache", **cached, **cache.stats()})

    start_time = time.time()
    with engine.connect() as conn:
        query = text("SELECT id, net, time, latitude, longitude FROM earthquakes WHERE time BETWEEN :start AND :end")
        result = conn.execute(query, {"start": start, "end": end})
        rows = [dict(row._mapping) for row in result]
    duration = round(time.time() - start_time, 4)

    data = {"rows": rows, "time": duration}
    cache.set(key, data)
    return jsonify({"source": "db", **data, **cache.stats()})

# ----------- Query (Part 10b) -----------
@app.route("/query_value", methods=["GET"])
def query_value():
    time_val = float(request.args.get("time"))
    net = request.args.get("net")
    count = int(request.args.get("count"))

    key = f"value:{time_val}-{net}-{count}"
    cached = cache.get(key)
    if cached:
        return jsonify({"source": "cache", **cached, **cache.stats()})

    start_time = time.time()
    with engine.connect() as conn:
        query = text("SELECT id, net, time, latitude, longitude FROM earthquakes WHERE net = :net AND time >= :time ORDER BY time LIMIT :count")
        result = conn.execute(query, {"net": net, "time": time_val, "count": count})
        rows = [dict(row._mapping) for row in result]
    duration = round(time.time() - start_time, 4)

    data = {"rows": rows, "time": duration}
    cache.set(key, data)
    return jsonify({"source": "db", **data, **cache.stats()})

# ----------- Update Record (Part 12) -----------
@app.route("/update_record", methods=["POST"])
def update_record():
    record_id = request.json.get("id")
    updates = request.json.get("updates", {})

    set_clause = ", ".join([f"{k} = :{k}" for k in updates])
    updates["id"] = record_id

    with engine.connect() as conn:
        conn.execute(text(f"UPDATE earthquakes SET {set_clause} WHERE id = :id"), updates)
        conn.commit()
    return jsonify({"status": "success", "updated_fields": updates})

if __name__ == "__main__":
    app.run(debug=True)
