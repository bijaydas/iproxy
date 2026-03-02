# TAPI

A minimal FastAPI template for building modern APIs quickly.

## Features

- **FastAPI** - Fast, modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Robust database backend
- **Alembic** - Database migrations
- **Argon2** - Secure password hashing
- **CORS** - Cross-Origin Resource Sharing enabled
- **Logging** - Built-in request logging middleware
- **Error Handling** - Centralized exception handling


## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL

### Installation

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uv run fastapi run app/main.py
```

### Running Tests

```bash
pytest
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

```bash
# Format and lint code
ruff check --fix .

# Generate new migration
alembic revision --autogenerate -m "description"
```

## License

MIT

