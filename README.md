# poke-transformer-api

A small FastAPI service that calls [PokeAPI](https://pokeapi.co/), computes custom
"power" metrics for a Pokémon, stores the result in PostgreSQL, and returns the
saved record.

## Features

- `POST /api/v1/pokemon/`
  - Accepts a Pokémon name (e.g. `"pikachu"`).
  - Fetches base stats from PokeAPI.
  - Computes:
    - `total_base_stats`
    - a custom `power_index`
    - a `tier` classification (`S`, `A`, `B`, `C`).
  - Persists the record in PostgreSQL and returns it.
- Auto-generated OpenAPI docs at `/docs` and `/openapi.json`.
- Separate dev and test databases (PostgreSQL).

## Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL (psycopg driver)
- httpx (PokeAPI client)
- Poetry for dependency management
- pytest (+ pytest-asyncio) for tests

## Getting started (development)

### 1. Clone and install

```bash
git clone <your-repo-url> poke-transformer-api
cd poke-transformer-api

# Install dependencies
poetry install
