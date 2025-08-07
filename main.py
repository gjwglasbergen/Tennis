from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from tennis import match


app = FastAPI()

dummy_db = [
    match.TennisMatch(
        "Govert Jan",
        "Nicolien",
        {
            "num_games_to_win": 6,
            "best_of_num_sets": 3,
            "whos_serve": "Govert Jan",
            "with_AD": True,
        },
    ),
    match.TennisMatch(
        "Jan",
        "Piet",
        {
            "num_games_to_win": 6,
            "best_of_num_sets": 3,
            "whos_serve": "Govert Jan",
            "with_AD": True,
        },
    ),
]


@app.get("/")
async def root():
    return {"message": "Welcome to the Tennis Match API!"}


@app.get("/matches")
async def get_matches():
    return jsonable_encoder(dummy_db)


@app.get("/matches/{match_id}")
async def get_match(match_id: int):
    if 0 <= match_id < len(dummy_db):
        return jsonable_encoder(dummy_db[match_id])
    return {"error": "Match not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
