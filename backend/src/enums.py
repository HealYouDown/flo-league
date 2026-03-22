import enum


class CharacterClass(enum.IntEnum):
    MERCENARY = 0
    EXPLORER = 2
    NOBLE = 3
    SAINT = 4

    GLADIATOR = 5
    GUARDIAN_SWORDSMAN = 6

    EXCAVATOR = 7
    SNIPER = 8

    COURT_MAGICIAN = 9
    MAGIC_KNIGHT = 10

    PRIEST = 11
    SHAMAN = 12

    @property
    def base_class(self) -> "CharacterClass":
        return {
            CharacterClass.MERCENARY: CharacterClass.MERCENARY,
            CharacterClass.GUARDIAN_SWORDSMAN: CharacterClass.MERCENARY,
            CharacterClass.GLADIATOR: CharacterClass.MERCENARY,
            CharacterClass.EXPLORER: CharacterClass.EXPLORER,
            CharacterClass.EXCAVATOR: CharacterClass.EXPLORER,
            CharacterClass.SNIPER: CharacterClass.EXPLORER,
            CharacterClass.NOBLE: CharacterClass.NOBLE,
            CharacterClass.MAGIC_KNIGHT: CharacterClass.NOBLE,
            CharacterClass.COURT_MAGICIAN: CharacterClass.NOBLE,
            CharacterClass.SAINT: CharacterClass.SAINT,
            CharacterClass.PRIEST: CharacterClass.SAINT,
            CharacterClass.SHAMAN: CharacterClass.SAINT,
        }[self]


class RoundMode(enum.IntEnum):
    ONE_VS_ONE = enum.auto()
    TWO_VS_TWO = enum.auto()
    THREE_VS_THREE = enum.auto()
    FOUR_VS_FOUR = enum.auto()
    FIVE_VS_FIVE = enum.auto()
    SIX_VS_SIX = enum.auto()

    @property
    def team_size(self) -> int:
        return {
            RoundMode.ONE_VS_ONE: 1,
            RoundMode.TWO_VS_TWO: 2,
            RoundMode.THREE_VS_THREE: 3,
            RoundMode.FOUR_VS_FOUR: 4,
            RoundMode.FIVE_VS_FIVE: 5,
            RoundMode.SIX_VS_SIX: 6,
        }[self]


class RoundStatus(enum.IntEnum):
    DRAFT = enum.auto()
    RUNNING = enum.auto()
    COMPLETED = enum.auto()


class MatchResult(enum.IntEnum):
    UNSET = enum.auto()
    CANCELED = enum.auto()
    WIN_TEAM_1 = enum.auto()
    WIN_TEAM_2 = enum.auto()
    DRAW = enum.auto()
