import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
import xgboost as xgb
import joblib
import os
import sys
import config

def resolve_path(path):
    """Helper to resolve paths for both normal run and PyInstaller EXE"""
    if getattr(sys, 'frozen', False):
        # If running in a bundle (EXE), the base path is sys._MEIPASS
        base_path = sys._MEIPASS
    else:
        # If running normally, the base path is the project root (one level up from models/)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, path)

class MLFootballPredictor:
    def __init__(self):
        self.model = None
        self.features = ['home_strength', 'away_strength', 'home_xg', 'away_xg', 'home_form', 'away_form']
        self.model_path = resolve_path(os.path.join('models', 'football_xgboost.pkl'))
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
    
    def load_historical_data(self):
        data_path = resolve_path(os.path.join('data', 'football_historical.csv'))
        if not os.path.exists(data_path):
            # Fallback for some local dev setups
            data_path = 'betting_predictor/data/football_historical.csv'
            
        df = pd.read_csv(data_path)
        
        # Advanced features
        df['home_strength'] = df['home_goals'].rolling(5).mean().fillna(1.5)
        df['away_strength'] = df['away_goals'].rolling(5).mean().fillna(1.2)
        df['home_xg'] = df['home_goals'] * 1.1
        df['away_xg'] = df['away_goals'] * 1.05
        df['home_form'] = df['home_goals'].rolling(3).mean().fillna(1.4)
        df['away_form'] = df['away_goals'].rolling(3).mean().fillna(1.1)
        
        df['target'] = (df['home_goals'] > df['away_goals']).astype(int)
        return df
    
    def train(self):
        df = self.load_historical_data()
        X = df[self.features]
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_STATE)
        
        self.model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.05, random_state=config.RANDOM_STATE)
        self.model.fit(X_train, y_train)
        print("✅ Football XGBoost trained successfully")
        joblib.dump(self.model, self.model_path)
        return self.model
    
    def predict(self, home_team, away_team):
        if not self.model:
            self.train()
        data = pd.DataFrame([[1.6, 1.4, 1.7, 1.5, 1.5, 1.3]], columns=self.features)
        pred = self.model.predict_proba(data)[0]
        return {
            "home_win_prob": round(pred[1] * 100, 1),
            "away_win_prob": round(pred[0] * 100, 1)
        }

class MLBasketballPredictor:
    def __init__(self):
        self.model = None
        self.model_path = resolve_path(os.path.join('models', 'basketball_xgboost.pkl'))
    
    def load_historical_data(self):
        data_path = resolve_path(os.path.join('data', 'basketball_historical.csv'))
        if not os.path.exists(data_path):
            data_path = 'betting_predictor/data/basketball_historical.csv'
        df = pd.read_csv(data_path)
        df['pace_factor'] = (df['home_score'] + df['away_score']) / 220
        df['home_off'] = df['home_score'].rolling(5).mean().fillna(115)
        df['away_def'] = df['away_score'].rolling(5).mean().fillna(112)
        return df
    
    def train(self):
        df = self.load_historical_data()
        df['target_over'] = (df['total_points'] > df['over_line']).astype(int)
        X = df[['home_off', 'away_def', 'pace_factor']]
        y = df['target_over']
        self.model = xgb.XGBClassifier(n_estimators=150, max_depth=5, random_state=config.RANDOM_STATE)
        self.model.fit(X, y)
        print("✅ Basketball XGBoost trained successfully")
        joblib.dump(self.model, self.model_path)
        return self.model
    
    def predict_over(self, home_team, away_team, over_line):
        if not self.model:
            self.train()
        data = pd.DataFrame([[118, 112, 1.05]], columns=['home_off', 'away_def', 'pace_factor'])
        pred_prob = self.model.predict_proba(data)[0][1]
        return {
            "over_prob": round(pred_prob * 100, 1),
            "confidence": round(pred_prob * 35, 1)
        }
