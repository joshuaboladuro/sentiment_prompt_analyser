# sentiment_prompt_analyser

A small Python tool that takes a piece of text and tells you whether the sentiment is **positive**, **negative** or **neutral**, with a confidence score. It's backed by a pre-trained RoBERTa model from Hugging Face (`cardiffnlp/twitter-roberta-base-sentiment-latest`), trained on roughly 124M tweets, so it handles conversational and informal text well.

## What you can do with it

Use it from Python, from the command line, or in batch over a list of strings. Returns a clean `SentimentResult` dataclass with `text`, `label` and `score`.

## Install

```bash
git clone https://github.com/joshuaboladuro/sentiment_prompt_analyser.git
cd sentiment_prompt_analyser
pip install -r requirements.txt
```

The first run downloads the model weights (around 500 MB) and caches them locally. After that it's offline.

## Use from Python

```python
from sentiment import SentimentAnalyser

analyser = SentimentAnalyser()
result = analyser.analyse("Honestly, the food was incredible.")

print(result.label)   # positive
print(result.score)   # 0.987
print(result)         # positive (0.987): 'Honestly, the food was incredible.'
```

Batch:

```python
results = analyser.analyse_batch([
    "great service, will come back",
    "terrible, never again",
    "it was fine I guess",
])
for r in results:
    print(r.label, r.score)
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

The first run loads the model so will be slow, after that the tests are quick.

## Why this model

`cardiffnlp/twitter-roberta-base-sentiment-latest` was specifically chosen because it returns three classes (positive, neutral, negative) rather than the binary output you get from most default sentiment pipelines, and because it was trained on social media text which lines up well with the kind of short, informal prompts this tool is built for.

## License

MIT.
# sentiment_prompt_analyser
A Python tool to output the sentiment (positive, negative or neutral) of user text prompts.
