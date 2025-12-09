import json
from openai import OpenAI
from ..models.ai_service_models import ParsedRideRequest
from dotenv import load_dotenv
import os

load_dotenv()

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def parse_ride_request(self, request_text: str) -> dict:
        # Get input text from user: request_text

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
        
        return ParsedRideRequest(
            pickup_location=parsed_json.get("pickup_location"),
            dropoff_location=parsed_json.get("dropoff_location")
        )

        # Call ride service to create ride request with parsed data (will implement later)