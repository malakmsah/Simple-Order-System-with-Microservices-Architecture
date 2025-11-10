# Simple Order System - Microservices Architecture

## Overview

This project implements a **modular order system** using **Django microservices**, with three independent services:

1. **Product Service** (`product_service`) - manages product catalog  
2. **Payment Service** (`payment_service`) - processes payments  
3. **Order Service** (`order_service`) - handles orders and orchestrates the workflow  

Each service runs independently, has its own database (SQLite), and communicates via **REST APIs**.  
The system demonstrates **Django fundamentals, RESTful design, microservice communication, and error handling**.

---

## Architecture

```text
+-----------------+         HTTP REST         +-----------------+
|                 |  GET /api/products/{id}  |                 |
|  Order Service  | ----------------------> | Product Service |
|                 |                          |                 |
|  Creates order  |  POST /api/products/     |  Manages        |
|  workflow       |                          |  products       |
|                 | <---------------------- |                 |
|                 |      JSON response       |                 |
+-----------------+                          +-----------------+
         |
         |  POST /api/payments/ (retries up to 2x)
         v
+-----------------+
| Payment Service |
|  Processes      |
|  payments       |
+-----------------+

```
---
## Services
1. **Product Service**
- Port: 8001
- Responsibilities:
    - CRUD operations for products
    - Validate price > 0 and stock ≥ 0
    - JWT-based admin authentication for creating products
- API Highlights:
    - GET /api/products/ - list all products
    - GET /api/products/{id}/ - product details
    - POST /api/products/ - create new product (admin only)

2. **Payment Service**
- Port: 8002
- Responsibilities:
    - Create payments for orders
    - Simulate payment processing: COMPLETED if amount > 0, FAILED otherwise
    - Prevent double charging
- API Highlights:
    - POST /api/payments/ - create a payment
    - GET /api/payments/{order_id}/ - check payment status

3. **Order Service**
- Port: 8000
- Responsibilities:
    - Create and manage orders
    - Fetch product data from Product Service
    - Reserve stock immediately
    - Call Payment Service with retries (2x)
    - Cancel orders on product/payment failures and store cancellation reason
    - Provide order details with payment status
- API Highlights:
    - POST /api/orders/ - create an order
    - GET /api/orders/{order_id}/ - get order details

---

## Prerequisites
- Python 3.10+
- pip
- virtualenv
- Git

Make sure each microservice is running before testing dependent services.

---

## Setup Instructions
1. Clone the repository
```bash
git clone <repository-url>
cd <repository-root>
```

2. Navigate and set up each service
Example for Product Service:
```bash
cd product_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

Repeat similar steps for:
- payment_service → port 8002
- order_service → port 8000

---

## Running the System
- Start Product Service: python manage.py runserver 8001
- Start Payment Service: python manage.py runserver 8002
- Start Order Service: python manage.py runserver 8000
Order Service depends on the other two services, so start them first.

---

## Assumptions

- Each service has its own database (SQLite)
- Communication is only via REST APIs
- Payment Service trusts amount from Order Service
- JWT auth is implemented only for admin POST on Product Service
- Stock is reserved immediately; cancellations are recorded with reason for audit
- Duplicate payment requests are prevented by Payment Service

---

## Logging
Minimal logging is included for:
- Product fetch errors
- Payment retries
- Order cancellations

--- 

## Example Workflow
1. Admin creates products in Product Service.
2. Customer creates an order via Order Service, providing product_ids and customer_name.
3. Order Service:
    - Validates product availability
    - Reserves stock
    - Calculates total amount
    - Calls Payment Service (2 retries on failure)
    - Updates order status to PAID or CANCELLED
4. Customer can check order details including payment status.

---

## Postman Collection URL

https://www.postman.com/malakmsah/workspace/simple-order-system/collection/4768069-35d6494c-a44b-4b37-9c00-ef340c05e9fa?action=share&source=copy-link&creator=4768069

--- 

## Notes
- Designed for simplicity using SQLite; can be replaced with PostgreSQL/MySQL in production.
- Each microservice is independent and deployable separately.
