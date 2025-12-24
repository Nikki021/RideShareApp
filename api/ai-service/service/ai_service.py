import json
from openai import OpenAI
from ..models.ai_service_models import ParsedRideRequest
from dotenv import load_dotenv
import os
import requests

load_dotenv()
ride_service_url = os.getenv("RIDE_SERVICE_URL", "http://localhost:8001")
user_service_url = os.getenv("USER_SERVICE_URL", "http://localhost:8000")

class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None

    def parse_ride_request(self, request_text: str) -> dict:
        # Get input text from user: request_text

        # If no OpenAI API key is provided, use simple text parsing
        if not self.client:
            return self._parse_with_simple_logic(request_text)

        # Pass this text to an AI model (e.g., OpenAI GPT) to extract pickup and dropoff locations
        response_from_llm = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": f"""You are an AI for a rideshare app. Extract ONLY:
- pickup_location
- dropoff_location

Ignore any time references because the user is requesting a ride NOW.

If the user message does not clearly contain two distinct locations,
return an error message instead of guessing.

Return strictly JSON with:
pickup_location, dropoff_location

User text: "{request_text}"
""",
                    "response_format": {"type": "json_object"}
                }
            ]
        )

        parsed_json = json.loads(response_from_llm.choices[0].message.content)

        if not parsed_json.get("pickup_location") or not parsed_json.get("dropoff_location"):
            raise ValueError("Failed to extract necessary ride request details")
        
        # Create a temporary user in user service to associate with the ride request
        print("Creating temporary user in user service...")
        user_creation_response = requests.post(user_service_url + "/users/register", json={
            "username": "temp_ai_user",
            "email": f"temp_ai_user_{os.urandom(4).hex()}@example.com",
            "password": "temporary_password",
            "role": "rider"
        })
        if user_creation_response.status_code != 200:
            raise Exception("Failed to create temporary user in user service")
        temp_user = user_creation_response.json().get("user_details")
        print("Temporary user created:", temp_user)

        # Login the temporary user to get a session (if needed)
        print("Logging in temporary user...")
        login_response = requests.post(user_service_url + "/users/login", params={
            "email": temp_user.get("email"),
            "password": "temporary_password"
        })
        if login_response.status_code != 200:
            raise Exception("Failed to log in temporary user")
        print("Temporary user logged in successfully.")
        
        # Call ride service to create ride request with parsed data
        print("Calling ride service to create ride request...")
        ride_service_response = requests.post(ride_service_url + "/ride-requests/create", json={
            "user_id": temp_user["id"],
            "pickup_location": parsed_json.get("pickup_location"),
            "dropoff_location": parsed_json.get("dropoff_location")
        })

        if ride_service_response.status_code != 200:
            raise Exception("Failed to create ride request in ride service")
        
        print("Ride request created successfully in ride service.")
        return {
            "pickup_location": parsed_json.get("pickup_location"),
            "dropoff_location": parsed_json.get("dropoff_location")
        }

    def _parse_with_simple_logic(self, request_text: str) -> dict:
        """Simple text parsing fallback when OpenAI API is not available"""
        # Look for common patterns like "from X to Y" or "X to Y"
        text_lower = request_text.lower()
        
        # Try to extract locations from common patterns
        if " from " in text_lower and " to " in text_lower:
            parts = text_lower.split(" from ")
            if len(parts) > 1:
                rest = parts[1].split(" to ")
                if len(rest) >= 2:
                    pickup = rest[0].strip()
                    dropoff = rest[1].strip()
                    return {
                        "pickup_location": pickup.title(),
                        "dropoff_location": dropoff.title()
                    }
        
        # Try simpler pattern "X to Y"
        if " to " in text_lower:
            parts = text_lower.split(" to ")
            if len(parts) >= 2:
                pickup = parts[0].strip()
                dropoff = parts[1].strip()
                return {
                    "pickup_location": pickup.title(),
                    "dropoff_location": dropoff.title()
                }
        
        # Default fallback
        raise ValueError("Could not parse locations. Please use format: 'from [pickup] to [dropoff]' or '[pickup] to [dropoff]'")

        # Call ride service to create ride request with parsed data (will implement later)