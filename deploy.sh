#!/bin/bash
# Activate virtual environment
source ~/Desktop/earthquake_performance/venv/bin/activate

# Start Gunicorn in background with 4 workers on port 8000
gunicorn app:app --bind 0.0.0.0:8000 --workers 4 --daemon

echo "App deployed on http://0.0.0.0:8000"
