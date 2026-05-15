# sentiment_prompt_analyser

A web app that takes any sentence you type and predicts whether the sentiment is **positive**, **negative** or **neutral**, with a confidence score. Built on a pretrained model trained on hundreds of millions of social media posts, so it handles conversational and informal text well.

A FastAPI backend serves the model and a Next.js frontend (TypeScript + Tailwind) renders the result as a colour-coded card with an animated SVG face, a confidence bar and smooth motion transitions.

## Architecture

```
backend/    Python FastAPI server. Loads the model once, exposes /analyse.
frontend/   Next.js + TypeScript + Tailwind. Talks to the backend over HTTP.
```

## Run locally

You'll need **Python 3.10+** and **Node.js 18+** installed.

### 1. Start the backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```

First run downloads the model (~500 MB), then runs on http://localhost:8000.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## Deploy

### Backend on Hugging Face Spaces

1. Create a new Space at https://huggingface.co/new-space, choose the **Docker** SDK.
2. Add a Dockerfile that copies backend/ and runs uvicorn api:app --host 0.0.0.0 --port 7860.
3. Push. You get a free permanent URL.

### Frontend on Vercel

1. Go to https://vercel.com/new and import this repo.
2. Set the **root directory** to frontend.
3. Add an env variable: NEXT_PUBLIC_API_URL pointing at your Space URL.
4. Deploy.

## Licence

MIT.
