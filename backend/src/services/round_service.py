import typing as t

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from src.db.models import Round, RoundParticipant
from src.enums import MatchResult, RoundMode, RoundStatus
from src.exceptions import (
    InvalidRoundStatus,
    ParticipantAlreadyAddedToRound,
    PlayerNotFound,
    RoundCannotBeEditedAnymore,
    RoundNotFound,
    SeasonCannotBeEditedAnymore,
    SeasonNotFound,
)

from .player_service import get_player
from .season_service import get_season


def create_round(
    session: Session,
    *,
    name: str,
    mode: RoundMode,
    season_id: t.Optional[int] = None,
) -> Round:
    if season_id is not None:
        season = get_season(session, id=season_id)
        if season is None:
            raise SeasonNotFound(id=season_id)
        if not season.is_running:
            raise SeasonCannotBeEditedAnymore(season_id=season_id)

    round = Round(season_id=season_id, name=name, mode=mode, status=RoundStatus.DRAFT)
    session.add(round)
    session.commit()

    return round


def delete_round(session: Session, round_id: int) -> None:
    round = get_round(session, id=round_id)
    if round is None:
        return

    if round.status == RoundStatus.COMPLETED:
        raise RoundCannotBeEditedAnymore(round_id=round_id)

    session.delete(round)
    session.commit()


def update_round_status(
    session: Session, round_id: int, new_status: RoundStatus
) -> None:
    from .match_service import create_matches, get_matches, set_match_result

    round = get_round(session, id=round_id)
    if round is None:
        raise RoundNotFound(id=round_id)

    if round.status == RoundStatus.COMPLETED:
        raise RoundCannotBeEditedAnymore(round_id=round_id)

    if round.status == RoundStatus.DRAFT and new_status == RoundStatus.RUNNING:
        create_matches(session, round_id=round_id)
        round.status = new_status
        session.commit()
        return

    if round.status == RoundStatus.RUNNING and new_status == RoundStatus.COMPLETED:
        # Closes all remaining matches
        matches = get_matches(session, round_id=round_id)
        for match in matches:
            if match.match_result == MatchResult.UNSET:
                set_match_result(
                    session, match_id=match.id, result=MatchResult.CANCELED
                )

        round.status = new_status
        session.commit()
        return

    raise InvalidRoundStatus()


def get_rounds(
    session: Session, *, status: list[RoundStatus] | None = None
) -> t.Sequence[Round]:
    stmt = select(Round)

    if status:
        stmt = stmt.where(Round.status.in_(status))

    return session.scalars(stmt).all()


def get_season_rounds(session: Session, season_id: int) -> t.Sequence[Round]:
    stmt = select(Round).where(Round.season_id == season_id)
    return session.scalars(stmt).all()


def get_round(session: Session, *, id: int) -> t.Optional[Round]:
    stmt = select(Round).where(Round.id == id)
    return session.scalar(stmt)


def get_round_participants(
    session: Session, *, id: int
) -> t.Sequence[RoundParticipant]:
    stmt = (
        select(RoundParticipant)
        .where(RoundParticipant.round_id == id)
        .options(joinedload(RoundParticipant.player))
    )
    return session.scalars(stmt).all()


def add_participant_to_round(
    session: Session,
    *,
    round_id: int,
    player_id: int,
) -> RoundParticipant:
    round = get_round(session, id=round_id)
    if round is None:
        raise RoundNotFound(id=round_id)

    if round.status != RoundStatus.DRAFT:
        raise RoundCannotBeEditedAnymore(round_id=round_id)

    player = get_player(session, id=player_id)
    if player is None:
        raise PlayerNotFound(id=player_id)
    if not player.is_active:
        raise PlayerNotFound(id=player_id)

    participant = RoundParticipant(player_id=player_id)

    # The player might already be part of the round
    # Checking manually might result in race conditions, so we just
    # try to add the player and let the database handle violations
    try:
        round.participants.append(participant)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ParticipantAlreadyAddedToRound(player_id=player_id, round_id=round_id)

    return participant


def remove_participant_from_round(
    session: Session,
    *,
    round_id: int,
    player_id: int,
) -> None:
    round = get_round(session, id=round_id)
    if round is None:
        raise RoundNotFound(id=round_id)

    if round.status != RoundStatus.DRAFT:
        raise RoundCannotBeEditedAnymore(round_id=round_id)

    stmt = select(RoundParticipant).where(
        RoundParticipant.player_id == player_id, RoundParticipant.round_id == round_id
    )
    participant = session.scalar(stmt)
    if participant is not None:
        session.delete(participant)
        session.commit()
