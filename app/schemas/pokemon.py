from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PokemonCreate(BaseModel):
    """Body of the POST request."""

    pokemon_name: str = Field(..., min_length=1)


class PokemonRecordRead(BaseModel):
    """What we return after processing and saving a Pokémon."""

    id: int
    pokemon_name: str
    pokedex_id: int

    base_hp: int
    base_attack: int
    base_defense: int
    base_special_attack: int
    base_special_defense: int
    base_speed: int

    total_base_stats: int
    power_index: float
    tier: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
