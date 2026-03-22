import typing as t

from pydantic import BaseModel, ConfigDict

from src.enums import CharacterClass, MatchResult


class MatchParticipant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: int
    name: str
    level_land: int
    level_sea: int
    character_class: CharacterClass
    is_female: bool

    elo_before: t.Optional[int]
    elo_change: t.Optional[int]


class MatchTeam(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    members: list[MatchParticipant]


class MatchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    round_id: int

    team_1: MatchTeam
    team_2: MatchTeam

    match_result: MatchResult


class MatchUpdate(BaseModel):
    result: MatchResult
