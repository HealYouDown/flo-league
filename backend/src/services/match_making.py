import random

from src.db.models import Player
from src.enums import RoundMode
from src.exceptions import UnableToCreateMatches


def fill_team(team: list[Player], pool: list[Player], team_size: int) -> None:
    """
    Fill `team` up to `team_size` by selecting from `pool`,
    preferring players with unique base_class.
    Selected players are removed from `pool`.
    """
    while len(team) < team_size:
        existing_classes = {p.character_class.base_class for p in team}
        candidates = [
            p for p in pool if p.character_class.base_class not in existing_classes
        ]

        if not candidates:
            candidates = pool  # fallback if diversity impossible

        chosen = random.choice(candidates)
        team.append(chosen)
        pool.remove(chosen)


def match_players(
    players: list[Player], mode: RoundMode
) -> list[tuple[tuple[Player, ...], tuple[Player, ...]]]:
    team_size = mode.team_size

    if len(players) < (team_size * 2):
        raise UnableToCreateMatches(
            f"Not enough players for {mode!r}, got {len(players)}"
        )

    matches: list[tuple[tuple[Player, ...], tuple[Player, ...]]] = []

    players_to_match = players[:]
    random.shuffle(players_to_match)

    if mode.team_size == 1:
        # An uneven amount of players means that someone has to fight twice
        # We have to be careful to not match the last player with itself
        if len(players) % 2 != 0:
            players_to_match.append(
                random.choice([p for p in players if p != players[-1]])
            )
        matches.extend(
            [
                ((players_to_match[i],), (players_to_match[i + 1],))
                for i in range(0, len(players_to_match), 2)
            ]
        )

    else:
        # Team size > 1
        # We try to diversify the matches by trying to not put
        # the same base class in a team
        total_per_match = team_size * 2

        while len(players_to_match) >= total_per_match:
            team_a: list[Player] = []
            team_b: list[Player] = []

            fill_team(team_a, players_to_match, team_size)
            fill_team(team_b, players_to_match, team_size)

            matches.append((tuple(team_a), tuple(team_b)))

        # leftover players will be put into a match with other players, that have
        # to play twice
        if players_to_match:
            leftover_players = players_to_match
            reusable_players = [p for p in players if p not in leftover_players]
            random.shuffle(reusable_players)

            count_leftovers = len(leftover_players)
            team_a = leftover_players[: count_leftovers // 2]
            team_b = leftover_players[count_leftovers // 2 :]

            fill_team(team_a, reusable_players, team_size)
            fill_team(team_b, reusable_players, team_size)

            matches.append((tuple(team_a), tuple(team_b)))

    return matches
