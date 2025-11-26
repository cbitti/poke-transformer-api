from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class PokemonRecord(Base):
    __tablename__ = "pokemon_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    pokemon_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
