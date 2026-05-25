import config

def kelly_criterion(probability, odds, bankroll=None):
    """Calculate recommended stake using Half-Kelly Criterion for safety"""
    if bankroll is None:
        bankroll = config.BANKROLL
    
    if odds <= 1.01 or probability <= 0.5:
        return 0.0
    
    b = odds - 1  # Net odds
    kelly_fraction = (probability * (b + 1) - 1) / b
    # Use half Kelly for lower variance
    safe_kelly = kelly_fraction * 0.5
    stake = round(safe_kelly * bankroll, 2)
    return max(stake, 0.0)
