# RideShareApp

A comprehensive ride-sharing application with microservices architecture and a web-based user interface.

## Architecture

This application consists of four main components:

1. **User Service** (Port 8000): Handles user registration, authentication, and profile management
2. **Ride Service** (Port 8001): Manages ride requests, ride lifecycle, and driver assignments
3. **AI Service** (Port 8002): Provides natural language processing for parsing ride requests
4. **Web Application** (Port 3000): Frontend interface for visual interaction with all services

## Features

### Backend Services
- RESTful API design
- User authentication and authorization
- Ride request management
- Driver-rider matching
- AI-powered natural language ride request parsing

### Web Application
- Real-time service status monitoring
- API call flow visualization
- User registration and login
- Rider interface for requesting rides
- Driver interface for accepting rides
- Detailed API response logging

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nikki021/RideShareApp.git
   cd RideShareApp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

You need to run all four services. Open four separate terminal windows:

**Terminal 1 - User Service:**
```bash
cd api/user-service
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Ride Service:**
```bash
cd api/ride-service
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 3 - AI Service:**
```bash
cd api/ai-service
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 4 - Web Application:**
```bash
cd website
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

### Accessing the Application

- **Web Interface**: http://localhost:3000
- **User Service API Docs**: http://localhost:8000/docs
- **Ride Service API Docs**: http://localhost:8001/docs
- **AI Service API Docs**: http://localhost:8002/docs

## Usage

### For Riders:
1. Register with role "Rider"
2. Login to your account
3. Request rides using AI (natural language) or manual form
4. View and manage your ride requests

### For Drivers:
1. Register with role "Driver"
2. Login to your account
3. View available ride requests
4. Accept and manage rides

## Project Structure

```
RideShareApp/
├── api/
│   ├── user-service/       # User management service
│   │   ├── controllers/    # API endpoints
│   │   ├── models/         # Data models
│   │   ├── service/        # Business logic
│   │   ├── security/       # Authentication
│   │   └── main.py         # Service entry point
│   ├── ride-service/       # Ride management service
│   │   ├── controllers/    # API endpoints
│   │   ├── models/         # Data models
│   │   ├── service/        # Business logic
│   │   └── main.py         # Service entry point
│   └── ai-service/         # AI processing service
│       ├── controllers/    # API endpoints
│       ├── models/         # Data models
│       ├── service/        # Business logic
│       └── main.py         # Service entry point
├── website/                # Web frontend
│   ├── static/
│   │   ├── css/           # Stylesheets
│   │   └── js/            # Client-side JavaScript
│   ├── templates/         # HTML templates
│   ├── main.py            # Web server
│   └── README.md          # Website documentation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Endpoints

### User Service (8000)
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user
- `POST /users/logout/{user_id}` - Logout user
- `GET /users/verify/{user_id}` - Verify user

### Ride Service (8001)
- `POST /ride-requests/create` - Create ride request
- `POST /ride-requests/cancel_request/{ride_request_id}` - Cancel ride request
- `POST /ride-requests/accept_ride/{ride_request_id}` - Accept ride (driver)
- `POST /ride-requests/cancel_ride/{ride_request_id}` - Cancel accepted ride

### AI Service (8002)
- `POST /ai/parse_ride_request` - Parse natural language ride request

## Technologies Used

- **Backend**: FastAPI, Python, Pydantic
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI**: OpenAI API
- **Security**: Passlib with bcrypt
- **Data Storage**: In-memory (SQLite support available)

## Development

### Adding New Features
1. Identify which service needs modification
2. Update models if necessary
3. Add/modify controller endpoints
4. Update service layer logic
5. Update web frontend if UI changes needed

### Testing
Each service can be tested independently using the FastAPI Swagger UI at `/docs` endpoint.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.