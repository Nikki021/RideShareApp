from fastapi import HTTPException
import requests
import uuid
from datetime import datetime, timezone
from ..models.payment_model import Payment, PaymentCreate, PaymentStatus, PaymentMethod

USER_SERVICE_URL = "http://localhost:8000"
RIDE_SERVICE_URL = "http://localhost:8001"

class PaymentService:
    def __init__(self):
        self.payments = {}
        self.rider_balances = {}
        self.driver_balances = {}
    
    def _validate_user(self, user_id: str, expected_role: str):
        try:
            response = requests.get(f"{USER_SERVICE_URL}/users/verify/{user_id}")
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="User service is unavailable")
            data = response.json()
            if not data.get("exists"):
                raise HTTPException(status_code=404, detail=f"{expected_role.capitalize()} not found")
            elif not data.get("is_logged_in"):
                raise HTTPException(status_code=401, detail=f"{expected_role.capitalize()} is not logged in")
            elif data.get("role") != expected_role:
                raise HTTPException(status_code=403, detail=f"User is not a {expected_role}")
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="Unable to connect to user service")
    
    def _validate_ride(self, ride_id: str):
        try:
            response = requests.get(f"{RIDE_SERVICE_URL}/rides/{ride_id}")
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Ride not found")
            elif response.status_code != 200:
                raise HTTPException(status_code=500, detail="Ride service is unavailable")
            return response.json()
        except requests.exceptions.RequestException:
            raise HTTPException(status_code=500, detail="Unable to connect to ride service")
    
    def process_payment(self, payment_create: PaymentCreate) -> Payment:
        self._validate_user(payment_create.rider_id, "rider")
        self._validate_user(payment_create.driver_id, "driver")
        
        if payment_create.amount <= 0:
            raise HTTPException(status_code=400, detail="Payment amount must be greater than 0")
        
        transaction_id = f"TXN-{uuid.uuid4()}"
        payment = Payment(
            id=str(uuid.uuid4()),
            ride_id=payment_create.ride_id,
            rider_id=payment_create.rider_id,
            driver_id=payment_create.driver_id,
            amount=payment_create.amount,
            payment_method=payment_create.payment_method,
            status=PaymentStatus.PROCESSING,
            transaction_id=transaction_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        try:
            self._process_transaction(payment)
            payment.status = PaymentStatus.COMPLETED
            payment.completed_at = datetime.now(timezone.utc)
            payment.updated_at = datetime.now(timezone.utc)
        except Exception as e:
            payment.status = PaymentStatus.FAILED
            payment.updated_at = datetime.now(timezone.utc)
            raise HTTPException(status_code=500, detail=f"Payment processing failed: {str(e)}")
        
        self.payments[payment.id] = payment
        return payment
    
    def _process_transaction(self, payment: Payment):
        if payment.rider_id not in self.rider_balances:
            self.rider_balances[payment.rider_id] = 0
        
        self.rider_balances[payment.rider_id] -= payment.amount
        
        if payment.driver_id not in self.driver_balances:
            self.driver_balances[payment.driver_id] = 0
        
        self.driver_balances[payment.driver_id] += payment.amount
    
    def get_payment(self, payment_id: str) -> Payment:
        payment = self.payments.get(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    
    def get_payment_history(self, user_id: str) -> list[Payment]:
        user_payments = [
            payment for payment in self.payments.values()
            if payment.rider_id == user_id or payment.driver_id == user_id
        ]
        return sorted(user_payments, key=lambda x: x.created_at, reverse=True)
    
    def get_rider_payments(self, rider_id: str) -> list[Payment]:
        self._validate_user(rider_id, "rider")
        rider_payments = [
            payment for payment in self.payments.values()
            if payment.rider_id == rider_id
        ]
        return sorted(rider_payments, key=lambda x: x.created_at, reverse=True)
    
    def get_driver_earnings(self, driver_id: str) -> dict:
        self._validate_user(driver_id, "driver")
        driver_payments = [
            payment for payment in self.payments.values()
            if payment.driver_id == driver_id and payment.status == PaymentStatus.COMPLETED
        ]
        total_earnings = sum(payment.amount for payment in driver_payments)
        return {
            "driver_id": driver_id,
            "total_earnings": total_earnings,
            "payment_count": len(driver_payments),
            "payments": sorted(driver_payments, key=lambda x: x.created_at, reverse=True)
        }
