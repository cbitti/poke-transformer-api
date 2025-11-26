"""drop redundant id index

Revision ID: 3233068d2641
Revises: 4ee000f50b34
Create Date: 2025-11-26 14:08:29.877915

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3233068d2641"
down_revision: Union[str, Sequence[str], None] = "4ee000f50b34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_pokemon_records_id", table_name="pokemon_records")


def downgrade() -> None:
    op.create_index(
        "ix_pokemon_records_id",
        "pokemon_records",
        ["id"],
        unique=False,
    )
