from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"

class PaymentCreate(BaseModel):
    ride_id: str
    rider_id: str
    driver_id: str
    amount: float
    payment_method: PaymentMethod = PaymentMethod.CREDIT_CARD

class Payment(BaseModel):
    id: str
    ride_id: str
    rider_id: str
    driver_id: str
    amount: float
    payment_method: PaymentMethod
    status: PaymentStatus
    transaction_id: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    completed_at: datetime | None = None

class PaymentResponse(BaseModel):
    message: str
    payment: Payment
