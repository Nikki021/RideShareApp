from fastapi import HTTPException
import requests
import uuid
from datetime import datetime, timezone
from ..models.ride_model import Ride, RideRequest, RideRequestCreate, RideRequestStatus, RideStatus

USER_SERVICE_URL = "http://localhost:8000"  # Example URL for the user service

class RideService:
    def __init__(self):
        self.ride_requests = {}
        self.rides = {}

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
        print("User validated successfully.")
        ride_request = RideRequest(
            id=str(uuid.uuid4()),
            user_id=create_ride_request.user_id,
            pickup_location=create_ride_request.pickup_location,
            dropoff_location=create_ride_request.dropoff_location,
            requested_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            status=RideRequestStatus.REQUESTED
        )
        self.ride_requests[ride_request.id] = ride_request
        return ride_request
    
    def cancel_ride_request(self, ride_request_id: str, user_id: str) -> RideRequest:
        ride_request = self.ride_requests.get(ride_request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        if ride_request.user_id != user_id:
            raise HTTPException(status_code=403, detail="You are not authorized to cancel this ride request")
        if ride_request.status != RideRequestStatus.REQUESTED:
            raise HTTPException(status_code=400, detail="Ride request cannot be cancelled in its current state")
        
        ride_request.status = RideRequestStatus.CANCELED
        ride_request.updated_at = datetime.now(timezone.utc)
        return ride_request
    
    def _validate_accept_request(self, driver_id: str, ride_request_id: str):
        ride_request = self.ride_requests.get(ride_request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        if ride_request.status != RideRequestStatus.REQUESTED:
            raise HTTPException(status_code=400, detail="Ride request is not in a valid state to be accepted")
        
        response = requests.get(f"{USER_SERVICE_URL}/users/verify/{driver_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="User service is unavailable")
        data = response.json()
        if not data.get("exists"):
            raise HTTPException(status_code=404, detail="Driver not found")
        elif not data.get("is_logged_in"):
            raise HTTPException(status_code=401, detail="Driver is not logged in")
        elif data.get("role") != "driver":
            raise HTTPException(status_code=403, detail="Please login as a driver to accept a ride")
    
    def accept_ride_request(self, ride_request_id: str, driver_id: str) -> Ride:
        # Placeholder logic for accepting a ride request
        self._validate_accept_request(driver_id, ride_request_id)
        ride_request = self.ride_requests[ride_request_id]
        
        ride_request.status = RideRequestStatus.ACCEPTED
        ride_request.updated_at = datetime.now(timezone.utc)
        ride = Ride(
            id=str(uuid.uuid4()),
            ride_request_id=ride_request.id,
            driver_id=driver_id,
            start_time=None,
            end_time=None,
            fare=None,
            status=RideStatus.DRIVER_ASSIGNED
        )
        self.rides[ride.id] = ride
        return ride
    
    def cancel_ride_request_by_driver(self, ride_request_id: str, driver_id: str, ride_id: str) -> RideRequest:
        ride_request = self.ride_requests.get(ride_request_id)
        if not ride_request:
            raise HTTPException(status_code=404, detail="Ride request not found")
        if ride_request.status != RideRequestStatus.ACCEPTED:
            raise HTTPException(status_code=400, detail="Ride request cannot be cancelled in its current state")
        
        response = requests.get(f"{USER_SERVICE_URL}/users/verify/{driver_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="User service is unavailable")
        data = response.json()
        if not data.get("exists"):
            raise HTTPException(status_code=404, detail="Driver not found")
        elif not data.get("is_logged_in"):
            raise HTTPException(status_code=401, detail="Driver is not logged in")
        elif data.get("role") != "driver":
            raise HTTPException(status_code=403, detail="Please login as a driver to cancel a ride")
        
        ride_request.status = RideRequestStatus.REQUESTED
        ride_request.updated_at = datetime.now(timezone.utc)
        ride = self.rides.get(ride_id)
        if ride:
            ride.status = RideStatus.CANCELED
            ride.driver_id = None

        return ride_request