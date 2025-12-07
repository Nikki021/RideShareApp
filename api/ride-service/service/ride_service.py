from fastapi import HTTPException
import requests
import uuid
from datetime import datetime, timezone
from ..models.ride_model import RideRequest, RideRequestCreate, RideStatus

USER_SERVICE_URL = "http://localhost:8000"  # Example URL for the user service

class RideService:
    def __init__(self):
        self.ride_requests = {}

    def _validate_user(self, user_id: str):
        # Simulate a call to the user service to validate user existence
        response = requests.get(f"{USER_SERVICE_URL}/users/verify/{user_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="User service is unavailable")
        data = response.json()
        if not data.get("exists"):
            raise HTTPException(status_code=404, detail="User not found")
        elif not data.get("is_logged_in"):
            raise HTTPException(status_code=401, detail="User is not logged in")
        elif data.get("role") != "rider":
            raise HTTPException(status_code=403, detail="Please login as a rider to request a ride")
        

    def create_ride_request(self, create_ride_request: RideRequestCreate) -> RideRequest:
        # Placeholder logic for creating a ride
        self._validate_user(create_ride_request.user_id)
        ride_request = RideRequest(
            id=str(uuid.uuid4()),
            user_id=create_ride_request.user_id,
            pickup_location=create_ride_request.pickup_location,
            dropoff_location=create_ride_request.dropoff_location,
            requested_at=datetime.now(timezone.utc),
            status=RideStatus.REQUESTED
        )
        self.ride_requests[ride_request.id] = ride_request
        return ride_request