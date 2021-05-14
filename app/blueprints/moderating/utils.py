import typing

from app.extensions import db
from app.models import RunningMatch, RunningMatchParticipant


def delete_match(
    match_id: int,
    commit_db: bool = True,
) -> None:
    # Delete matches
    RunningMatch.query.filter(
        RunningMatch.id == match_id,
    ).delete()

    # Delete participants
    RunningMatchParticipant.query.filter(
        RunningMatchParticipant.match_id == match_id
    ).delete()

    if commit_db:
        db.session.commit()


def calculate_elo(
    player_1_points: int,
    player_2_points: int,
    draw: bool = False,
    k: int = 50,
) -> typing.Tuple[int, int]:
    """Returns elo changes for given players. player_1 is supposed
    to be the winner.
    As K is 50, maximum returned value is 50 and -50."""

    if draw:
        win = 0.5
        loss = 0.5
    else:
        win = 1
        loss = 0

    expected_score_player_1 = (
        1 / (1 + 10 ** ((player_2_points - player_1_points)/400)))

    expected_score_player_2 = (
        1 / (1 + 10 ** ((player_1_points - player_2_points)/400)))

    p1_points_change = int(k * (win - expected_score_player_1))

    p2_points_change = int(k * (loss - expected_score_player_2))

    return p1_points_change, p2_points_change
