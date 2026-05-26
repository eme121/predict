import requests
import pandas as pd
from datetime import datetime
import config

def get_fixtures(sport="football", league=None, date=None):
    """Universal fixture fetcher supporting real API data"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🔌 Fetching {sport} fixtures for {date} - League: {league or 'ALL'}")
    
    if sport == "football":
        df = fetch_real_football_fixtures(league, date)
        if df.empty:
            print("⚠️ No real football data found, falling back to demo data.")
            return fetch_all_football_fixtures(league, date)
        return df
    else:
        df = fetch_real_basketball_odds(league)
        if df.empty:
            print("⚠️ No real basketball data found, falling back to demo data.")
            return fetch_all_basketball_fixtures(league, date)
        return df

def fetch_real_football_fixtures(league=None, date=None):
    """Fetch real football fixtures and odds from API-Football"""
    if not config.API_FOOTBALL_KEY or "YOUR_API" in config.API_FOOTBALL_KEY:
        return pd.DataFrame()

    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-apisports-key': config.API_FOOTBALL_KEY
    }
    
    params = {"date": date}
    if league and league in config.FOOTBALL_LEAGUES:
        params["league"] = config.FOOTBALL_LEAGUES[league]["id"]
        params["season"] = datetime.now().year
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        
        matches = []
        for item in data.get("response", []):
            fixture = item["fixture"]
            league_info = item["league"]
            teams = item["teams"]
            
            # Note: Odds usually require a separate call or specific plan
            # Here we provide structure; if odds aren't in this endpoint, we'd fetch them separately
            matches.append({
                "sport": "football",
                "league": league_info["name"],
                "home_team": teams["home"]["name"],
                "away_team": teams["away"]["name"],
                "date": fixture["date"][:10],
                "home_odds": 2.0, # Placeholder if not in basic plan
                "draw_odds": 3.4,
                "away_odds": 3.6,
            })
        return pd.DataFrame(matches)
    except Exception as e:
        print(f"❌ Football API Error: {e}")
        return pd.DataFrame()

def fetch_real_basketball_odds(league=None):
    """Fetch real basketball odds from The Odds API"""
    if not config.ODDS_API_KEY or "YOUR_API" in config.ODDS_API_KEY:
        return pd.DataFrame()

    # Map our league keys to Odds API sport keys
    sport_map = {
        "NBA": "basketball_nba",
        "NBL": "basketball_nbl",
        "EUROLEAGUE": "basketball_euroleague"
    }
    
    sport_key = sport_map.get(league, "basketball_nba")
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
    params = {
        "apiKey": config.ODDS_API_KEY,
        "regions": "us,au",
        "markets": "h2h,totals",
        "oddsFormat": "decimal"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        matches = []
        for item in data:
            home_team = item["home_team"]
            away_team = item["away_team"]
            
            # Find totals line (Over/Under)
            over_line = 220.5 # Default
            for bookmaker in item.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    if market["key"] == "totals":
                        over_line = market["outcomes"][0]["point"]
                        break
            
            matches.append({
                "sport": "basketball",
                "league": item["sport_title"],
                "home_team": home_team,
                "away_team": away_team,
                "date": item["commence_time"][:10],
                "over_line": over_line,
                "home_recent_totals": [110, 105, 115], # Would ideally fetch historical
                "away_recent_totals": [108, 112, 100]
            })
        return pd.DataFrame(matches)
    except Exception as e:
        print(f"❌ Odds API Error: {e}")
        return pd.DataFrame()

# --- Legacy Mock Functions for Fallback ---

def fetch_all_football_fixtures(league=None, date=None):
    if league:
        leagues = [league]
    else:
        leagues = list(config.FOOTBALL_LEAGUES.keys())[:5]
    
    all_matches = []
    for lg in leagues:
        if lg in config.FOOTBALL_LEAGUES:
            league_info = config.FOOTBALL_LEAGUES[lg]
            matches = generate_mock_football_matches(lg, league_info["name"])
            all_matches.extend(matches)
    return pd.DataFrame(all_matches)

def fetch_all_basketball_fixtures(league=None, date=None):
    if league:
        leagues = [league]
    else:
        leagues = list(config.BASKETBALL_LEAGUES.keys())[:3]
    
    all_matches = []
    for lg in leagues:
        matches = generate_mock_basketball_matches(lg)
        all_matches.extend(matches)
    return pd.DataFrame(all_matches)

def generate_mock_football_matches(league_key, league_name):
    try:
        df_hist = pd.read_csv(config.FOOTBALL_HISTORICAL)
        teams = pd.concat([df_hist['home_team'], df_hist['away_team']]).unique()
        import random
        matches = []
        for i in range(5):
            h, a = random.sample(list(teams), 2)
            matches.append({
                "sport": "football",
                "league": league_name,
                "home_team": h,
                "away_team": a,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "home_odds": round(random.uniform(1.5, 4.0), 2),
                "draw_odds": round(random.uniform(3.0, 4.5), 2),
                "away_odds": round(random.uniform(2.0, 5.0), 2),
            })
        return matches
    except:
        return []

def generate_mock_basketball_matches(league_key):
    try:
        df_hist = pd.read_csv(config.BASKETBALL_HISTORICAL)
        teams = pd.concat([df_hist['home_team'], df_hist['away_team']]).unique()
        import random
        matches = []
        for i in range(3):
            h, a = random.sample(list(teams), 2)
            matches.append({
                "sport": "basketball",
                "league": league_key,
                "home_team": h,
                "away_team": a,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "over_line": round(random.uniform(200, 230) * 2) / 2,
                "home_recent_totals": [random.randint(90, 120) for _ in range(3)],
                "away_recent_totals": [random.randint(90, 120) for _ in range(3)]
            })
        return matches
    except:
        return []
