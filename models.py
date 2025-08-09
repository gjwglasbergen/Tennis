from pydantic import BaseModel, Field
from typing import Any, Dict


# --- Pydantic modellen ---
class TennisMatchSettings(BaseModel):
    player1: str = Field(..., description="Naam van speler 1")
    player2: str = Field(..., description="Naam van speler 2")
    num_games_to_win: int = Field(6, description="Aantal games om te winnen")
    best_of_num_sets: int = Field(3, description="Aantal sets om te winnen")
    whos_serve: str = Field(..., description="Wie serveert")
    with_AD: bool = Field(True, description="Speel met advantage (AD) of niet")


class PointRequest(BaseModel):
    player: str = Field(..., description="Naam van speler die het punt wint")


class MatchScore(BaseModel):
    game: Dict[str, int]
    sets: Dict[str, int]
    match: Dict[str, int]
