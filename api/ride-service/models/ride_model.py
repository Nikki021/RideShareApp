from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class RideRequestStatus(str, Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    CANCELED = "canceled"

class RideStatus(str, Enum):
    REQUESTED = "requested"
    DRIVER_ASSIGNED = "driver_assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"

class RideRequestCreate(BaseModel):
    user_id: str
    pickup_location: str
    dropoff_location: str

class RideRequest(BaseModel):
    id: str
    user_id: str
    pickup_location: str
    dropoff_location: str
    requested_at: datetime
    status: RideRequestStatus = RideRequestStatus.REQUESTED

class DriverStatus(BaseModel):
    driver_id: str
    is_available: bool
    current_location: str
    updated_at: datetime

class Ride(BaseModel):
    id: str
    ride_request_id: str
    driver_id: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    fare: float | None = None
    status: str  # e.g., "in_progress", "completed", "canceled"
