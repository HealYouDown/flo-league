import typing as t


def calculate_elo(
    p1: int,
    p2: int,
    is_draw: bool = False,
    k: int = 50,
) -> t.Tuple[int, int]:
    """Returns the delta elo changes for P1 and

    Args:
        p1 (int): Winner ELO
        p2 (int): Loser ELO
        is_draw (bool, optional): Whether the match was a draw. Defaults to False.
        k (int, optional): Maximum change. Defaults to 50.

    Returns:
        t.Tuple[int, int]: P1 and P2 Delta
    """

    if is_draw:
        win = 0.5
        loss = 0.5
    else:
        win = 1
        loss = 0

    expected_score_player_1 = 1 / (1 + 10 ** ((p2 - p1) / 400))

    expected_score_player_2 = 1 / (1 + 10 ** ((p1 - p2) / 400))

    p1_delta = int(k * (win - expected_score_player_1))

    p2_delta = int(k * (loss - expected_score_player_2))

    return p1_delta, p2_delta
