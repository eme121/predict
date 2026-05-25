import discord
from discord.ext import tasks, commands
import config
from main import run_predictions

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Discord Bot {bot.user} is ready!')
    daily_predictions.start()

@tasks.loop(hours=24)
async def daily_predictions():
    """Send daily predictions to channel"""
    channel = bot.get_channel(1234567890)  # Replace with your channel ID
    if channel:
        await channel.send("🏀 **SENE Daily Betting Predictions**")
        # Add predictions here
        await channel.send("✅ Predictions generated! Check Streamlit dashboard.")

@bot.command()
async def predict(ctx):
    """Manual prediction command"""
    await ctx.send("🔄 Generating predictions across all leagues...")
    run_predictions()

if __name__ == "__main__":
    if config.DISCORD_TOKEN:
        bot.run(config.DISCORD_TOKEN)
    else:
        print("Set DISCORD_TOKEN in config.py")
