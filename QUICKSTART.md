# Quick Start Guide

## Starting the RideShare Application

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start All Services**
   ```bash
   ./start.sh
   ```
   
   This will start:
   - User Service on port 8000
   - Ride Service on port 8001
   - AI Service on port 8002
   - Web Application on port 3000

3. **Access the Application**
   
   Open your browser and go to: **http://localhost:3000**

### Using the Application

#### As a Rider:

1. **Register**
   - Click "Register" tab
   - Fill in username, email, password
   - Select "Rider" as role
   - Click "Register" button

2. **Login**
   - Enter your email and password
   - Click "Login" button

3. **Request a Ride**
   
   **Option A: AI-Powered Request**
   - Type naturally: "I need to go from Times Square to Central Park"
   - Click "Parse with AI"
   - The AI will extract locations and create the ride request
   
   **Option B: Manual Request**
   - Enter pickup location
   - Enter dropoff location
   - Click "Request Ride"

4. **View Your Requests**
   - Your active ride requests appear in "Your Active Requests" section

#### As a Driver:

1. **Register** with role "Driver"
2. **Login**
3. **View Available Rides**
   - See all pending ride requests
   - Click "Refresh Requests" to update the list
4. **Accept Rides**
   - Click "Accept" on any available ride
   - Manage your accepted rides

### Monitoring Services

The **Service Status Dashboard** shows:
- 🟢 Green dot = Service is running
- 🔴 Red dot = Service is offline
- Status updates every 30 seconds

### API Call Flow Visualization

Watch the **API Call Flow Visualization** panel to see:
- Which services are being called
- What data is being sent
- Real-time flow of requests through the system
- Color-coded: Green for success, Red for errors

### API Response Log

The **API Response Log** at the bottom shows:
- Complete HTTP request details
- Request body/parameters
- Response data
- Timestamps
- Status codes (200 = success)

## Stopping the Application

```bash
./stop.sh
```

Or press `Ctrl+C` in the terminal where you ran `start.sh`

## Troubleshooting

### Services show as "Offline"
- Check that all services started successfully
- Look for error messages in the terminal
- Make sure ports 8000, 8001, 8002, 3000 are not in use

### Can't login
- Make sure you've registered first
- Check that User Service (port 8000) is running
- Verify your email and password are correct

### AI parsing doesn't work
- The AI service has a fallback parser
- Use format: "from [location] to [location]" or "[location] to [location]"
- Example: "Times Square to Central Park"

### Port already in use
- Stop any existing services on those ports
- Run `./stop.sh` to clean up
- Or kill processes manually: `lsof -ti:8000 | xargs kill`

## API Documentation

Each service has interactive API documentation:
- User Service: http://localhost:8000/docs
- Ride Service: http://localhost:8001/docs
- AI Service: http://localhost:8002/docs

## Getting Help

- Check the main README.md for detailed information
- Check website/README.md for web-specific details
- Review the API documentation at `/docs` endpoints
- Look at the API Response Log for debugging information

## Example Usage Flow

1. Start services: `./start.sh`
2. Open browser: http://localhost:3000
3. Register as "Rider"
4. Login
5. Type: "I need to go from Brooklyn to Manhattan"
6. Click "Parse with AI"
7. Watch the magic happen:
   - AI Service parses your request
   - Ride Service creates the ride request
   - Everything is logged in real-time
8. See your ride request appear!

Enjoy using RideShare! 🚗
