import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import config
from data_fetcher import get_fixtures
import analyzer
import plotly.express as px
from kelly import kelly_criterion

# PWA + Dark Mode Configuration
st.set_page_config(
    page_title="SENE Predictor",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced CSS: Dark Mode + Mobile Optimization
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stMetric { background-color: #1E242F; border-radius: 8px; padding: 10px; border: 1px solid #30363D; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #262D38; border-radius: 6px; color: white; }
    .stExpander { border: 1px solid #30363D !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

st.title("🏆 SENE Betting Predictor")
st.caption(f"**Updated:** {datetime.now().strftime('%B %d, %Y at %H:%M')}")

# Bankroll Input
bankroll = st.sidebar.number_input("Your Bankroll ($)", value=1000, min_value=100, step=50)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🔥 Daily Strong Picks", "⚽ Football", "🏀 Basketball"])

with tab1:
    st.subheader("🔥 Today's Strongest Bets")
    
    football_fixtures = get_fixtures("football")
    basketball_fixtures = get_fixtures("basketball")
    
    if not football_fixtures.empty:
        st.markdown("### ⚽ Football Highlights")
        for _, match in football_fixtures.head(5).iterrows():
            analysis = analyzer.analyze_match(match.to_dict())
            with st.expander(f"**{match['home_team']} vs {match['away_team']}**"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Home Win", f"{analysis['home_win_prob']}%")
                col2.metric("Over 2.5", f"{analysis['over_2_5_prob']}%")
                col3.metric("Exp. Goals", f"{analysis.get('expected_goals')}")
                st.info(f"Verdict: **{analysis['recommended']}**")

    if not basketball_fixtures.empty:
        st.markdown("### 🏀 Basketball Highlights")
        for _, match in basketball_fixtures.iterrows():
            analysis = analyzer.analyze_match(match.to_dict())
            icon = "✅" if "OVER" in analysis['recommended'] else "❌"
            if "STRONG" in analysis['recommended'] or "MASSIVE" in analysis['recommended']:
                icon = "🔥"
                
            with st.expander(f"{icon} **{match['home_team']} vs {match['away_team']}**"):
                c1, c2 = st.columns(2)
                c1.metric("Model Line", f"OVER {match['over_line']}")
                edge_val = analysis['edge']
                c2.metric("Edge", f"{'+' if edge_val > 0 else ''}{edge_val}", delta=edge_val)
                
                if analysis.get('home_recent_totals'):
                    st.write(f"📊 **{match['home_team']}** recent totals: `{', '.join(map(str, analysis['home_recent_totals']))}`")
                if analysis.get('away_recent_totals'):
                    st.write(f"📊 **{match['away_team']}** recent totals: `{', '.join(map(str, analysis['away_recent_totals']))}`")
                
                color = "orange" if analysis.get('status') == "IMPORTANT" else "red"
                st.markdown(f":{color}[**{analysis.get('status')}**]: {analysis.get('reasoning')}")
                st.success(f"**Verdict**: {analysis['recommended']}")

with tab2:
    st.subheader("⚽ Football Predictions")
    league_filter = st.selectbox("Filter by League", ["All Leagues"] + list(config.FOOTBALL_LEAGUES.keys()))
    
    selected_league = None if league_filter == "All Leagues" else league_filter
    football_all = get_fixtures("football", league=selected_league)
    
    if football_all.empty:
        st.warning("No football matches found for the selected filter.")
    else:
        for _, match in football_all.iterrows():
            analysis = analyzer.analyze_match(match.to_dict())
            with st.expander(f"{match['home_team']} vs {match['away_team']} ({match['league']})"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Home Win", f"{analysis['home_win_prob']}%")
                col2.metric("Over 2.5", f"{analysis['over_2_5_prob']}%")
                col3.metric("Exp. Goals", f"{analysis.get('expected_goals')}")
                st.info(f"Verdict: **{analysis['recommended']}**")

with tab3:
    st.subheader("🏀 Basketball Predictions")
    bs_league_filter = st.selectbox("Filter by League ", ["All Leagues"] + list(config.BASKETBALL_LEAGUES.keys()))
    
    selected_bs_league = None if bs_league_filter == "All Leagues" else bs_league_filter
    basketball_all = get_fixtures("basketball", league=selected_bs_league)
    
    if basketball_all.empty:
        st.warning("No basketball matches found for the selected filter.")
    else:
        for _, match in basketball_all.iterrows():
            analysis = analyzer.analyze_match(match.to_dict())
            with st.expander(f"{match['home_team']} vs {match['away_team']} ({match.get('league', 'Pro')})"):
                c1, c2 = st.columns(2)
                c1.metric("Model Line", f"OVER {match['over_line']}")
                c2.metric("Edge", f"{analysis['edge']}")
                st.success(f"**Verdict**: {analysis['recommended']}")
