# sentiment_prompt_analyser

A small Python tool that takes a piece of text and tells you whether the sentiment is **positive**, **negative** or **neutral**, with a confidence score. It's backed by a pre-trained RoBERTa model from Hugging Face (`cardiffnlp/twitter-roberta-base-sentiment-latest`), trained on roughly 124M tweets, so it handles conversational and informal text well.

## The web UI

The repo includes a Gradio app (`app.py`) that wraps the analyser in a friendly interface: type a sentence, hit Analyse, and you get a big colour-coded card with an emoji, confidence bar and a short sound effect that matches the mood.

Try it on Colab (no install on your machine):

```
!git clone https://github.com/joshuaboladuro/sentiment_prompt_analyser.git
%cd sentiment_prompt_analyser
!pip install -r requirements.txt
!python app.py
```

Gradio prints a public `*.gradio.live` URL you can open in any browser.

Or run locally:

```bash
git clone https://github.com/joshuaboladuro/sentiment_prompt_analyser.git
cd sentiment_prompt_analyser
pip install -r requirements.txt
python app.py
```

## Use from Python

```python
from sentiment import SentimentAnalyser

analyser = SentimentAnalyser()
result = analyser.analyse("Honestly, the food was incredible.")

print(result.label)   # positive
print(result.score)   # 0.987
```

## Use from the command line

```bash
python cli.py "Honestly, the food was incredible."
# Sentiment: positive (confidence: 0.987)

python cli.py --json "I'm not impressed."
# {"text": "I'm not impressed.", "label": "negative", "score": 0.842}

echo "Mixed feelings about this one." | python cli.py
```

## Tests

```bash
pip install pytest
pytest -q
```

## Why this model

`cardiffnlp/twitter-roberta-base-sentiment-latest` returns three classes (positive, neutral, negative) rather than the binary output you get from most default sentiment pipelines, and it was trained on social media text which lines up well with the kind of short, informal prompts this tool is built for.

## License

MIT.
