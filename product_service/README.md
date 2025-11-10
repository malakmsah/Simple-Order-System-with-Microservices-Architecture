# Product Service

## Overview
The Product Service is a standalone microservice that manages the product catalog for an order system.  
It provides CRUD operations for products via a RESTful API and is built with **Django** and **Django REST Framework (DRF)**.

### Key Features
- List all products (public)
- Get product details (public)
- Create new products (admin-only, JWT authentication)
- Validation for `price > 0` and `stock >= 0`
- Structured according to SOLID principles and clean architecture
- SQLite database (configurable)

---

## Assumptions
- Each microservice has its own database. For simplicity, SQLite is used.
- POST (create product) requires an **admin user** with JWT token.
- GET endpoints are public and do not require authentication.
- No update or delete endpoints are implemented at this stage.
- This service runs independently on port **8001**.
- Minimal logging is enabled via Django’s default logging.
- Product IDs are auto-incremented integers.

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
cd product_service
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
DB_NAME=/full/path/to/product_service_db.sqlite3
```

5. **Apply database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser (admin)**
```bash
python manage.py createsuperuser
```

---

## Running the Service
```bash
# Run Django development server
python manage.py runserver 8001
```

The API will be accessible at: http://localhost:8001/api/products/

---

## API Endpoints

| Method	| Endpoint	| Auth	| Description |
|---|---|---|---|
| GET	| /api/products/ |	None |List all products |
| GET	| /api/products/{id}/ |	None	| Get product details by ID |
| POST | /api/products/ |	JWT | admin	Create a new product |

## JWT Authentication

1. Obtain access token:
```http
POST /api/token/
{
    "username": "<admin>",
    "password": "<password>"
}
```

2. Refresh token:
```http
POST /api/token/refresh/
{
    "refresh": "<refresh_token>"
}
```

3. Use token for POST requests:
```
Authorization: Bearer <access_token>
```

## Sample POST Request (Admin)
```
POST /api/products/
{
  "name": "Cat Food",
  "price": 10.50,
  "stock": 25
}
```

Response:
```
{
  "id": 1,
  "name": "Cat Food",
  "price": 10.50,
  "stock": 25,
  "created_at": "2025-11-10T12:00:00Z",
  "updated_at": "2025-11-10T12:00:00Z"
}
```
