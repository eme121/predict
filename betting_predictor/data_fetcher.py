import requests
import pandas as pd
from datetime import datetime
import config

def get_fixtures(sport="football", league=None, date=None):
    """Universal fixture fetcher supporting ALL leagues"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"🔌 Fetching {sport} fixtures for {date} - League: {league or 'ALL'}")
    
    if sport == "football":
        return fetch_all_football_fixtures(league, date)
    else:
        return fetch_all_basketball_fixtures(league, date)

def fetch_all_football_fixtures(league=None, date=None):
    """Fetch from ALL football leagues"""
    if league:
        leagues = [league]
    else:
        leagues = list(config.FOOTBALL_LEAGUES.keys())[:5]  # Top 5 for demo performance
    
    all_matches = []
    for lg in leagues:
        if lg in config.FOOTBALL_LEAGUES:
            league_info = config.FOOTBALL_LEAGUES[lg]
            matches = generate_mock_football_matches(lg, league_info["name"])
            all_matches.extend(matches)
    
    return pd.DataFrame(all_matches)

def fetch_all_basketball_fixtures(league=None, date=None):
    """Fetch from ALL basketball leagues"""
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
    """Dynamic mock data for any league"""
    base_teams = {
        "EPL": ["Man City", "Arsenal", "Liverpool", "Chelsea", "Tottenham"],
        "LA_LIGA": ["Real Madrid", "Barcelona", "Atletico", "Sevilla"],
        "BUNDESLIGA": ["Bayern", "Dortmund", "Leipzig"],
        "CHAMPIONS_LEAGUE": ["PSG", "Inter", "Real Madrid", "Bayern"],
        "MLS": ["LAFC", "Inter Miami", "NYCFC"],
    }
    teams = base_teams.get(league_key, ["Team A", "Team B", "Team C"])
    
    matches = []
    for i in range(3):
        home = teams[i % len(teams)]
        away = teams[(i + 2) % len(teams)]
        matches.append({
            "sport": "football",
            "league": league_name,
            "home_team": home,
            "away_team": away,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "home_odds": round(1.6 + i*0.2, 2),
            "draw_odds": 3.6,
            "away_odds": round(4.5 - i*0.3, 2),
        })
    return matches

def generate_mock_basketball_matches(league_key):
    """Dynamic mock for basketball with recent totals"""
    teams = {
        "NBA": ["Lakers", "Warriors", "Celtics", "Knicks", "Nuggets"],
        "EUROLEAGUE": ["Real Madrid", "Barcelona", "Olympiacos"],
        "NBL": ["Sutherland", "Central Coast", "Gold Coast Rollers", "Rockhampton Rockets", "Newcastle Falcons", "Illawarra Hawks", "South Adelaide Panthers", "Sturt Sabres"]
    }
    team_list = teams.get(league_key, ["Home Team", "Away Team"])
    
    matches = []
    # Create specific matches based on user example if NBL
    if league_key == "NBL":
        nbl_matches = [
            ("Sutherland", "Central Coast", 165.5, [111, 205], [197, 170, 153, 155, 148]),
            ("Gold Coast Rollers", "Rockhampton Rockets", 190.5, [210, 206, 224], [189, 164, 164, 197]),
            ("Newcastle Falcons", "Illawarra Hawks", 170.5, [175, 167, 135, 126, 133, 151], [178]),
            ("South Adelaide Panthers", "Sturt Sabres", 180.5, [185, 190, 175], [182, 178, 188])
        ]
        for home, away, line, h_totals, a_totals in nbl_matches:
            matches.append({
                "sport": "basketball",
                "league": league_key,
                "home_team": home,
                "away_team": away,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "over_line": line,
                "home_recent_totals": h_totals,
                "away_recent_totals": a_totals
            })
    else:
        for i in range(2):
            home = team_list[i % len(team_list)]
            away = team_list[(i+1) % len(team_list)]
            matches.append({
                "sport": "basketball",
                "league": league_key,
                "home_team": home,
                "away_team": away,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "over_line": 222.5 if league_key == "NBA" else 192.5,
                "home_recent_totals": [105, 110, 115],
                "away_recent_totals": [108, 112, 105]
            })
    return matches