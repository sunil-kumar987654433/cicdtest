#!/bin/bash
set -e

# Agar command "web" hai to FastAPI start karein
if [ "$1" = "web" ]; then
    echo "Starting FastAPI Application..."
    exec uvicorn src:app --host 0.0.0.0 --port 8000

# Agar command "worker" hai to Celery Worker start karein
elif [ "$1" = "worker" ]; then
    echo "Starting Celery Worker..."
    exec celery -A src.celery worker --concurrency=1 --loglevel=info

# Agar command "beat" hai to Celery Beat start karein
# elif [ "$1" = "beat" ]; then
#     echo "Starting Celery Beat..."
#     exec celery -A src.celery beat --loglevel=info

# Agar koi matched command nahi mili to pass-through run karein
else
    exec "$@"
fi
