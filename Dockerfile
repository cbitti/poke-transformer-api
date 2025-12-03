# Dockerfile
# Use a reasonably modern Python image.
FROM python:3.12-slim

# Environment settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false

# System deps (build tools, postgres client libs if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir "poetry"

# Set working directory
WORKDIR /app

# Install dependencies first (cache-friendly layer)
COPY pyproject.toml poetry.lock* ./

# Only install main (non-dev) dependencies for the runtime image
RUN poetry install --no-root --only main

# Now copy the rest of the app
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run migrations then start the server.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
