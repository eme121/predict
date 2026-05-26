import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env")) # Local
load_dotenv() # Deployed/System

# API Configuration
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")


# ALL MAJOR FOOTBALL LEAGUES
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
    "RUSSIAN_PREMIER": {"id": 235, "name": "Premier League", "country": "Russia"},
    # Add more leagues easily here
}

# ALL MAJOR BASKETBALL LEAGUES
BASKETBALL_LEAGUES = {
    "NBA": {"name": "NBA", "country": "USA"},
    "EUROLEAGUE": {"name": "EuroLeague", "country": "Europe"},
    "NBL": {"name": "NBL", "country": "Australia"},
    "ACB": {"name": "ACB League", "country": "Spain"},
    "LNB": {"name": "LNB Pro A", "country": "France"},
    "BBL": {"name": "Basketball Bundesliga", "country": "Germany"},
    # Add more here
}

# Betting Settings
MIN_EDGE = 5.0
STRONG_EDGE = 12.0
BANKROLL = 1000.0
MIN_CONFIDENCE = 18.0

# Paths
DATA_DIR = "data"
FOOTBALL_HISTORICAL = f"{DATA_DIR}/football_historical.csv"
BASKETBALL_HISTORICAL = f"{DATA_DIR}/basketball_historical.csv"

# ML Settings
RANDOM_STATE = 42
TEST_SIZE = 0.2
MODELS_DIR = "models"

# Bot Settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_DISCORD_BOT_TOKEN")
CHANNEL_ID = 1234567890  # Update with your Discord channel ID