from fastapi import APIRouter
from ..models.payment_model import PaymentCreate, PaymentResponse
from ..service.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])
payment_service = PaymentService()

@router.post("/process", response_model=PaymentResponse)
def process_payment(payment_create: PaymentCreate):
    """
    Process a payment for a ride.
    Deducts amount from rider and credits it to the driver.
    """
    payment = payment_service.process_payment(payment_create)
    return PaymentResponse(
        message="Payment processed successfully",
        payment=payment
    )

@router.get("/{payment_id}")
def get_payment(payment_id: str):
    """
    Get details of a specific payment by payment ID.
    """
    payment = payment_service.get_payment(payment_id)
    return {
        "message": "Payment details retrieved successfully",
        "payment": payment
    }

@router.get("/history/{user_id}")
def get_payment_history(user_id: str):
    """
    Get payment history for a user (rider or driver).
    """
    payments = payment_service.get_payment_history(user_id)
    return {
        "message": "Payment history retrieved successfully",
        "user_id": user_id,
        "payment_count": len(payments),
        "payments": payments
    }

@router.get("/rider/{rider_id}/payments")
def get_rider_payments(rider_id: str):
    """
    Get all payments made by a specific rider.
    """
    payments = payment_service.get_rider_payments(rider_id)
    return {
        "message": "Rider payments retrieved successfully",
        "rider_id": rider_id,
        "payment_count": len(payments),
        "payments": payments
    }

@router.get("/driver/{driver_id}/earnings")
def get_driver_earnings(driver_id: str):
    """
    Get total earnings and payment details for a specific driver.
    """
    earnings = payment_service.get_driver_earnings(driver_id)
    return {
        "message": "Driver earnings retrieved successfully",
        **earnings
    }
