from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.api.deps import get_db, require_user
from src.db.models import User
from src.enums import RoundStatus
from src.exceptions import ParticipantAlreadyAddedToRound, RoundNotFound
from src.schemas.players import PlayerRead
from src.schemas.rounds import RoundCreate, RoundRead, RoundUpdate
from src.services.round_service import (
    add_participant_to_round,
    create_round,
    delete_round,
    get_round,
    get_round_participants,
    get_rounds,
    remove_participant_from_round,
    update_round_status,
)

router = APIRouter(prefix="/rounds")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_round_route(
    data: RoundCreate,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> RoundRead:
    round = create_round(
        session, name=data.name, season_id=data.season_id, mode=data.mode
    )
    return RoundRead.model_validate(round)


@router.get("/")
async def get_rounds_route(
    status: list[RoundStatus] | None = Query(default=None),
    session: Session = Depends(get_db),
) -> list[RoundRead]:
    return [RoundRead.model_validate(obj) for obj in get_rounds(session, status=status)]


@router.get("/{round_id}")
async def get_round_route(
    round_id: int,
    session: Session = Depends(get_db),
) -> RoundRead:
    round = get_round(session, id=round_id)
    if round is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return RoundRead.model_validate(round)


@router.delete("/{round_id}")
async def delete_round_route(
    round_id: int,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> None:
    delete_round(session, round_id=round_id)


@router.post("/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_round_route(
    round_id: int,
    data: RoundUpdate,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> None:
    try:
        update_round_status(session, round_id=round_id, new_status=data.status)
    except RoundNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.get("/{round_id}/participants")
async def get_round_participants_route(
    round_id: int,
    session: Session = Depends(get_db),
) -> list[PlayerRead]:
    try:
        return [
            PlayerRead.model_validate(obj.player)
            for obj in get_round_participants(session, id=round_id)
        ]
    except RoundNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.put("/{round_id}/participants/{player_id}")
async def add_participant_route(
    round_id: int,
    player_id: int,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> list[PlayerRead]:
    try:
        add_participant_to_round(
            session,
            round_id=round_id,
            player_id=player_id,
        )
    except RoundNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    except ParticipantAlreadyAddedToRound:
        pass

    return [
        PlayerRead.model_validate(obj.player)
        for obj in get_round_participants(session, id=round_id)
    ]


@router.delete("/{round_id}/participants/{player_id}")
async def remove_participant_route(
    round_id: int,
    player_id: int,
    user: User = Depends(require_user),
    session: Session = Depends(get_db),
) -> list[PlayerRead]:
    try:
        remove_participant_from_round(
            session,
            round_id=round_id,
            player_id=player_id,
        )
    except RoundNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return [
        PlayerRead.model_validate(obj.player)
        for obj in get_round_participants(session, id=round_id)
    ]
