from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import analyzer

console = Console()

def print_dashboard(matches):
    console.print(Panel("[bold magenta]🏆 SENE BETTING PREDICTOR[/bold magenta]", 
                       title="Complete Sports Predictor", subtitle="Football + Basketball"))
    
    for i, match in enumerate(matches, 1):
        analysis = analyzer.analyze_match(match)
        
        if analysis['sport'] == "football":
            console.print(f"\n[bold cyan]{i}. {match['home_team']} vs {match['away_team']} ({analysis['sport'].upper()})[/bold cyan]")
            console.print(f"   Expected Goals: {analysis.get('expected_goals', 'N/A')}")
            console.print(f"   Home: {analysis['home_win_prob']}% | Draw: {analysis['draw_prob']}% | Away: {analysis['away_win_prob']}%")
            console.print(f"   Over 2.5 Goals: {analysis['over_2_5_prob']}% → [green]{analysis['recommended']}[/green]")
            if 'ml_confidence' in analysis:
                console.print(f"   ML Confidence: {analysis['ml_confidence']}%")
            
        elif analysis['sport'] == "basketball":
            icon = "✅"
            if "SKIP" in analysis.get('recommended', ''):
                icon = "❌"
            elif "STRONG" in analysis.get('recommended', ''):
                icon = "🔥"
                
            console.print(f"\n[bold]{icon} {i}. {match['home_team']} vs {match['away_team']}[/bold]")
            
            if analysis.get('edge') is not None:
                edge_color = "green" if analysis['edge'] > 0 else "red"
                console.print(f"Model: OVER {match.get('over_line', 'N/A')} | Edge: [{edge_color}]{'+' if analysis['edge'] > 0 else ''}{analysis['edge']}[/{edge_color}]")
                
                if analysis.get('home_recent_totals'):
                    console.print(f"• {match['home_team']} recent totals: {', '.join(map(str, analysis['home_recent_totals']))}")
                if analysis.get('away_recent_totals'):
                    console.print(f"• {match['away_team']} recent totals: {', '.join(map(str, analysis['away_recent_totals']))}")
                
                status_color = "bold yellow" if analysis.get('status') == "IMPORTANT" else "bold red"
                console.print(f"[{status_color}]{analysis.get('status', 'ANALYSIS')}[/{status_color}]")
                
                verdict_icon = "❌" if "SKIP" in analysis['recommended'] or "OVERRIDE" in analysis['recommended'] else "✅"
                console.print(f"Verdict: {verdict_icon} [bold]{analysis['recommended']}[/bold] — {analysis.get('reasoning', '')}")
        
        console.print("─" * 70)