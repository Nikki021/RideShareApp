# RideShare Website

This is the web frontend for the RideShare application that provides a visual interface to interact with all backend services.

## Features

- **Service Status Dashboard**: Real-time monitoring of all three backend services (User, Ride, AI)
- **API Call Flow Visualization**: Visual representation of API calls and their flow through services
- **User Authentication**: Register and login functionality
- **Rider Interface**: 
  - AI-powered natural language ride requests
  - Manual ride request creation
  - View active ride requests
  - Cancel ride requests
- **Driver Interface**:
  - View available ride requests
  - Accept ride requests
  - Manage accepted rides
- **API Response Log**: Detailed logging of all API calls with request/response data

## Architecture

The website acts as a client that communicates with three backend services:

1. **User Service** (Port 8000): Handles user registration, login, and authentication
2. **Ride Service** (Port 8001): Manages ride requests and ride lifecycle
3. **AI Service** (Port 8002): Provides natural language processing for ride requests

## Setup and Running

### Prerequisites

- Python 3.8+
- All backend services running (User, Ride, AI services)

### Installation

1. Ensure you have installed the required dependencies from the root requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. Navigate to the website directory:
   ```bash
   cd website
   ```

3. Start the web server:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 3000 --reload
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Running All Services

To run the complete application, you need to start all four services:

### Terminal 1: User Service
```bash
cd api/user-service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Ride Service
```bash
cd api/ride-service
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 3: AI Service
```bash
cd api/ai-service
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Terminal 4: Web Application
```bash
cd website
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## Usage Guide

### For Riders:

1. **Register**: Create a new account with role "Rider"
2. **Login**: Sign in with your credentials
3. **Request a Ride**: 
   - Use AI-powered request: Type naturally (e.g., "I need to go from Times Square to Central Park")
   - Or use manual form: Enter pickup and dropoff locations directly
4. **View Requests**: See your active ride requests
5. **Cancel Requests**: Cancel any pending requests

### For Drivers:

1. **Register**: Create a new account with role "Driver"
2. **Login**: Sign in with your credentials
3. **View Available Rides**: See all pending ride requests
4. **Accept Rides**: Accept rides to become the assigned driver
5. **Manage Rides**: View and manage your accepted rides

## API Flow Example

When a user requests a ride using AI:

1. **Frontend** → **AI Service**: Parse natural language request
2. **AI Service** → **Frontend**: Return structured location data
3. **Frontend** → **Ride Service**: Create ride request with parsed locations
4. **Ride Service** → **Frontend**: Return ride request confirmation

All these interactions are visualized in real-time in the "API Call Flow Visualization" panel.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: FastAPI (Python)
- **Styling**: Custom CSS with gradient backgrounds and animations
- **Communication**: REST APIs with JSON

## File Structure

```
website/
├── main.py                 # FastAPI server
├── static/
│   ├── css/
│   │   └── style.css      # All styling
│   └── js/
│       └── app.js         # Client-side logic
└── templates/
    └── index.html         # Main HTML page
```

## Configuration

Service endpoints are configured in `static/js/app.js`:

```javascript
const API_CONFIG = {
    USER_SERVICE: 'http://localhost:8000',
    RIDE_SERVICE: 'http://localhost:8001',
    AI_SERVICE: 'http://localhost:8002'
};
```

Modify these if your services run on different ports.

## Troubleshooting

### Services show as "Offline"
- Ensure all backend services are running on their respective ports
- Check that there are no CORS issues (the web app enables CORS by default)

### API calls fail
- Verify backend services are accessible
- Check browser console for detailed error messages
- Review the API Response Log panel for debugging information

### Login doesn't work
- Ensure the User Service is running on port 8000
- Check that you've registered first before trying to login

## Development

To modify the frontend:

1. **HTML**: Edit `templates/index.html`
2. **Styling**: Edit `static/css/style.css`
3. **Logic**: Edit `static/js/app.js`

Changes to static files are served immediately (no restart needed with --reload flag).

## Future Enhancements

- WebSocket support for real-time ride updates
- Map integration for visual location display
- Driver location tracking
- Ride history and receipts
- Rating and review system
- Payment integration
