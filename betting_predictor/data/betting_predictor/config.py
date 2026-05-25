import os
from datetime import datetime

# ============== API KEYS ==============
# Get free API keys here:
# API-Football: https://www.api-football.com/ → Register → Dashboard (Free plan: 100 req/day)
# The Odds API: https://the-odds-api.com/ → Subscribe for Starter FREE (500 credits/month)

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "YOUR_API_FOOTBALL_KEY_HERE")
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "YOUR_ODDS_API_KEY_HERE")

# ALL MAJOR LEAGUES (Football)
FOOTBALL_LEAGUES = {
    "EPL": {"id": 39, "name": "Premier League", "country": "England"},
    "LA_LIGA": {"id": 140, "name": "La Liga", "country": "Spain"},
    "BUNDESLIGA": {"id": 78, "name": "Bundesliga", "country": "Germany"},
    "SERIE_A": {"id": 135, "name": "Serie A", "country": "Italy"},
    "LIGUE_1": {"id": 61, "name": "Ligue 1", "country": "France"},
    "CHAMPIONS_LEAGUE": {"id": 2, "name": "UEFA Champions League", "country": "Europe"},
    "EUROPA_LEAGUE": {"id": 3, "name": "UEFA Europa League", "country": "Europe"},
    "MLS": {"id": 253, "name": "Major League Soccer", "country": "USA"},
    "BRAZIL_SERIE_A": {"id": 71, "name": "Brasileirão Série A", "country": "Brazil"},
    "SAUDI_PRO": {"id": 362, "name": "Saudi Pro League", "country": "Saudi Arabia"},
    "A_LEAGUE": {"id": 211, "name": "A-League", "country": "Australia"},
    "EREDIVISIE": {"id": 88, "name": "Eredivisie", "country": "Netherlands"},
    "PORTUGAL_PRIMEIRA": {"id": 94, "name": "Primeira Liga", "country": "Portugal"},
    "TURKISH_SUPER_LIG": {"id": 203, "name": "Süper Lig", "country": "Turkey"},
}

# BASKETBALL LEAGUES
BASKETBALL_LEAGUES = {
    "NBA": {"name": "NBA", "country": "USA"},
    "EUROLEAGUE": {"name": "EuroLeague", "country": "Europe"},
    "NBL": {"name": "NBL", "country": "Australia"},
    "ACB": {"name": "ACB", "country": "Spain"},
    "LNB": {"name": "LNB Pro A", "country": "France"},
}

# Betting & Model Settings
MIN_EDGE = 5.0
STRONG_EDGE = 12.0
BANKROLL = 1000.0
MIN_CONFIDENCE = 18.0

# Data Paths
DATA_DIR = "data"
FOOTBALL_HISTORICAL = f"{DATA_DIR}/football_historical.csv"
BASKETBALL_HISTORICAL = f"{DATA_DIR}/basketball_historical.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.2