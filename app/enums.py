import enum


class Server(enum.Enum):
    bergruen = "bergruen"
    luxplena = "luxplena"


class CharacterClass(enum.Enum):
    noble = "noble"
    magic_knight = "magic_knight"
    court_magician = "court_magician"

    saint = "saint"
    priest = "priest"
    shaman = "shaman"

    explorer = "explorer"
    sniper = "sniper"
    excavator = "excavator"

    mercenary = "mercenary"
    gladiator = "gladiator"
    guardian_swordsman = "guardian_swordsman"


class Winner(enum.Enum):
    draw = 0
    team_1 = 1
    team_2 = 2


class TeamSize(enum.Enum):
    one_vs_one = 1
    two_vs_two = 2
    three_vs_three = 3
