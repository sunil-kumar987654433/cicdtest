#!/bin/bash
set -e

# 1. Condition for FastAPI Web execution
if [ "$1" = "web" ]; then
    echo "Starting FastAPI Application..."
    exec uvicorn src:app --host 0.0.0.0 --port 8000

# 2. Condition for Celery Background Worker (Syntax branching logic fixed)
elif [ "$1" = "worker" ]; then
    echo "Starting Celery Worker..."
    exec celery -A src.celery worker --concurrency=1 --loglevel=info

# 3. Fallback conditional capture
else
    echo "No matching command found, running pass-through execution for: $@"
    exec "$@"
fi
