import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import RoundMatch, RoundParticipant, Season
from src.enums import MatchResult, RoundMode, RoundStatus
from src.exceptions import (
    ParticipantAlreadyAddedToRound,
    PlayerNotFound,
    RoundCannotBeEditedAnymore,
    RoundNotFound,
    SeasonCannotBeEditedAnymore,
    SeasonNotFound,
)
from src.services.round_service import (
    add_participant_to_round,
    create_round,
    remove_participant_from_round,
    update_round_status,
)
from tests.seeds import (
    seed_player,
    seed_players,
    seed_round,
    seed_round_with_matches,
    seed_round_with_players,
)


def test_create_round_without_season(session: Session):
    round = create_round(session, name="Test", mode=RoundMode.ONE_VS_ONE)
    assert round.id == 1
    assert round.season_id is None


def test_create_round_with_season(session: Session):
    season = Season(name="Test Season")
    session.add(season)
    session.flush()

    round = create_round(
        session,
        name="Test",
        mode=RoundMode.ONE_VS_ONE,
        season_id=season.id,
    )
    assert round.id == 1
    assert round.season_id is season.id


def test_create_round_with_inactive_season(session: Session):
    season = Season(name="Test Season")
    season.is_running = False
    session.add(season)
    session.flush()

    with pytest.raises(SeasonCannotBeEditedAnymore):
        create_round(
            session,
            name="Test",
            mode=RoundMode.ONE_VS_ONE,
            season_id=season.id,
        )


def test_create_round_with_non_existing_season(session: Session):
    with pytest.raises(SeasonNotFound):
        create_round(
            session,
            name="Test",
            mode=RoundMode.ONE_VS_ONE,
            season_id=69,
        )


def test_add_round_participant(session: Session):
    round = seed_round(session)
    player = seed_player(session)

    add_participant_to_round(session, round_id=round.id, player_id=player.id)
    assert len(session.scalars(select(RoundParticipant)).all()) == 1


def test_add_round_participant_multiple_times(session: Session):
    round = seed_round(session)
    player = seed_player(session)

    add_participant_to_round(session, round_id=round.id, player_id=player.id)
    assert len(session.scalars(select(RoundParticipant)).all()) == 1

    # If we add the same player a second time, it should still be only one

    with pytest.raises(ParticipantAlreadyAddedToRound):
        add_participant_to_round(session, round_id=round.id, player_id=player.id)
    assert len(session.scalars(select(RoundParticipant)).all()) == 1


def test_add_round_participant_not_existing(session: Session):
    round = seed_round(session)
    with pytest.raises(PlayerNotFound):
        add_participant_to_round(session, round_id=round.id, player_id=1)


def test_add_round_participant_not_existing_round(session: Session):
    player = seed_player(session)

    with pytest.raises(RoundNotFound):
        add_participant_to_round(session, round_id=1, player_id=player.id)


def test_add_round_participant_to_non_draft_round(session: Session):
    round = seed_round(session, status=RoundStatus.RUNNING)
    player = seed_player(session)

    with pytest.raises(RoundCannotBeEditedAnymore):
        add_participant_to_round(session, round_id=round.id, player_id=player.id)


def test_remove_round_participant(session: Session):
    player = seed_player(session)
    round = seed_round_with_players(session, players=[player])

    assert len(session.scalars(select(RoundParticipant)).all()) == 1
    remove_participant_from_round(session, round_id=round.id, player_id=player.id)
    assert len(session.scalars(select(RoundParticipant)).all()) == 0


def test_remove_round_participant_from_non_draft_round(session: Session):
    player = seed_player(session)
    round = seed_round_with_players(session, players=[player])
    round.status = RoundStatus.RUNNING
    session.flush()

    with pytest.raises(RoundCannotBeEditedAnymore):
        assert len(session.scalars(select(RoundParticipant)).all()) == 1
        remove_participant_from_round(session, round_id=round.id, player_id=player.id)


def test_update_round_status_draft_to_running(session: Session):
    players = seed_players(session, count=10)
    round = seed_round_with_players(session, players=players)

    update_round_status(session, round_id=round.id, new_status=RoundStatus.RUNNING)

    assert round.status == RoundStatus.RUNNING
    # As a side effect, we should now have matches
    assert len(session.scalars(select(RoundMatch)).all()) > 0


def test_update_round_status_running_to_completed(session: Session):
    players = seed_players(session, count=10)
    round, matches = seed_round_with_matches(session, players=players)

    update_round_status(session, round_id=round.id, new_status=RoundStatus.COMPLETED)

    assert round.status == RoundStatus.COMPLETED
    # If no match status was set, all matches should now be CANCELED
    assert all(m.match_result == MatchResult.CANCELED for m in matches)
