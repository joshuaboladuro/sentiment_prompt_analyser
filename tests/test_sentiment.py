"""Smoke tests for SentimentAnalyser.

These tests load the real model once (module-scoped fixture), so the
first test run takes a while as the weights download. After that they
hit cache and run quickly.

Run with: pytest -q
"""
from __future__ import annotations

import pytest

from sentiment import SentimentAnalyser, SentimentResult


@pytest.fixture(scope="module")
def analyser() -> SentimentAnalyser:
    return SentimentAnalyser()


def test_positive_text(analyser: SentimentAnalyser) -> None:
    result = analyser.analyse("This is brilliant, I absolutely love it.")
    assert result.label == "positive"
    assert 0 < result.score <= 1
    assert isinstance(result, SentimentResult)


def test_negative_text(analyser: SentimentAnalyser) -> None:
    result = analyser.analyse("This was awful, I'm really disappointed.")
    assert result.label == "negative"


def test_empty_string_raises(analyser: SentimentAnalyser) -> None:
    with pytest.raises(ValueError):
        analyser.analyse("   ")


def test_non_string_raises(analyser: SentimentAnalyser) -> None:
    with pytest.raises(ValueError):
        analyser.analyse(None)  # type: ignore[arg-type]


def test_batch(analyser: SentimentAnalyser) -> None:
    results = analyser.analyse_batch([
        "great service, will come back",
        "terrible, never again",
        "it was fine I guess",
    ])
    assert len(results) == 3
    assert all(isinstance(r, SentimentResult) for r in results)
    assert {r.label for r in results} <= {"positive", "negative", "neutral"}
