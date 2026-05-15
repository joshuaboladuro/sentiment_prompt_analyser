"""Gradio web UI for the sentiment analyser.

Renders the result as a colour-coded card with an emoji, a confidence bar
and a short sound effect that matches the mood: a cheerful chord for
positive, a single tone for neutral, and a low minor chord for negative.

Run locally:
    pip install -r requirements.txt
    python app.py

Run on Google Colab:
    !git clone https://github.com/joshuaboladuro/sentiment_prompt_analyser.git
    %cd sentiment_prompt_analyser
    !pip install -r requirements.txt
    !python app.py

Gradio prints a public *.gradio.live URL you can open in any browser.
"""
from __future__ import annotations

import numpy as np
import gradio as gr

from sentiment import SentimentAnalyser

SAMPLE_RATE = 44_100

analyser = SentimentAnalyser()


SENTIMENT_CONFIG: dict[str, dict] = {
    "positive": {
        "emoji": "😄",
        "label": "Positive",
        "color": "#10b981",
        "bg": "#d1fae5",
        "frequencies": [523.25, 659.25, 783.99],
        "duration": 0.55,
    },
    "neutral": {
        "emoji": "😐",
        "label": "Neutral",
        "color": "#6b7280",
        "bg": "#e5e7eb",
        "frequencies": [440.0],
        "duration": 0.4,
    },
    "negative": {
        "emoji": "😔",
        "label": "Negative",
        "color": "#ef4444",
        "bg": "#fee2e2",
        "frequencies": [220.0, 261.63, 329.63],
        "duration": 0.7,
    },
}


def _generate_tone(frequencies: list[float], duration: float) -> tuple[int, np.ndarray]:
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    audio = np.zeros_like(t)
    for f in frequencies:
        audio += np.sin(2 * np.pi * f * t)
    audio /= max(len(frequencies), 1)

    fade = int(0.04 * SAMPLE_RATE)
    envelope = np.ones_like(audio)
    envelope[:fade] = np.linspace(0, 1, fade)
    envelope[-fade:] = np.linspace(1, 0, fade)
    audio *= envelope

    return SAMPLE_RATE, (audio * 0.5 * 32_767).astype(np.int16)


def _result_card(text: str, label: str, score: float) -> str:
    config = SENTIMENT_CONFIG[label]
    pct = int(score * 100)
    bg = config["bg"]
    color = config["color"]
    emoji = config["emoji"]
    name = config["label"]
    return (
        f'<div style="background:{bg};border:2px solid {color};'
        f'border-radius:16px;padding:32px;text-align:center;'
        f'font-family:-apple-system,system-ui,sans-serif">'
        f'<div style="font-size:88px;line-height:1">{emoji}</div>'
        f'<div style="font-size:32px;font-weight:700;color:{color};'
        f'margin-top:8px">{name}</div>'
        f'<div style="background:white;border-radius:999px;height:12px;'
        f'margin:16px auto;max-width:320px;overflow:hidden">'
        f'<div style="background:{color};height:100%;width:{pct}%"></div></div>'
        f'<div style="color:#4b5563;font-size:14px">Confidence: <b>{pct}%</b></div>'
        f'<div style="color:#6b7280;font-size:13px;margin-top:16px;'
        f'font-style:italic;max-width:480px;margin:16px auto 0">'
        f'&ldquo;{text}&rdquo;</div></div>'
    )


def analyse(text: str) -> tuple[str, tuple[int, np.ndarray] | None]:
    if text is None or not text.strip():
        empty = (
            '<p style="color:#6b7280;text-align:center;padding:24px">'
            'Type something above and hit Analyse.</p>'
        )
        return empty, None

    result = analyser.analyse(text)
    config = SENTIMENT_CONFIG[result.label]
    audio = _generate_tone(config["frequencies"], config["duration"])
    return _result_card(result.text, result.label, result.score), audio


CSS = """
.gradio-container { max-width: 760px !important; }
footer { display: none !important; }
"""


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="indigo"),
    css=CSS,
    title="Sentiment Analyser",
) as demo:
    gr.Markdown(
        "# 🎯 Sentiment Prompt Analyser\n"
        "\n"
        "Type a sentence below and the AI will tell you whether it sounds "
        "**positive**, **neutral** or **negative**, with a confidence score "
        "and a matching sound effect."
    )

    with gr.Row():
        text_in = gr.Textbox(
            label="Your text",
            placeholder="e.g. Honestly, the food was incredible.",
            lines=3,
            autofocus=True,
            scale=4,
        )

    submit = gr.Button("Analyse sentiment", variant="primary", size="lg")

    result = gr.HTML()
    audio_out = gr.Audio(autoplay=True, visible=False, label="Sound")

    submit.click(analyse, inputs=text_in, outputs=[result, audio_out])
    text_in.submit(analyse, inputs=text_in, outputs=[result, audio_out])

    gr.Examples(
        examples=[
            "Honestly, the food was incredible.",
            "I am really not impressed by this at all.",
            "It was okay I guess, nothing special.",
            "Absolutely brilliant, would recommend to anyone!",
            "Worst experience of my life, never again.",
            "The package arrived on time.",
        ],
        inputs=text_in,
        label="Try one of these",
    )


if __name__ == "__main__":
    demo.launch()
