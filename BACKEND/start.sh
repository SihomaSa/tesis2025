#!/bin/bash
echo "=== Starting Python FastAPI ==="
uvicorn app.main:app --host 0.0.0.0 --port $PORT
