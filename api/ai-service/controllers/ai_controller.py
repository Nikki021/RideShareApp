from fastapi import APIRouter
from pydantic import BaseModel
from ..service.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["ai"])

ai_service = AIService()

class ParseRequest(BaseModel):
    request_text: str

@router.post("/parse_ride_request")
def parse_ride_request(request: ParseRequest):
    # Placeholder logic for parsing ride request using AI
    try:
        response = ai_service.parse_ride_request(request.request_text)
        return {
            "message": "Ride request parsed successfully",
            "parsed_details": response
        }
    except Exception as e:
        return {"error": str(e)}