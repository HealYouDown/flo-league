import csv
import io
import typing as t

from sqlalchemy import case, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.db.models import Player
from src.enums import CharacterClass


def upsert_players(session: Session, *, data: list[dict]) -> None:
    stmt = insert(Player)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Player.id],
        set_={
            "name": stmt.excluded.name,
            "level_land": stmt.excluded.level_land,
            "level_sea": stmt.excluded.level_sea,
            "character_class": stmt.excluded.character_class,
            "is_female": stmt.excluded.is_female,
            "is_active": stmt.excluded.is_active,
            "updated_at": func.now(),
        },
    )
    session.execute(stmt, data)


def update_players_from_csv(session: Session, *, data: bytes) -> None:
    """Given a SQL Server 2005 export, we upsert all player data.

    Args:
        session (Session): DB Session
        data (bytes): CSV with player data exported and converted to bytes.
    """
    text_stream = io.TextIOWrapper(io.BytesIO(data), encoding="utf-16", newline="")
    reader = csv.DictReader(text_stream, delimiter=";")

    players_data = [
        {
            "id": int(row["id"]),
            "name": row["name"],
            "level_land": int(row["level_land"]),
            "level_sea": int(row["level_sea"]),
            "character_class": CharacterClass(int(row["character_class"])),
            "is_female": bool(int(row["is_female"])),
            "is_active": bool(int(row["is_active"])),
        }
        for row in reader
    ]

    upsert_players(session, data=players_data)
    session.commit()


def get_player(session: Session, *, id: int) -> Player | None:
    stmt = select(Player).where(Player.id == id)
    return session.scalar(stmt)


def search_players(session: Session, *, name: str, limit: int) -> t.Sequence[Player]:
    search_term = name.strip()

    stmt = (
        select(Player)
        .where(Player.is_active)
        .where(Player.name.ilike(f"%{search_term}%"))
        .order_by(
            # exact match first
            case((func.lower(Player.name) == search_term.lower(), 0), else_=1),
            # prefix match next
            case((func.lower(Player.name).startswith(search_term.lower()), 0), else_=1),
            # fallback ordering by id
            Player.id.asc(),
        )
        .limit(limit)
    )

    return session.scalars(stmt).all()
