from models.football_model import FootballModel
from models.basketball_model import BasketballModel
import config

football_model = FootballModel()
basketball_model = BasketballModel()

def analyze_match(match):
    sport = match.get("sport", "football")
    
    if sport == "football":
        result = football_model.predict_match(match["home_team"], match["away_team"])
        return {**match, **result, "sport": sport}
    
    elif sport == "basketball":
        over_line = match.get("over_line", 220.0)
        h_totals = match.get("home_recent_totals")
        a_totals = match.get("away_recent_totals")
        result = basketball_model.predict_match(match["home_team"], match["away_team"], over_line, h_totals, a_totals)
        return {**match, **result, "sport": sport}
    
    return match