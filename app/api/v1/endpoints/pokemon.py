from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.pokemon import PokemonCreate, PokemonRecordRead
from app.services.pokemon_transformer import (
    PokemonAPIError,
    PokemonNotFoundError,
    fetch_transform_and_store_pokemon,
)

router = APIRouter()


@router.post(
    "/",
    response_model=PokemonRecordRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a transformed Pokémon record",
    description=(
        "Fetches Pokémon data from PokeAPI, computes power metrics, "
        "stores the record in the database, and returns the stored row."
    ),
)
async def create_pokemon_record_endpoint(
    payload: PokemonCreate,
    db: Session = Depends(get_db),
) -> PokemonRecordRead:
    """
    Create a Pokémon record by fetching data from PokeAPI and transforming it.
    """
    try:
        record = await fetch_transform_and_store_pokemon(
            db=db,
            pokemon_name=payload.pokemon_name,
        )
    except PokemonNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except PokemonAPIError as exc:
        # Something else went wrong talking to PokeAPI
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return record
