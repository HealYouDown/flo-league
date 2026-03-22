import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.db.models import PlayerSeasonStats, Season
from src.exceptions import SeasonNotFound


def create_season(session: Session, *, name: str, description: str) -> Season:
    season = Season(name=name, description=description)
    session.add(season)
    session.commit()
    return season


def get_seasons(session: Session) -> t.Sequence[Season]:
    stmt = select(Season)
    return session.scalars(stmt).all()


def get_season(session: Session, *, id: int) -> t.Optional[Season]:
    stmt = select(Season).where(Season.id == id)
    return session.scalar(stmt)


def delete_season(session: Session, *, id: int) -> None:
    season = get_season(session, id=id)
    if season is not None:
        session.delete(season)
        session.commit()


def get_season_leaderboard(session: Session, id: int) -> t.Sequence[PlayerSeasonStats]:
    stmt = (
        select(PlayerSeasonStats)
        .where(PlayerSeasonStats.season_id == id)
        .options(
            selectinload(PlayerSeasonStats.player),
            selectinload(PlayerSeasonStats.season),
        )
        .order_by(PlayerSeasonStats.elo.desc())
    )
    return session.scalars(stmt).all()


def update_season(
    session: Session,
    *,
    id: int,
    name: t.Optional[str] = None,
    description: t.Optional[str] = None,
    is_running: t.Optional[bool] = None,
) -> Season:
    season = get_season(session, id=id)
    if season is None:
        raise SeasonNotFound(id=id)

    if name is not None:
        season.name = name
    if description is not None:
        season.description = description
    if is_running is not None:
        season.is_running = is_running

    session.commit()

    return season
