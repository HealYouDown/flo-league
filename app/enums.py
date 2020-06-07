from enum import Enum


class ServerEnum(Enum):
    bergruen = "Bergruen"
    luxplena = "LuxPlena"


class CharacterClassEnum(Enum):
    noble = "Noble"
    magic_knight = "Magic Knight"
    court_magician = "Court Magician"

    explorer = "Explorer"
    sniper = "Sniper"
    excavator = "Excavator"

    saint = "Saint"
    shaman = "Shaman"
    priest = "Priest"

    mercenary = "Mercenary"
    guardian_swordsman = "Guardian Swordsman"
    gladiator = "Gladiator"


class MatchWinnerEnum(Enum):
    player_1 = 0
    player_2 = 1
    draw = 2
