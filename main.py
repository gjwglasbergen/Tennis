from fastapi import FastAPI, HTTPException
from tennis.match import TennisMatch
from typing import Any, Dict
from models import *

app = FastAPI()


# --- Data opslag (in geheugen) ---
matches: Dict[int, TennisMatch] = {}
current_id = 1


# --- Endpoints ---


@app.post("/matches/create", status_code=201)
async def create_match(settings: TennisMatchSettings) -> dict[str, Any]:
    global current_id

    match_format = {
        "num_games_to_win": settings.num_games_to_win,
        "best_of_num_sets": settings.best_of_num_sets,
        "whos_serve": settings.whos_serve,
        "with_AD": settings.with_AD,
    }

    matches[current_id] = TennisMatch(
        player1=settings.player1, player2=settings.player2, matchFormat=match_format
    )

    match_id = current_id
    current_id += 1

    return {"match_id": match_id, "message": "Match created successfully"}


@app.get("/matches")
async def get_all_matches() -> dict[int, dict[str, Any]]:
    return {match_id: match.get_all_info() for match_id, match in matches.items()}


@app.get("/matches/{match_id}")
async def get_match(match_id: int) -> dict[str, Any]:
    if match_id not in matches:
        raise HTTPException(status_code=404, detail="Match does not exist")
    return matches[match_id].get_all_info()


@app.post("/matches/{match_id}/point")
async def make_point(match_id: int, point: PointRequest) -> dict[str, Any]:
    if match_id not in matches:
        raise HTTPException(status_code=404, detail="Match does not exist")

    match: TennisMatch = matches[match_id]

    # Validatie speler
    if point.player not in [match.player1, match.player2]:
        raise HTTPException(status_code=400, detail=f"Invalid player: {point.player}")

    try:
        match.win_point(player=point.player)
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid player name or internal error: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": f"{point.player} wins a point!",
        "current_game_score": match.gameScore,
        "current_set_score": match.setScore,
        "current_match_score": match.matchScore,
    }


@app.get("/matches/{match_id}/score", response_model=MatchScore)
async def get_score(match_id: int) -> MatchScore:
    if match_id not in matches:
        raise HTTPException(status_code=404, detail="Match does not exist")

    match: TennisMatch = matches[match_id]
    return MatchScore(game=match.gameScore, sets=match.setScore, match=match.matchScore)
