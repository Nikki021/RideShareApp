#!/bin/bash

# RideShare Application Startup Script
# This script starts all four services in separate terminals

echo "🚗 Starting RideShare Application..."
echo "========================================"
echo ""

# Function to check if a port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $1 is already in use. Please stop the service using that port."
        return 1
    fi
    return 0
}

# Check if all required ports are available
echo "Checking ports..."
check_port 8000 || exit 1
check_port 8001 || exit 1
check_port 8002 || exit 1
check_port 3000 || exit 1
echo "✅ All ports are available"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting services..."
echo "-------------------"

# Start User Service
echo "🟢 Starting User Service on port 8000..."
cd "$SCRIPT_DIR/api"
python run_user_service.py &
USER_PID=$!
echo "User Service PID: $USER_PID"

# Wait a moment before starting next service
sleep 2

# Start Ride Service
echo "🟢 Starting Ride Service on port 8001..."
python run_ride_service.py &
RIDE_PID=$!
echo "Ride Service PID: $RIDE_PID"

# Wait a moment before starting next service
sleep 2

# Start AI Service
echo "🟢 Starting AI Service on port 8002..."
python run_ai_service.py &
AI_PID=$!
echo "AI Service PID: $AI_PID"

# Wait a moment before starting next service
sleep 2

# Start Web Application
echo "🟢 Starting Web Application on port 3000..."
cd "$SCRIPT_DIR/website"
python main.py &
WEB_PID=$!
echo "Web Application PID: $WEB_PID"

echo ""
echo "========================================"
echo "✅ All services started successfully!"
echo "========================================"
echo ""
echo "Access the application at:"
echo "  Web Interface: http://localhost:3000"
echo ""
echo "API Documentation:"
echo "  User Service:  http://localhost:8000/docs"
echo "  Ride Service:  http://localhost:8001/docs"
echo "  AI Service:    http://localhost:8002/docs"
echo ""
echo "Process IDs:"
echo "  User Service:  $USER_PID"
echo "  Ride Service:  $RIDE_PID"
echo "  AI Service:    $AI_PID"
echo "  Web App:       $WEB_PID"
echo ""
echo "To stop all services, run: ./stop.sh"
echo "Or press Ctrl+C and run: kill $USER_PID $RIDE_PID $AI_PID $WEB_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Save PIDs to file for stop script
echo "$USER_PID $RIDE_PID $AI_PID $WEB_PID" > "$SCRIPT_DIR/.pids"

# Wait for all background processes
wait
