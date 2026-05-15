"""Command line wrapper for the sentiment analyser.

Examples:
    python cli.py "Honestly, the food was incredible."
    python cli.py --json "I am not impressed."
    echo "Mixed feelings about this one." | python cli.py
"""
from __future__ import annotations

import argparse
import json
import sys

from sentiment import SentimentAnalyser


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyse the sentiment of a piece of text "
        "(positive, negative or neutral).",
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to analyse. If omitted, the tool reads from stdin.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the result as JSON instead of a friendly line.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    text = args.text if args.text is not None else sys.stdin.read()
    text = text.strip()
    if not text:
        print("Error: no text provided.", file=sys.stderr)
        return 1

    analyser = SentimentAnalyser()
    result = analyser.analyse(text)

    if args.json:
        print(json.dumps({
            "text": result.text,
            "label": result.label,
            "score": result.score,
        }))
    else:
        print(f"Sentiment: {result.label} (confidence: {result.score:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
