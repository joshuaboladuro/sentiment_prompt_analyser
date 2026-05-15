"""Sentiment analyser backed by a pre-trained transformer model.

Wraps a Hugging Face pipeline and returns a structured result with a
3-class label (positive, neutral, negative) and a confidence score.
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
    """The outcome of analysing one piece of text."""

    text: str
    label: Sentiment
    score: float

    def __str__(self) -> str:
        return f"{self.label} ({self.score:.3f}): {self.text!r}"


class SentimentAnalyser:
    """Loads the model once and exposes a small analyse / analyse_batch API."""

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        self._model_name = model_name
        self._pipe = pipeline("sentiment-analysis", model=model_name, top_k=None)

    @property
    def model_name(self) -> str:
        return self._model_name

    def analyse(self, text: str) -> SentimentResult:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")

        raw = self._pipe(text)[0]  
        top = max(raw, key=lambda r: r["score"])
        label = _LABEL_MAP.get(top["label"], top["label"].lower()) 
        return SentimentResult(text=text, label=label, score=float(top["score"]))

    def analyse_batch(self, texts: list[str]) -> list[SentimentResult]:
        return [self.analyse(t) for t in texts]
