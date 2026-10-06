"""Smoke tests for the sentiment analyser."""
from __future__ import annotations

import pytest

from sentiment import SentimentAnalyser


@pytest.fixture(scope="module")
def analyser() -> SentimentAnalyser:
    return SentimentAnalyser()


def test_positive_sentence(analyser: SentimentAnalyser) -> None:
    result = analyser.analyse("I love this, it's absolutely brilliant.")
    assert result.label == "positive"
    assert 0.0 <= result.score <= 1.0


def test_negative_sentence(analyser: SentimentAnalyser) -> None:
    result = analyser.analyse("This is awful, I hate it.")
    assert result.label == "negative"


def test_empty_text_raises(analyser: SentimentAnalyser) -> None:
    with pytest.raises(ValueError):
        analyser.analyse("   ")
