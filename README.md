# sentiment_prompt_analyser

A web app that takes any sentence you type and predicts whether the sentiment is **positive**, **negative** or **neutral**, with a confidence score. Built on a pretrained model trained on hundreds of millions of social media posts, so it handles conversational and informal text well.

## The web app

Type a sentence, hit Analyse, and you get a colour-coded card with an emoji, a confidence bar and a short sound effect that matches the mood.

Run it on Google Colab (no install on your machine):

```
!git clone https://github.com/joshuaboladuro/sentiment_prompt_analyser.git
%cd sentiment_prompt_analyser
!pip install -r requirements.txt
!python app.py
```

Gradio prints a public `*.gradio.live` link you can open in any browser.

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

python cli.py --json "I am not impressed."
# {"text": "I am not impressed.", "label": "negative", "score": 0.842}

echo "Mixed feelings about this one." | python cli.py
```

## Tests

```bash
pip install pytest
pytest -q
```

## Licence

MIT.
