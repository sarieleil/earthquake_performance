from flask import Flask, render_template, request, jsonify
from models import insert_earthquake_data, query_time_range, query_net_value, update_event
from cache_utils import SimpleCache
import time

app = Flask(__name__)

# Simple in-memory cache
cache = SimpleCache()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if file:
        insert_earthquake_data(file)
        return jsonify({"message": "Processing completed successfully"})
    return jsonify({"message": "No file uploaded"}), 400

@app.route('/query_range', methods=['GET'])
def query_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    
    cache_key = f"range:{start}:{end}"
    if cache_key in cache:
        results = cache.get(cache_key)
        cache_hit = True
    else:
        start_time = time.time()
        results = query_time_range(start, end)
        query_time_taken = time.time() - start_time
        cache.set(cache_key, results)
        cache_hit = False
    return jsonify({"results": results, "cache_hit": cache_hit})

@app.route('/query_net', methods=['GET'])
def query_net():
    start_time_val = int(request.args.get('time'))
    net_val = request.args.get('net')
    count = int(request.args.get('count'))

    cache_key = f"net:{start_time_val}:{net_val}:{count}"
    if cache_key in cache:
        results = cache.get(cache_key)
        cache_hit = True
    else:
        start = time.time()
        results = query_net_value(start_time_val, net_val, count)
        query_time_taken = time.time() - start
        cache.set(cache_key, results)
        cache_hit = False
    return jsonify({"results": results, "cache_hit": cache_hit})

@app.route('/update_event', methods=['POST'])
def update():
    event_id = int(request.form.get('id'))
    data = {
        "time": int(request.form.get('time')),
        "net": request.form.get('net'),
        "lat": float(request.form.get('lat')),
        "lon": float(request.form.get('lon'))
    }
    update_event(event_id, data)
    return jsonify({"message": "Event updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
