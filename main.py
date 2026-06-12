"""FastAPI server — serves the Snake Game frontend and leaderboard API."""

import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from history import GameHistoryManager

app = FastAPI(
    title="Snake Game API",
    description=(
        "REST API for the Snake Game leaderboard.\n\n"
        "- **GET /api/scores** — retrieve the top scores, sorted highest first\n"
        "- **POST /api/scores** — submit a score after a game session\n\n"
        "Play the game at [`/`](/)."
    ),
    version="1.0.0",
    contact={"name": "Snake Game"},
    license_info={"name": "MIT"},
)

_history = GameHistoryManager()


# ── Schemas ───────────────────────────────────────────────────────────────────

class ScoreIn(BaseModel):
    name:  str = Field(..., min_length=1, max_length=14, examples=["Player1"])
    score: int = Field(..., ge=0, examples=[120])

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip() or "Anonymous"


class ScoreRecord(BaseModel):
    name:      str = Field(..., examples=["Player1"])
    score:     int = Field(..., examples=[120])
    timestamp: str = Field(..., examples=["2026-06-12 14:30:00"])


class SubmitResponse(BaseModel):
    ok: bool = Field(..., examples=[True])


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get(
    "/api/scores",
    response_model=List[ScoreRecord],
    summary="Get leaderboard",
    description="Returns up to all saved scores, sorted by score descending.",
    tags=["Leaderboard"],
)
def get_scores():
    return _history.load_history()


@app.post(
    "/api/scores",
    response_model=SubmitResponse,
    summary="Submit a score",
    description="Save a player's score. Name is trimmed; blank names become `Anonymous`.",
    status_code=201,
    tags=["Leaderboard"],
)
def post_score(body: ScoreIn):
    _history.save_record(body.name, body.score)
    return {"ok": True}


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(os.path.join("static", "index.html"))


app.mount("/static", StaticFiles(directory="static"), name="static")
