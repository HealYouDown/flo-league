import os
import random
import typing as t

from sqlalchemy.orm import Session

from src.db.models import Player, Round, RoundMatch, RoundParticipant, Season
from src.enums import CharacterClass, RoundMode, RoundStatus
from src.services.match_service import create_matches


def seed_season(
    session: Session,
) -> Season:
    season = Season(name="Season")
    session.add(season)
    session.flush()
    return season


def seed_round(
    session: Session,
    *,
    season_id: t.Optional[int] = None,
    mode: RoundMode = RoundMode.ONE_VS_ONE,
    status: RoundStatus = RoundStatus.DRAFT,
) -> Round:
    round = Round(name="Round Name", season_id=season_id, mode=mode, status=status)
    session.add(round)
    session.flush()
    return round


def seed_player(session: Session) -> Player:
    return seed_players(session, count=1)[0]


def seed_players(session: Session, *, count: int) -> list[Player]:
    player_data = [
        {
            "id": i,
            "name": os.urandom(12).hex(),
            "level_land": random.randint(1, 120),
            "level_sea": random.randint(1, 99),
            "character_class": random.choice(list(CharacterClass)),
            "is_female": random.choice([True, False]),
            "is_active": True,
        }
        for i in range(1, count + 1)
    ]
    players = [Player(**p) for p in player_data]
    session.add_all(players)
    session.flush()
    return players


def seed_round_with_players(
    session: Session,
    players: list[Player],
    round_args: t.Optional[dict] = None,
) -> Round:
    round = seed_round(session, **(round_args or {}))
    for player in players:
        participant = RoundParticipant(player_id=player.id)
        round.participants.append(participant)
    session.flush()
    return round


def seed_round_with_matches(
    session: Session,
    players: list[Player],
    round_args: t.Optional[dict] = None,
) -> tuple[Round, list[RoundMatch]]:
    round = seed_round_with_players(session, players=players, round_args=round_args)
    # FIXME: Technically it's bad to use our service function for seeding, but I really don't
    # want to duplicate all that logic..
    matches = create_matches(session, round_id=round.id)
    round.status = RoundStatus.RUNNING
    session.flush()

    return round, matches
