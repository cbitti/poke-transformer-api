# poke-transformer-api

A FastAPI-based web service that:

- Accepts POST requests with a Pokémon name.
- Calls the public PokeAPI to fetch data about that Pokémon.
- Applies a custom transformation (e.g. compute power index / tier).
- Stores the transformed result in the database.

## Tech stack (planned)

- Python (FastAPI)
- SQLite (dev) → PostgreSQL (later)
- Poetry for dependency management
- SQLAlchemy + Alembic for database/migrations

## Development

Instructions will be filled in as we build the project step by step.
