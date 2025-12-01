from __future__ import annotations

from typing import Any, Dict

import httpx
from sqlalchemy.orm import Session

from app.models.pokemon_record import PokemonRecord

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"


class PokemonAPIError(Exception):
    """Base error for PokeAPI-related issues."""


class PokemonNotFoundError(PokemonAPIError):
    """Raised when the Pokémon is not found in PokeAPI."""


async def fetch_pokemon_from_pokeapi(name: str) -> Dict[str, Any]:
    """Call PokeAPI and return the JSON payload for a given Pokémon name."""
    url = f"{POKEAPI_BASE_URL}{name.lower()}"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
    except httpx.RequestError as exc:
        raise PokemonAPIError("Could not reach PokeAPI") from exc

    if response.status_code == 404:
        raise PokemonNotFoundError(f"Pokémon '{name}' not found in PokeAPI")

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise PokemonAPIError(
            f"PokeAPI returned an error: {exc.response.status_code}"
        ) from exc

    data = response.json()
    if not isinstance(data, dict):
        raise PokemonAPIError("Unexpected response format from PokeAPI")

    return data


def compute_metrics(poke_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Take the raw PokeAPI payload and compute our custom metrics, plus
    extract the base stats we want to store.

    Expects structure roughly like:
    {
        "id": 25,
        "name": "pikachu",
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp", ...}},
            {"base_stat": 55, "stat": {"name": "attack", ...}},
            ...
        ],
        ...
    }
    """
    try:
        pokedex_id = int(poke_data["id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise PokemonAPIError("PokeAPI payload missing or invalid 'id' field") from exc

    stats_list = poke_data.get("stats")
    if not isinstance(stats_list, list):
        raise PokemonAPIError("PokeAPI payload missing 'stats' list")

    # Map of stat name -> base_stat
    stat_map: Dict[str, int] = {}
    for entry in stats_list:
        try:
            stat_name = str(entry["stat"]["name"])
            base_stat = int(entry["base_stat"])
        except (KeyError, TypeError, ValueError) as exc:
            raise PokemonAPIError("Unexpected structure in 'stats' entries") from exc
        stat_map[stat_name] = base_stat

    # Extract the stats we care about, defaulting to 0 if missing
    base_hp = stat_map.get("hp", 0)
    base_attack = stat_map.get("attack", 0)
    base_defense = stat_map.get("defense", 0)
    base_special_attack = stat_map.get("special-attack", 0)
    base_special_defense = stat_map.get("special-defense", 0)
    base_speed = stat_map.get("speed", 0)

    total_base_stats = (
        base_hp
        + base_attack
        + base_defense
        + base_special_attack
        + base_special_defense
        + base_speed
    )

    # A made-up but consistent "power index"
    power_index = (
        total_base_stats
        + base_attack * 0.5
        + base_special_attack * 0.5
        + base_speed * 0.3
    )

    if power_index >= 600:
        tier = "S"
    elif power_index >= 500:
        tier = "A"
    elif power_index >= 400:
        tier = "B"
    else:
        tier = "C"

    return {
        "pokedex_id": pokedex_id,
        "base_hp": base_hp,
        "base_attack": base_attack,
        "base_defense": base_defense,
        "base_special_attack": base_special_attack,
        "base_special_defense": base_special_defense,
        "base_speed": base_speed,
        "total_base_stats": total_base_stats,
        "power_index": float(power_index),
        "tier": tier,
    }


def create_pokemon_record(
    db: Session,
    pokemon_name: str,
    metrics: Dict[str, Any],
) -> PokemonRecord:
    """Persist a Pokémon record in the database and return it."""
    record = PokemonRecord(
        pokemon_name=pokemon_name.lower(),
        pokedex_id=metrics["pokedex_id"],
        base_hp=metrics["base_hp"],
        base_attack=metrics["base_attack"],
        base_defense=metrics["base_defense"],
        base_special_attack=metrics["base_special_attack"],
        base_special_defense=metrics["base_special_defense"],
        base_speed=metrics["base_speed"],
        total_base_stats=metrics["total_base_stats"],
        power_index=metrics["power_index"],
        tier=metrics["tier"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


async def fetch_transform_and_store_pokemon(
    db: Session,
    pokemon_name: str,
) -> PokemonRecord:
    """
    High-level operation used by the endpoint:

    1) Fetch from PokeAPI
    2) Compute metrics
    3) Store in DB
    4) Return the SQLAlchemy model
    """
    poke_data = await fetch_pokemon_from_pokeapi(pokemon_name)
    metrics = compute_metrics(poke_data)
    record = create_pokemon_record(db, pokemon_name, metrics)
    return record
