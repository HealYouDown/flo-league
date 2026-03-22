from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.deps import get_db, require_admin, require_user
from src.db.models import User
from src.exceptions import SeasonNotFound
from src.schemas.rounds import RoundRead
from src.schemas.seasons import (
    SeasonCreate,
    SeasonPlayerStatsRead,
    SeasonRead,
    SeasonUpdate,
)
from src.services.round_service import get_season_rounds
from src.services.season_service import (
    create_season,
    delete_season,
    get_season,
    get_season_leaderboard,
    get_seasons,
    update_season,
)

router = APIRouter(prefix="/seasons")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_season_route(
    data: SeasonCreate,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> SeasonRead:
    season = create_season(session, name=data.name, description=data.description)
    return SeasonRead.model_validate(season)


@router.get("/")
async def get_seasons_route(
    session: Session = Depends(get_db),
) -> list[SeasonRead]:
    return [SeasonRead.model_validate(obj) for obj in get_seasons(session)]


@router.get("/{id}")
async def get_season_route(
    id: int,
    session: Session = Depends(get_db),
) -> SeasonRead:
    season = get_season(session, id=id)
    session.delete(season)
    if season is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return SeasonRead.model_validate(season)


@router.delete("/{id}")
async def delete_season_route(
    id: int,
    user: User = Depends(require_admin),
    session: Session = Depends(get_db),
) -> None:
    delete_season(session, id=id)


@router.get("/{id}/leaderboard")
async def get_season_leaderboard_route(
    id: int,
    session: Session = Depends(get_db),
) -> list[SeasonPlayerStatsRead]:
    return [
        SeasonPlayerStatsRead.model_validate(obj)
        for obj in get_season_leaderboard(session, id=id)
    ]


@router.get("/{id}/rounds")
async def get_season_rounds_route(
    id: int,
    session: Session = Depends(get_db),
) -> list[RoundRead]:
    return [
        RoundRead.model_validate(obj)
        for obj in get_season_rounds(session, season_id=id)
    ]


@router.patch("/{id}")
async def patch_season_route(
    id: int,
    data: SeasonUpdate,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> SeasonRead:
    try:
        season = update_season(
            session,
            id=id,
            name=data.name,
            description=data.description,
            is_running=data.is_running,
        )
        return SeasonRead.model_validate(season)
    except SeasonNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
