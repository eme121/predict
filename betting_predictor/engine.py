import pandas as pd
from data_fetcher import get_fixtures
from dashboard import print_dashboard
from backtester import Backtester
import config
from datetime import datetime
from models.ml_models import MLFootballPredictor, MLBasketballPredictor
import os
import sys

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, path)

def run_predictions(send_to_telegram=False, send_to_discord=False):
    """Main prediction engine"""
    print("🚀 SENE Betting Predictor - ALL LEAGUES ACTIVATED")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Ensure directories (use relative paths for normal run)
    data_dir = resolve_path('data')
    models_dir = resolve_path('models')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    # Train Advanced XGBoost Models
    print("🧠 Training Advanced XGBoost Models with Feature Engineering...")
    ml_football = MLFootballPredictor()
    ml_football.train()
    ml_basketball = MLBasketballPredictor()
    ml_basketball.train()
    
    # Backtesting
    print("\n📈 Running Full Backtest...")
    backtester = Backtester()
    backtester.run_full_backtest()
    
    # Fetch from ALL Leagues
    print("\n🌍 Fetching Fixtures from ALL Leagues...")
    football_matches = get_fixtures(sport="football", league=None)
    basketball_matches = get_fixtures(sport="basketball", league=None)
    
    print(f"   → Fetched {len(football_matches)} Football matches")
    print(f"   → Fetched {len(basketball_matches)} Basketball matches")
    
    all_matches = pd.concat([football_matches, basketball_matches], ignore_index=True)
    
    print("\n🤖 Generating Advanced AI Predictions...")
    print_dashboard(all_matches.to_dict('records'))
    
    print(f"\n💰 Current Bankroll: ${config.BANKROLL:,}")
    print("🎯 System supports 15+ Football Leagues & Multiple Basketball Leagues")
    print("✅ Real-time odds comparison + Kelly Staking enabled")
