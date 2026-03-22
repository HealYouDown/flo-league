import typing as t

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.db.models import (
    Player,
    PlayerSeasonStats,
    Round,
    RoundMatch,
    RoundMatchParticipant,
    RoundMatchTeam,
)
from src.enums import MatchResult, RoundStatus
from src.exceptions import MatchAlreadyConcluded, MatchNotFound, RoundNotFound

from .elo import calculate_elo
from .match_making import match_players
from .round_service import get_round, get_round_participants


def get_matches(session: Session, round_id: int) -> t.Sequence[RoundMatch]:
    stmt = (
        select(RoundMatch)
        .where(RoundMatch.round_id == round_id)
        .options(
            joinedload(RoundMatch.team_1).options(joinedload(RoundMatchTeam.members))
        )
        .options(
            joinedload(RoundMatch.team_2).options(joinedload(RoundMatchTeam.members))
        )
    )
    return session.scalars(stmt).unique().all()


def get_match(session: Session, match_id: int) -> RoundMatch | None:
    stmt = (
        select(RoundMatch)
        .where(RoundMatch.id == match_id)
        .options(joinedload(RoundMatch.round).options(joinedload(Round.season)))
        .options(
            joinedload(RoundMatch.team_1).options(joinedload(RoundMatchTeam.members))
        )
        .options(
            joinedload(RoundMatch.team_2).options(joinedload(RoundMatchTeam.members))
        )
    )
    return session.scalar(stmt)


def create_matches(session: Session, *, round_id: int):
    round = get_round(session, id=round_id)
    if round is None:
        raise RoundNotFound(id=round_id)
    if round.status != RoundStatus.DRAFT:
        raise Exception()  # TODO

    players = [p.player for p in get_round_participants(session, id=round_id)]
    matchups = match_players(players, round.mode)

    matches: list[RoundMatch] = []

    def create_team(players: t.Iterable[Player]) -> RoundMatchTeam:
        team = RoundMatchTeam()
        for p in players:
            team.members.append(
                RoundMatchParticipant(
                    player_id=p.id,
                    name=p.name,
                    level_land=p.level_land,
                    level_sea=p.level_sea,
                    character_class=p.character_class,
                    is_female=p.is_female,
                )
            )
        return team

    for team1_players, team2_players in matchups:
        team1 = create_team(team1_players)
        team2 = create_team(team2_players)

        session.add_all([team1, team2])
        session.flush()

        session.flush()

        match = RoundMatch(
            round_id=round_id,
            team_1_id=team1.id,
            team_2_id=team2.id,
        )
        matches.append(match)

    session.add_all(matches)
    session.commit()

    return matches


def get_or_create_season_stats(
    session: Session, player_id: int, season_id: int
) -> PlayerSeasonStats:
    stmt = select(PlayerSeasonStats).where(
        PlayerSeasonStats.player_id == player_id,
        PlayerSeasonStats.season_id == season_id,
    )
    stats = session.scalar(stmt)

    if stats is None:
        stats = PlayerSeasonStats(player_id=player_id, season_id=season_id)
        session.add(stats)
        session.flush()

    return stats


def set_match_result(session: Session, *, match_id: int, result: MatchResult) -> None:
    match = get_match(session, match_id=match_id)
    if match is None:
        raise MatchNotFound(id=match_id)

    if match.match_result != MatchResult.UNSET:
        raise MatchAlreadyConcluded(id=match_id)

    if result == MatchResult.UNSET:
        raise ValueError("Match cannot be set to unset")

    season = match.round.season
    has_effect_on_elo = season is not None

    match.match_result = result

    if has_effect_on_elo:
        assert season is not None
        team_1_players = match.team_1.members
        team_2_players = match.team_2.members

        team_1_stats = [
            get_or_create_season_stats(
                session,
                player_id=p.player_id,
                season_id=season.id,
            )
            for p in team_1_players
        ]
        team_2_stats = [
            get_or_create_season_stats(
                session,
                player_id=p.player_id,
                season_id=season.id,
            )
            for p in team_2_players
        ]

        team_1_elo = sum(s.elo for s in team_1_stats) // len(team_1_stats)
        team_2_elo = sum(s.elo for s in team_2_stats) // len(team_2_stats)

        if result == MatchResult.WIN_TEAM_1:
            p1_change, p2_change = calculate_elo(team_1_elo, team_2_elo)
        elif result == MatchResult.WIN_TEAM_2:
            p2_change, p1_change = calculate_elo(team_2_elo, team_1_elo)
        elif result == MatchResult.DRAW:
            p1_change, p2_change = calculate_elo(team_1_elo, team_2_elo, is_draw=True)
        elif result == MatchResult.CANCELED:
            p1_change = p2_change = 0

        for s in team_1_stats:
            p = next(p for p in team_1_players if p.player_id == s.player_id)
            p.elo_before = s.elo
            p.elo_change = p1_change

            s.elo += p1_change
            if result == MatchResult.WIN_TEAM_1:
                s.wins += 1
            elif result == MatchResult.WIN_TEAM_2:
                s.losses += 1
            elif result == MatchResult.DRAW:
                s.draws += 1

        for s in team_2_stats:
            p = next(p for p in team_2_players if p.player_id == s.player_id)
            p.elo_before = s.elo
            p.elo_change = p2_change

            s.elo += p2_change
            if result == MatchResult.WIN_TEAM_1:
                s.losses += 1
            elif result == MatchResult.WIN_TEAM_2:
                s.wins += 1
            elif result == MatchResult.DRAW:
                s.draws += 1

    # Check if all matches have a result, which then closes the round
    matches = get_matches(session, round_id=match.round_id)
    unset_matches = [m for m in matches if m.match_result == MatchResult.UNSET]
    all_matches_done = len(unset_matches) == 0
    if all_matches_done:
        round = match.round
        round.status = RoundStatus.COMPLETED

    session.commit()
