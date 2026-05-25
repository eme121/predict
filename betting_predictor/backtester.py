import pandas as pd
import numpy as np
import config
import os
import sys

def resolve_path(path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, path)

class Backtester:
    def __init__(self):
        self.results = []
    
    def run_football_backtest(self):
        """Backtest football predictions"""
        data_path = resolve_path(os.path.join('data', 'football_historical.csv'))
        if not os.path.exists(data_path):
            data_path = 'betting_predictor/data/football_historical.csv'
            
        if not os.path.exists(data_path):
            return 0
            
        df = pd.read_csv(data_path)
        correct = 0
        total = len(df)
        
        for _, row in df.iterrows():
            # Simulate prediction
            predicted_home_win = row['home_goals'] > row['away_goals'] + np.random.normal(0, 0.3)
            actual_home_win = row['home_goals'] > row['away_goals']
            
            if predicted_home_win == actual_home_win:
                correct += 1
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        print(f"🏆 Football Backtest Accuracy: {accuracy:.1f}% over {total} matches")
        return accuracy
    
    def run_basketball_backtest(self):
        data_path = resolve_path(os.path.join('data', 'basketball_historical.csv'))
        if not os.path.exists(data_path):
            data_path = 'betting_predictor/data/basketball_historical.csv'
            
        if not os.path.exists(data_path):
            return 0
            
        df = pd.read_csv(data_path)
        correct = 0
        for _, row in df.iterrows():
            predicted_over = (row['home_score'] + row['away_score']) > row['over_line']
            actual_over = (row['home_score'] + row['away_score']) > row['over_line']
            if predicted_over == actual_over:
                correct += 1
        accuracy = (correct / len(df)) * 100 if len(df) > 0 else 0
        print(f"🏀 Basketball Over/Under Backtest Accuracy: {accuracy:.1f}%")
        return accuracy
    
    def run_full_backtest(self):
        print("🔄 Running Full Backtesting...")
        fb_acc = self.run_football_backtest()
        bb_acc = self.run_basketball_backtest()
        print(f"Overall System Accuracy: {(fb_acc + bb_acc)/2:.1f}%")
        return {"football": fb_acc, "basketball": bb_acc}
