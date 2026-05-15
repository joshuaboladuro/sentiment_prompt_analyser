"""FastAPI server that exposes the sentiment analyser over HTTP.

Endpoints:
    GET  /          health check
    POST /analyse   accepts {"text": str}, returns {"label", "score", "text"}

Run locally:
    uvicorn api:app --reload --port 8000
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from sentiment import SentimentAnalyser, SentimentResult

app = FastAPI(title="Sentiment Prompt Analyser API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyser = SentimentAnalyser()


class AnalyseRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


class AnalyseResponse(BaseModel):
    text: str
    label: str
    score: float


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sentiment-prompt-analyser"}


@app.post("/analyse", response_model=AnalyseResponse)
def analyse(req: AnalyseRequest) -> AnalyseResponse:
    try:
        result: SentimentResult = analyser.analyse(req.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return AnalyseResponse(text=result.text, label=result.label, score=result.score)
