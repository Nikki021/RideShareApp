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
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
        if response.status_code != 200:
            raise ValueError("User not found")

        return response.json()

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