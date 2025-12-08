from pydantic import BaseModel
from datetime import datetime

class ParsedRideRequest(BaseModel):
    pickup_location: str
    dropoff_location: str