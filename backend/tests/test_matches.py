from sqlalchemy.orm import Session

from src.enums import MatchResult, RoundMode
from src.services.match_service import create_matches, set_match_result
from tests.seeds import (
    seed_players,
    seed_round_with_matches,
    seed_round_with_players,
    seed_season,
)


def test_matchmaking_1v1(session: Session):
    players = seed_players(session, count=10)
    round = seed_round_with_players(session, players=players)

    matches = create_matches(session, round_id=round.id)

    assert len(matches) == 5

    # Check that all players are present
    flattened_match_participant_ids = []
    for match in matches:
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_1.members]
        )
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_2.members]
        )
    assert len(flattened_match_participant_ids) == 10

    assert all(p.id in flattened_match_participant_ids for p in players)


def test_matchmaking_1v1_uneven(session: Session):
    players = seed_players(session, count=9)
    round = seed_round_with_players(session, players=players)

    matches = create_matches(session, round_id=round.id)

    assert len(matches) == 5

    # Check that all players are present
    flattened_match_participant_ids = []
    for match in matches:
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_1.members]
        )
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_2.members]
        )
    assert len(flattened_match_participant_ids) == 10
    assert len(set(flattened_match_participant_ids)) == 9

    assert all(p.id in flattened_match_participant_ids for p in players)


def test_matchmaking_6v6(session: Session):
    players = seed_players(session, count=12)
    round = seed_round_with_players(
        session, players=players, round_args={"mode": RoundMode.SIX_VS_SIX}
    )

    matches = create_matches(session, round_id=round.id)

    assert len(matches) == 1

    # Check that all players are present
    flattened_match_participant_ids = []
    for match in matches:
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_1.members]
        )
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_2.members]
        )
    assert len(flattened_match_participant_ids) == 12

    assert all(p.id in flattened_match_participant_ids for p in players)


def test_matchmaking_6v6_uneven(session: Session):
    players = seed_players(session, count=13)
    round = seed_round_with_players(
        session, players=players, round_args={"mode": RoundMode.SIX_VS_SIX}
    )

    matches = create_matches(session, round_id=round.id)

    assert len(matches) == 2

    # Check that all players are present
    flattened_match_participant_ids = []
    for match in matches:
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_1.members]
        )
        flattened_match_participant_ids.extend(
            [p.player_id for p in match.team_2.members]
        )
    assert len(flattened_match_participant_ids) == 24

    assert all(p.id in flattened_match_participant_ids for p in players)


def test_match_result_team_1_win(session: Session):
    season = seed_season(session)
    players = seed_players(session, count=2)
    round, matches = seed_round_with_matches(
        session,
        players,
        round_args={"season_id": season.id},
    )
    assert len(matches) == 1
    match = matches[0]

    set_match_result(session, match_id=match.id, result=MatchResult.WIN_TEAM_1)
    assert match.match_result == MatchResult.WIN_TEAM_1

    assert (
        match.team_1.members[0].elo_before is not None
        and match.team_1.members[0].elo_before == 1000
    )
    assert (
        match.team_1.members[0].elo_change is not None
        and match.team_1.members[0].elo_change > 0
    )

    assert (
        match.team_2.members[0].elo_before is not None
        and match.team_2.members[0].elo_before == 1000
    )
    assert (
        match.team_2.members[0].elo_change is not None
        and match.team_2.members[0].elo_change < 0
    )


def test_match_result_team_2_win(session: Session):
    season = seed_season(session)
    players = seed_players(session, count=2)
    round, matches = seed_round_with_matches(
        session,
        players,
        round_args={"season_id": season.id},
    )
    assert len(matches) == 1
    match = matches[0]

    set_match_result(session, match_id=match.id, result=MatchResult.WIN_TEAM_2)
    assert match.match_result == MatchResult.WIN_TEAM_2

    assert (
        match.team_1.members[0].elo_before is not None
        and match.team_1.members[0].elo_before == 1000
    )
    assert (
        match.team_1.members[0].elo_change is not None
        and match.team_1.members[0].elo_change < 0
    )

    assert (
        match.team_2.members[0].elo_before is not None
        and match.team_2.members[0].elo_before == 1000
    )
    assert (
        match.team_2.members[0].elo_change is not None
        and match.team_2.members[0].elo_change > 0
    )


def test_match_result_draw(session: Session):
    season = seed_season(session)
    players = seed_players(session, count=2)
    round, matches = seed_round_with_matches(
        session,
        players,
        round_args={"season_id": season.id},
    )
    assert len(matches) == 1
    match = matches[0]

    set_match_result(session, match_id=match.id, result=MatchResult.DRAW)
    assert match.match_result == MatchResult.DRAW

    assert (
        match.team_1.members[0].elo_before is not None
        and match.team_1.members[0].elo_before == 1000
    )
    assert (
        match.team_1.members[0].elo_change is not None
        and match.team_1.members[0].elo_change == 0
    )

    assert (
        match.team_2.members[0].elo_before is not None
        and match.team_2.members[0].elo_before == 1000
    )
    assert (
        match.team_2.members[0].elo_change is not None
        and match.team_2.members[0].elo_change == 0
    )
