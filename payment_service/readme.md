# Payment Service

## Overview
The Payment Service is a standalone microservice responsible for processing payments for orders.  
It provides RESTful APIs to create and retrieve payments and is built with **Django** and **Django REST Framework (DRF)**.

### Key Features
- Create a payment for an order
- Simulate payment processing:
  - `COMPLETED` if `amount > 0`
  - `FAILED` if `amount <= 0`
- Retrieve payment status by `order_id`
- Prevent double-charging using `update_or_create`
- Minimal logging for debugging
- Each service has its own database (SQLite by default)

---

## Assumptions
- Each microservice has its own isolated database (SQLite for simplicity)
- Payment Service trusts the amount sent by Order Service
- Duplicate payment requests for the same `order_id` are prevented
- Service runs independently on port **8002**
- Only `POST` (create) and `GET` (status) endpoints are implemented
- No user authentication is required for now

---

## Prerequisites
- Python 3.10+  
- pip  
- virtualenv  

---

## Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd payment_service
```

2. **Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file (optional for custom DB configuration)**
```bash
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/full/path/to/payments_db.sqlite3
```

5. **Apply database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Service
```bash
python manage.py runserver 8002
```

The API will be accessible at: http://localhost:8002/api/payments/

## API Endpoints

Base URL: http://localhost:8002/api/payments/

| Method | Endpoint | Auth | Request | Body | Response | Description |
|--- |--- |--- |--- |--- |--- |--- |
| POST | / | None | json | { "order_id": "<uuid>", "amount": 100.50 } | json | { "id": "<uuid>", "order_id": "<uuid>", "amount": 100.50, "status": "COMPLETED", "timestamp": "2025-11-10T12:00:00Z" } | Create a payment for an order. Status is COMPLETED if amount > 0, FAILED otherwise. Prevents double-charging using update_or_create. |
| GET | /<order_id>/ | None | N/A | json | { "id": "<uuid>", "order_id": "<uuid>", "amount": 100.50, "status": "COMPLETED", "timestamp": "2025-11-10T12:00:00Z" } | Retrieve payment details and status for a specific order ID. Returns 404 if payment not found. |

## Example POST request
```
curl -X POST http://localhost:8002/api/payments/ \
-H "Content-Type: application/json" \
-d '{
    "order_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "amount": 50.00
}'
```

Response:
```
{
    "id": "f9a1b2c3-d4e5-6789-abcd-ef0123456789",
    "order_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "amount": 50.00,
    "status": "COMPLETED",
    "timestamp": "2025-11-10T12:05:00Z"
}
```

## Example GET request
```
curl -X GET http://localhost:8002/api/payments/a1b2c3d4-e5f6-7890-abcd-ef1234567890/
```

Response:
```
{
    "id": "f9a1b2c3-d4e5-6789-abcd-ef0123456789",
    "order_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "amount": 50.00,
    "status": "COMPLETED",
    "timestamp": "2025-11-10T12:05:00Z"
}
```

## Error Responses
| Status Code | Response | Description |
|--- |--- |--- |
| 400 | { "error": "order_id and amount required" } | Missing parameters in POST |
| 404 | { "error": "Payment not found" } | GET request for unknown order_id |
| 400 | { "error": "Amount must be positive." } | Validation error if amount <= 0 (status set to FAILED internally) |
