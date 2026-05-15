# Pizza App API

A clean, production-style FastAPI backend for a pizza ordering platform. It combines JWT authentication, role-based access control, and order management in a compact codebase that is easy to extend.

## Highlights

- FastAPI with automatic OpenAPI docs
- JWT-based authentication and protected routes
- Regular user and superuser roles
- PostgreSQL-backed persistence with SQLAlchemy
- Consistent JSON responses through a shared response wrapper
- Health endpoint for quick service checks

## What This API Does

Users can sign up, log in, place orders, inspect their own order history, and update pending orders. Superusers can view every order and change order status across the system.

The API intentionally keeps the surface small and focused:

- Authentication lives under `/auth`
- User-facing order actions live under `/orders`
- Admin order actions are protected by superuser checks

## Quick Start

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and set at least:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/pizza_db
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=True
```

If you do not set these values, the app falls back to development defaults defined in `core/config.py`.

### 4. Run the API

```powershell
uvicorn main:app --reload
```

If you prefer a different port, add `--port 5000` or any other available port.

## Access Points

Replace `<port>` with the port you used when starting Uvicorn.

- API root: `http://127.0.0.1:<port>/`
- Health check: `http://127.0.0.1:<port>/health`
- Swagger UI: `http://127.0.0.1:<port>/docs`
- ReDoc: `http://127.0.0.1:<port>/redoc`

## API Overview

### Authentication

- `POST /auth/signup` - Create a regular user
- `POST /auth/login` - Log in and receive an access token

### Orders

Authenticated users can:

- `POST /orders/order` - Create a new order
- `GET /orders/user/orders` - List their own orders
- `GET /orders/user/order/{order_id}` - Retrieve one of their orders
- `PUT /orders/order/update/{order_id}` - Update a pending order
- `DELETE /orders/order/delete/{order_id}` - Delete an order they own

### Superuser Order Controls

Superusers can:

- `GET /orders/orders` - List all orders
- `GET /orders/orders/{order_id}` - Retrieve any order by id
- `PUT /orders/order/status/{order_id}` - Update an order status

## Request Examples

### Sign Up

```bash
curl -X POST "http://127.0.0.1:8000/auth/signup" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"john_doe\",\"email\":\"john@example.com\",\"password\":\"securepassword123\"}"
```

### Log In

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"john@example.com\",\"password\":\"securepassword123\"}"
```

### Create an Order

```bash
curl -X POST "http://127.0.0.1:8000/orders/order" ^
  -H "Authorization: Bearer <your_token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"items\":[{\"name\":\"Margherita\",\"quantity\":2,\"price\":12.99},{\"name\":\"Pepperoni\",\"quantity\":1,\"price\":14.99}],\"total_price\":40.97,\"delivery_address\":\"123 Main St, City, State 12345\"}"
```

## Data Shapes

### User signup

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Order creation

```json
{
  "items": [
    { "name": "Margherita", "quantity": 2, "price": 12.99 },
    { "name": "Pepperoni", "quantity": 1, "price": 14.99 }
  ],
  "total_price": 40.97,
  "delivery_address": "123 Main St, City, State 12345"
}
```

### Order status values

- `pending`
- `confirmed`
- `preparing`
- `ready`
- `delivered`
- `cancelled`

## Authentication Flow

1. Create an account through `/auth/signup`
2. Log in through `/auth/login`
3. Copy the returned access token
4. Send it in the `Authorization: Bearer <token>` header for protected endpoints

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Superuser Setup

The public signup endpoint creates regular users only. To create or promote a superuser, run:

```powershell
python scripts/create_superuser.py --username admin --email admin@example.com
```

You will be prompted for a password securely. You can also pass one directly:

```powershell
python scripts/create_superuser.py --username admin --email admin@example.com --password "StrongPass123"
```

## Response Format

API responses use a consistent envelope:

```json
{
  "status": 200,
  "message": "Success message",
  "data": {}
}
```

That makes client handling predictable across auth and order routes.

## Project Structure

```text
pizza-app-backend-new/
├── api/
│   ├── auth.py
│   └── orders.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── middleware/
│   └── auth.py
├── models/
│   ├── user.py
│   └── order.py
├── schemas/
│   ├── user.py
│   └── order.py
├── services/
│   ├── user_service.py
│   └── order_service.py
├── scripts/
│   └── create_superuser.py
├── utlis/
│   └── response.py
├── main.py
├── requirements.txt
└── README.md
```

## Configuration

Key environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing secret
- `DEBUG` - Debug mode toggle

Defaults are defined in `core/config.py`.

## Notes For Development

- The app enables CORS for all origins in development.
- Tables are created on startup from SQLAlchemy metadata.
- The root endpoint returns a simple status message, and `/health` is useful for uptime checks or smoke tests.

## Troubleshooting

- If login fails, confirm the database is reachable and your user exists.
- If startup fails, check `DATABASE_URL` and your PostgreSQL credentials.
- If protected routes return `401`, make sure you are sending a valid bearer token.

## License

No license file is currently included. Add one if you plan to publish or distribute this project.
