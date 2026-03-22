class PlayerNotFound(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Player with {id=} not found")


class SeasonNotFound(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Season with {id=} not found")


class RoundNotFound(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Round with {id=} not found")


class ParticipantAlreadyAddedToRound(Exception):
    def __init__(self, player_id: int, round_id: int):
        self.id = id
        super().__init__(f"Player with {player_id=} already part of {round_id=}")


class RoundCannotBeEditedAnymore(Exception):
    def __init__(self, round_id: int):
        self.id = id
        super().__init__(f"Round with {round_id=} cannot be edited anymore")


class SeasonCannotBeEditedAnymore(Exception):
    def __init__(self, season_id: int):
        self.id = id
        super().__init__(f"Season with {season_id=} cannot be edited anymore")


class InvalidRoundStatus(Exception):
    pass


class UnableToCreateMatches(Exception):
    pass


class MatchNotFound(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Match with {id=} not found")


class MatchAlreadyConcluded(Exception):
    def __init__(self, id: int):
        self.id = id
        super().__init__(f"Match with {id} is already concluded")
