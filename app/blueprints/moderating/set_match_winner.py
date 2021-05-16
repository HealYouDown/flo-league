import typing

from app.blueprints.moderating.utils import calculate_elo
from app.constants import SEASON
from app.enums import Winner
from app.extensions import db
from app.models import (FinishedMatch, FinishedMatchParticipant, Player,
                        PlayerStatistics, RunningMatch)


def set_match_winner(
    match: RunningMatch,
    winner: Winner,
) -> None:
    # Create the match object which is permanently stored to database
    finished_match = FinishedMatch(
        server=match.server,
        winner=winner,
    )
    db.session.add(finished_match)
    db.session.flush()  # flush to get id of match

    team_1_players: typing.List[typing.Tuple[Player, PlayerStatistics]] = (
        db.session.query(
            Player, PlayerStatistics,
        ).join(
            PlayerStatistics,
        ).filter(
            Player.id.in_([rmp.player_id for rmp in match.team_1]),
            PlayerStatistics.season == SEASON,
        ).all()
    )

    team_2_players: typing.List[typing.Tuple[Player, PlayerStatistics]] = (
        db.session.query(
            Player, PlayerStatistics,
        ).join(
            PlayerStatistics,
        ).filter(
            Player.id.in_([rmp.player_id for rmp in match.team_2]),
            PlayerStatistics.season == SEASON,
        ).all()
    )

    team_1_points_avg = sum([
        statistics.points for _, statistics in team_1_players
    ]) // len(team_1_players)

    team_2_points_avg = sum([
        statistics.points for _, statistics in team_2_players
    ]) // len(team_2_players)

    if winner == Winner.team_1:
        team_1_change, team_2_change = calculate_elo(
            team_1_points_avg,
            team_2_points_avg,
            draw=False,
        )

        # Set wins / losses
        for _, statistics in team_1_players:
            statistics.wins += 1
        for _, statistics in team_2_players:
            statistics.losses += 1

    elif winner == Winner.team_2:
        team_2_change, team_1_change = calculate_elo(
            team_2_points_avg,
            team_1_points_avg,
            draw=False,
        )

        # Set wins / losses
        for _, statistics in team_1_players:
            statistics.losses += 1
        for _, statistics in team_2_players:
            statistics.wins += 1

    elif winner == Winner.draw:
        team_1_change, team_2_change = calculate_elo(
            team_1_points_avg,
            team_2_points_avg,
            draw=True,
        )

        # Set draws
        for _, statistics in team_1_players:
            statistics.draws += 1
        for _, statistics in team_2_players:
            statistics.draws += 1

    # Create finished match participants
    # Team 1
    for player, statistics in team_1_players:
        db.session.add(FinishedMatchParticipant(
            match_id=finished_match.id,
            team=0,
            points_before=statistics.points,
            points_after=statistics.points + team_1_change,
            player_id=player.id,
            username=player.username,
            character_class=player.character_class,
            level_land=player.level_land,
            level_sea=player.level_sea,
        ))

    # Team 2
    for player, statistics in team_2_players:
        db.session.add(FinishedMatchParticipant(
            match_id=finished_match.id,
            team=1,
            points_before=statistics.points,
            points_after=statistics.points + team_2_change,
            player_id=player.id,
            username=player.username,
            character_class=player.character_class,
            level_land=player.level_land,
            level_sea=player.level_sea,
        ))

    # Update points
    for _, statistics in team_1_players:
        statistics.points = statistics.points + team_1_change
    for _, statistics in team_2_players:
        statistics.points = statistics.points + team_2_change

    db.session.commit()
