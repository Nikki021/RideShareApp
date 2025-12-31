# Payment Service

## Overview
The Payment Service handles payment processing for rides in the RideShareApp. It manages transactions between riders and drivers, including payment processing, transaction history, and earnings tracking.

## Features
- **Payment Processing**: Process payments for completed rides
- **Transaction Management**: Track payment status and transaction details
- **Rider Payments**: View payment history for riders
- **Driver Earnings**: Track and view driver earnings
- **Payment Methods**: Currently supports Credit Card payments

## Architecture
The service follows a microservices architecture pattern:
- **Models**: Data models for payments and transactions
- **Service**: Business logic for payment processing
- **Controllers**: REST API endpoints
- **Integration**: Communicates with User Service and Ride Service

## API Endpoints

### Health Check
- `GET /` - Check if the service is running

### Payment Operations
- `POST /payments/process` - Process a payment for a ride
  - Request body: `PaymentCreate` (ride_id, rider_id, driver_id, amount, payment_method)
  - Returns: `PaymentResponse` with payment details and status

- `GET /payments/{payment_id}` - Get details of a specific payment
  - Returns: Payment details including status and transaction ID

- `GET /payments/history/{user_id}` - Get payment history for a user (rider or driver)
  - Returns: List of all payments associated with the user

- `GET /payments/rider/{rider_id}/payments` - Get all payments made by a rider
  - Returns: List of rider's payment history

- `GET /payments/driver/{driver_id}/earnings` - Get driver's total earnings
  - Returns: Total earnings, payment count, and payment list

## Payment Status
Payments can have the following statuses:
- `PENDING`: Payment is initiated but not yet processed
- `PROCESSING`: Payment is being processed
- `COMPLETED`: Payment successfully completed
- `FAILED`: Payment processing failed
- `REFUNDED`: Payment has been refunded

## Payment Methods
Currently supported payment methods:
- `CREDIT_CARD`: Credit card payment (more payment methods to be added in future)

## Running the Service

### Prerequisites
- Python 3.10+
- FastAPI
- Uvicorn

### Installation
```bash
pip install -r requirements.txt
```

### Start the Service
```bash
python3 -m uvicorn api.payment-service.main:app --host 0.0.0.0 --port 8002
```

The service will be available at:
- API: http://localhost:8002
- Interactive API Docs: http://localhost:8002/docs
- OpenAPI Spec: http://localhost:8002/openapi.json

## Integration with Other Services
The Payment Service integrates with:
- **User Service** (port 8000): Validates rider and driver identities
- **Ride Service** (port 8001): Retrieves ride information

## Transaction Flow
1. Rider completes a ride
2. Payment request is submitted with ride details and amount
3. Service validates the rider and driver via User Service
4. Service validates the ride via Ride Service
5. Payment is processed and transaction is created
6. Amount is deducted from rider's account
7. Amount is credited to driver's account
8. Payment status is updated to COMPLETED

## Data Models

### PaymentCreate
```json
{
  "ride_id": "string",
  "rider_id": "string",
  "driver_id": "string",
  "amount": 0.0,
  "payment_method": "credit_card"
}
```

### Payment
```json
{
  "id": "string",
  "ride_id": "string",
  "rider_id": "string",
  "driver_id": "string",
  "amount": 0.0,
  "payment_method": "credit_card",
  "status": "completed",
  "transaction_id": "TXN-...",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "completed_at": "2024-01-01T00:00:00Z"
}
```

## Future Enhancements
- Add more payment methods (Debit Card, PayPal, Wallet, etc.)
- Implement payment refund functionality
- Add payment dispute handling
- Implement payment notifications
- Add payment analytics and reporting
- Integrate with real payment gateways
