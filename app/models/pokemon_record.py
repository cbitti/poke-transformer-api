from datetime import datetime

from sqlalchemy import String, DateTime, Integer, Float, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class PokemonRecord(Base):
    __tablename__ = "pokemon_records"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Core identity
    pokemon_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    pokedex_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Raw base stats
    base_hp: Mapped[int] = mapped_column(Integer, nullable=False)
    base_attack: Mapped[int] = mapped_column(Integer, nullable=False)
    base_defense: Mapped[int] = mapped_column(Integer, nullable=False)
    base_special_attack: Mapped[int] = mapped_column(Integer, nullable=False)
    base_special_defense: Mapped[int] = mapped_column(Integer, nullable=False)
    base_speed: Mapped[int] = mapped_column(Integer, nullable=False)

    # Aggregated / derived metrics
    total_base_stats: Mapped[int] = mapped_column(Integer, nullable=False)
    power_index: Mapped[float] = mapped_column(Float, nullable=False)
    tier: Mapped[str] = mapped_column(String(1), nullable=False)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
