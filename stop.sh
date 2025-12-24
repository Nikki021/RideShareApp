#!/bin/bash

# RideShare Application Stop Script
# This script stops all running services

echo "🛑 Stopping RideShare Application..."
echo "====================================="

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/.pids"

if [ -f "$PID_FILE" ]; then
    PIDS=$(cat "$PID_FILE")
    echo "Found PIDs: $PIDS"
    
    for PID in $PIDS; do
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping process $PID..."
            kill $PID
        else
            echo "Process $PID not running"
        fi
    done
    
    # Remove PID file
    rm "$PID_FILE"
    echo "✅ All services stopped"
else
    echo "⚠️  No PID file found. Attempting to stop services by port..."
    
    # Try to kill processes by port
    for PORT in 8000 8001 8002 3000; do
        PID=$(lsof -ti:$PORT)
        if [ ! -z "$PID" ]; then
            echo "Stopping service on port $PORT (PID: $PID)..."
            kill $PID
        fi
    done
    
    echo "✅ Done"
fi

echo "====================================="
