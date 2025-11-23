# Mini Rewards Service

A Django-based Rewards Management API where businesses can award points to customers and customers can redeem points. This service is designed with a focus on clean code, correctness, API design, and Django best practices.

## Features

- **Customer Management**:
    - Create, Retrieve, Update, and Soft Delete customers.
    - List customers with pagination and filtering by phone number.
- **Wallet System**:
    - Each customer has a dedicated wallet.
    - **Credit Points**: Add points to a wallet.
    - **Debit Points**: Redeem points from a wallet (checks for sufficient balance).
    - **Atomic Transactions**: Ensures data integrity during credit/debit operations.
    - **Idempotency**: Prevents double-processing of transactions using a unique `idempotency_key`.
- **Transaction History**:
    - View transaction history with filtering (by customer, type, date range) and ordering.
- **API Documentation**: Integrated Swagger/OpenAPI documentation.

## Tech Stack

- **Language**: Python 3.x
- **Framework**: Django 5.x, Django REST Framework (DRF)
- **Database**: SQLite (default) / Postgres ready
- **Documentation**: drf-yasg (Swagger)

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rewards_service
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

Interactive API documentation (Swagger UI) is available at:
- **URL**: `http://127.0.0.1:8000/swagger/`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/customers/` | List all customers (paginated, filter by `search=<phone>`) |
| POST | `/api/customers/` | Create a new customer |
| GET | `/api/customers/{id}/` | Get customer details |
| DELETE | `/api/customers/{id}/` | Soft delete a customer |
| POST | `/api/wallet/credit/` | Credit points to a wallet |
| POST | `/api/wallet/debit/` | Debit points from a wallet |
| GET | `/api/wallet/transactions/` | Get transaction history |

## Testing

### Automated Tests
Run the Django test suite:
```bash
python manage.py test
```


## Sample Inputs & Outputs

### 1. Create Customer
**Endpoint**: `POST /api/customers/`

**Request**:
```json
{
    "name": "Jane Doe",
    "phone": "+19876543210",
    "email": "jane@example.com"
}
```

**Response** (`201 Created`):
```json
{
    "id": 1,
    "name": "Jane Doe",
    "phone": "+19876543210",
    "email": "jane@example.com",
    "created_at": "2025-11-23T10:00:00Z",
    "updated_at": "2025-11-23T10:00:00Z",
    "is_active": true
}
```

### 2. Credit Wallet
**Endpoint**: `POST /api/wallet/credit/`

**Request**:
```json
{
    "customer_id": 1,
    "points": 100,
    "idempotency_key": "unique-key-123"
}
```

**Response** (`201 Created`):
```json
{
    "id": 1,
    "wallet": 1,
    "type": "CREDIT",
    "points": 100,
    "idempotency_key": "unique-key-123",
    "created_at": "2025-11-23T10:05:00Z",
    "meta": {}
}
```

### 3. Debit Wallet
**Endpoint**: `POST /api/wallet/debit/`

**Request**:
```json
{
    "customer_id": 1,
    "points": 50,
    "idempotency_key": "unique-key-456"
}
```

**Response** (`201 Created`):
```json
{
    "id": 2,
    "wallet": 1,
    "type": "DEBIT",
    "points": 50,
    "idempotency_key": "unique-key-456",
    "created_at": "2025-11-23T10:10:00Z",
    "meta": {}
}
```

### 4. Transaction History
**Endpoint**: `GET /api/wallet/transactions/?customer_id=1`

**Response** (`200 OK`):
```json
[
    {
        "id": 2,
        "wallet": 1,
        "type": "DEBIT",
        "points": 50,
        "idempotency_key": "unique-key-456",
        "created_at": "2025-11-23T10:10:00Z",
        "meta": {}
    },
    {
        "id": 1,
        "wallet": 1,
        "type": "CREDIT",
        "points": 100,
        "idempotency_key": "unique-key-123",
        "created_at": "2025-11-23T10:05:00Z",
        "meta": {}
    }
]
```
