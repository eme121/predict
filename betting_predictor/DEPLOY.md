# SENE Betting Predictor - Deployment Guide

## 1. GitHub Repo Structure (Recommended)

```
sene-betting-predictor/
├── betting_predictor/
│   ├── main.py
│   ├── streamlit_app.py
│   ├── config.py
│   ├── data_fetcher.py
│   ├── analyzer.py
│   ├── dashboard.py
│   ├── backtester.py
│   ├── kelly.py
│   ├── scheduler.py
│   ├── odds_comparator.py
│   ├── telegram_bot.py
│   ├── discord_bot.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── DEPLOY.md
│   ├── README.md
│   ├── manifest.json
│   ├── data/
│   │   ├── football_historical.csv
│   │   └── basketball_historical.csv
│   └── models/
│       ├── __init__.py
│       ├── football_model.py
│       ├── basketball_model.py
│       └── ml_models.py
├── .streamlit/
│   └── config.toml
└── .gitignore
```

## 2. Dockerfile (Already Created)

Use the `Dockerfile` for Docker / Heroku / Railway / Fly.io

```bash
docker build -t sene-predictor .
docker run -p 8501:8501 sene-predictor
```

## 3. Streamlit Cloud (Easiest for Android PWA)
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Add Secrets (API keys)

## 4. Docker Deployment
```bash
docker build -t sene-betting .
docker run -p 8501:8501 \
  -e API_FOOTBALL_KEY=yourkey \
  -e ODDS_API_KEY=yourkey \
  sene-betting
```

## 5. Android Installation
Open deployed URL in Chrome → Menu → "Install app"
