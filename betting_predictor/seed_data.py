import requests
import pandas as pd
import os
import config
from datetime import datetime, timedelta

def seed_football():
    print("⚽ Seeding Football Historical Data...")
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-apisports-key': config.API_FOOTBALL_KEY}
    
    # Fetch last 30 days of data for a major league (e.g., EPL id 39)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    
    all_fixtures = []
    
    # API Football usually requires league and season
    params = {
        "league": 39, 
        "season": 2023, # Using 2023 as 2024 might not have much historical yet depending on time of year
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        data = response.json()
        
        for item in data.get("response", []):
            if item["fixture"]["status"]["short"] == "FT":
                all_fixtures.append({
                    "date": item["fixture"]["date"][:10],
                    "home_team": item["teams"]["home"]["name"],
                    "away_team": item["teams"]["away"]["name"],
                    "home_goals": item["goals"]["home"],
                    "away_goals": item["goals"]["away"]
                })
        
        if all_fixtures:
            df = pd.DataFrame(all_fixtures)
            path = os.path.join("data", "football_historical.csv")
            df.to_csv(path, index=False)
            print(f"✅ Saved {len(df)} football matches to {path}")
        else:
            print("⚠️ No football fixtures found to seed.")
            
    except Exception as e:
        print(f"❌ Error seeding football: {e}")

def seed_basketball():
    print("🏀 Seeding Basketball Historical Data (Mocking realistic patterns)...")
    # Historical basketball data is harder to get in bulk from free tier Odds API
    # We will generate 100 rows of realistic historical data to allow the model to train
    data = []
    teams = ["Lakers", "Warriors", "Celtics", "Nuggets", "Suns", "Bucks", "76ers", "Heat"]
    
    for i in range(100):
        h = teams[i % len(teams)]
        a = teams[(i + 3) % len(teams)]
        h_score = 100 + (i % 30)
        a_score = 95 + (i % 25)
        over_line = 210.5
        
        data.append({
            "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
            "home_team": h,
            "away_team": a,
            "home_score": h_score,
            "away_score": a_score,
            "total_points": h_score + a_score,
            "over_line": over_line
        })
    
    df = pd.DataFrame(data)
    path = os.path.join("data", "basketball_historical.csv")
    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df)} basketball matches to {path}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    seed_football()
    seed_basketball()
