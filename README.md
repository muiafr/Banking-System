# Banking System

A Python banking application with a command-line interface, a MySQL data layer, and a small FastAPI interface. The project manages users, balances, deposits, and transfers; the same MySQL tables are used by the CLI and the API models.

## Features

### Command-line application

- Creates the `users`, `transactions`, and `deposits` tables on startup when they do not exist.
- Creates, views, updates, and deletes user profiles.
- Checks unique nicknames, emails, and phone numbers when a user is created.
- Validates email addresses, phone numbers, positive amounts, and password strength.
- Stores passwords as SHA-256 hashes in the CLI flow.
- Adds deposits to a user's balance and records each deposit with a timestamp.
- Sends money between two different users, checks for sufficient balance, and records the transfer.
- Uses `SELECT ... FOR UPDATE` while reading the sender balance for a transfer.
- Shows a user's transaction history, ordered from newest to oldest.

### FastAPI interface

- Uses FastAPI, SQLAlchemy, and Pydantic schemas.
- Provides read endpoints for users, transactions, and deposits.
- Provides a user-creation endpoint with Pydantic validation.

> The API currently exposes data retrieval and user creation. Deposits and transfers are created through the CLI, not through API POST endpoints.

## Tech stack

- Python
- MySQL
- `mysql-connector-python` for the CLI data access layer
- SQLAlchemy and PyMySQL for the FastAPI models/session
- FastAPI, Pydantic, and Uvicorn
- `python-dotenv` for database configuration

## Project structure

```text
.
├── main.py                         # CLI entry point
├── backend/
│   └── api.py                      # FastAPI application entry point
├── banking/
│   ├── db.py                       # MySQL helpers and table creation
│   ├── database.py                 # SQLAlchemy engine and session
│   ├── models/                     # SQLAlchemy models
│   ├── routes/                     # FastAPI routers
│   ├── schemas/                    # Pydantic request schemas
│   ├── profile/                    # CLI menus and operations
│   └── validators.py               # CLI input validation and hashing
└── requirements.txt
```

## Database configuration

Create a `.env` file in the project root:

```env
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=banking_system
```

Create the database in MySQL before starting the application. The CLI creates the required tables automatically on its first run.

## Installation

```bash
git clone <repository-url>
cd <repository-folder>
python -m venv .venv
```

Activate the virtual environment, then install the listed dependencies:

```bash
pip install -r requirements.txt
```

The API code also imports `pymysql` and uses Pydantic's `EmailStr`; install `PyMySQL` and `email-validator` if they are not already available in your environment:

```bash
pip install PyMySQL email-validator
```

## Run the CLI

```bash
python main.py
```

Choose a menu section to manage user profiles, transfers, or deposits.

## Run the API

```bash
uvicorn backend.api:app --reload
```

The server starts at `http://127.0.0.1:8000`. Interactive API documentation is available at `/docs`.

## API routes currently implemented

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/users/` | List users |
| `GET` | `/users/{user_id}` | Get a user by ID |
| `POST` | `/users/users` | Create a user |
| `GET` | `/transactions/` | List transactions |
| `GET` | `/transactions/{transaction_id}` | Get a transaction by ID |
| `GET` | `/deposits/` | List deposits |
| `GET` | `/deposits/{deposit_id}` | Get a deposit by ID |

## Notes

This is a learning project, not a production banking service. Before production use it would need, among other work, a stronger password-hashing algorithm, authentication and authorization, API error handling, and automated tests.

The source also declares `GET /transactions/user/{user_id}`. Because `GET /transactions/{transaction_id}` is registered first, the more general route currently matches that URL first; reordering those two declarations is needed before the user-specific API route can be used.
