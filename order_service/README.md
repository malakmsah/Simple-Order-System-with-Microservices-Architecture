# Order Service

## Overview
The Order Service is a standalone microservice responsible for managing customer orders.  
It orchestrates the workflow between the **Product Service** and **Payment Service**, handling:

- Product validation and stock reservation
- Order creation and persistence
- Payment processing with retries
- Order cancellation with reason
- Logging and error handling

It is built with **Django** and **Django REST Framework (DRF)**.

---

## Key Features
- Create orders with multiple products
- Validate product existence and stock via Product Service
- Reserve stock immediately
- Integrate with Payment Service for payments
- Retry payments up to 2 times on failure
- Cancel orders on failures (payment or product issues) and store cancellation reason
- Audit for all orders, including cancelled ones
- Fetch order details along with payment status

---

## Assumptions
- Each microservice has its own database (SQLite for simplicity)
- Product Service provides `id`, `name`, `price`, `stock` only
- Payment Service trusts the `amount` provided by Order Service
- Duplicate requests to Payment Service are handled by `update_or_create` in Payment Service
- Service runs independently on port **8000**
- Only basic logging is included
- Order Service communicates with other services **only via REST APIs**

---

## Prerequisites
- Python 3.10+  
- pip  
- virtualenv  
- Product Service running on `http://localhost:8001/api/products/`  
- Payment Service running on `http://localhost:8002/api/payments/`  

---

## Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd order_service
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
DB_NAME=/full/path/to/order_service_db.sqlite3
PRODUCT_SERVICE_URL=http://localhost:8001/api/products/
PAYMENT_SERVICE_URL=http://localhost:8002/api/payments/
```

5. **Apply database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```
---

## Running the Service
```bash
python manage.py runserver 8000
```

The API will be accessible at: http://localhost:8000/api/orders/

---

## API Endpoints
| Method | Endpoint | Request Body | Response | Description |
|--- |--- |--- |--- |--- |
| POST | /api/orders/ | { "customer_name": "Alice", "product_ids": [1,2] } | Order JSON (status: PAID or CANCELLED)	| Create a new order, reserve stock, call Payment Service, handle retries, and update status. |
| GET | /api/orders/{order_id}/ | N/A | Order JSON with payment_status | Retrieve order details including the payment status. |


### Example POST request
```
curl -X POST http://localhost:8000/api/orders/ \
-H "Content-Type: application/json" \
-d '{
    "customer_name": "Alice",
    "product_ids": [1,2]
}'
```

### Sample Response (PAID):
```
{
    "id": "c1a2b3d4-e5f6-7890-abcd-ef1234567890",
    "customer_name": "Alice",
    "total_amount": 50.00,
    "status": "PAID",
    "cancellation_reason": null,
    "created_at": "2025-11-10T12:05:00Z",
    "payment_status": "COMPLETED"
}
```

### Sample Response (CANCELLED):
```
{
    "id": "f9a8b7c6-d5e4-3210-abcd-ef0987654321",
    "customer_name": "Bob",
    "total_amount": 30.00,
    "status": "CANCELLED",
    "cancellation_reason": "Product 2 not found",
    "created_at": "2025-11-10T12:10:00Z",
    "payment_status": null
}
```

### Error Responses
| Status Code | Response | Description |
|--- |--- |--- |
| 400 | { "error": "customer_name and product_ids required" } | Missing required parameters |
| 404 | { "error": "Order not found" } | GET request for unknown order_id |
| 400 | { "error": "Product X is out of stock" } | Product stock validation failure |
| 400 | { "error": "Payment failed" } | Payment service failed after retries |