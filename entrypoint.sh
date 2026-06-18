#!/bin/bash
set -e

if [ "$1" = "web" ]; then
    echo "Running database migrations..."

    until alembic upgrade head; do
        echo "Database not ready yet, retrying in 5 seconds..."
        sleep 5
    done

    echo "Starting FastAPI Application..."
    exec uvicorn src:app --host 0.0.0.0 --port 8000

elif [ "$1" = "worker" ]; then
    echo "Starting Celery Worker..."
    exec celery -A src.celery worker --concurrency=1 --loglevel=info

else
    exec "$@"
fi
