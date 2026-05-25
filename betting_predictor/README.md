# SENE Betting Predictor

Full-featured AI sports betting predictor for **Football + Basketball** across all major leagues.

## 🚀 How to Install on Android Phone

### Easiest Way (PWA - Recommended)

1. **Deploy to Streamlit Cloud** (Free):
   - Go to https://share.streamlit.io
   - Connect GitHub repo containing this folder
   - Deploy `streamlit_app.py`

2. **Or Run Locally**:
   ```bash
   cd betting_predictor
   streamlit run streamlit_app.py
   ```

3. **Install on Phone**:
   - Open the app URL in **Chrome**
   - Tap **⋮** (3 dots) → **"Install app"** or **"Add to home screen"**
   - The app will now work offline and appear as a native app!

## Features
- All major leagues (EPL, La Liga, NBA, etc.)
- XGBoost ML with feature engineering
- Real-time odds comparison
- Kelly Criterion staking
- Daily scheduler
- Telegram + Discord bots

## Setup API Keys
```bash
export API_FOOTBALL_KEY=your_key
export ODDS_API_KEY=your_key
```

**Ready for daily use!**