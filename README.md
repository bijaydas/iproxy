# TAPI

A minimal FastAPI template for building modern APIs quickly.

## Quick Start


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

