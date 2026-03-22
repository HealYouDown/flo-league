from pydantic import BaseModel, ConfigDict

from src.enums import CharacterClass


class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    level_land: int
    level_sea: int
    character_class: CharacterClass
    is_female: bool
