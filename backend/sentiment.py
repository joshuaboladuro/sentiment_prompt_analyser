"""Sentiment analyser backed by a pre-trained transformer.

Wraps a Hugging Face pipeline and returns a structured ``SentimentResult``
with a 3-class label (positive, neutral, negative) and a confidence score.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from transformers import pipeline

Sentiment = Literal["positive", "negative", "neutral"]
DEFAULT_MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"

_LABEL_MAP: dict[str, Sentiment] = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
    "negative": "negative",
    "neutral": "neutral",
    "positive": "positive",
}


@dataclass(frozen=True)
class SentimentResult:
    text: str
    label: Sentiment
    score: float


class SentimentAnalyser:
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self._pipe = pipeline("sentiment-analysis", model=model_name, top_k=None)

    def analyse(self, text: str) -> SentimentResult:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        raw = self._pipe(text)[0]
        top = max(raw, key=lambda r: r["score"])
        label = _LABEL_MAP.get(top["label"], top["label"].lower())
        return SentimentResult(text=text, label=label, score=float(top["score"]))
