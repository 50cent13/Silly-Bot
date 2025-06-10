
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()

# Set up bot with proper intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Python bot logged in as {bot.user}")
    print(f"Bot is in {len(bot.guilds)} guilds")

@bot.command()
async def ping(ctx):
    """Simple ping command that responds with pong"""
    try:
        # Write to shared file (create in current directory instead of parent)
        with open("shared.txt", "w") as f:
            f.write("Python bot received a ping command!")
        
        await ctx.send("Ping received! Message saved to shared.txt")
        print("Ping command executed successfully")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
        print(f"Error in ping command: {e}")

@bot.command()
async def hello(ctx):
    """Greet the user"""
    await ctx.send(f"Hello {ctx.author.mention}!")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use `!help` to see available commands.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
        print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN_PY")
    if not token:
        print("Error: BOT_TOKEN_PY environment variable not found!")
        print("Please set up your bot token in the Secrets tab.")
    else:
        try:
            bot.run(token)
        except discord.LoginFailure:
            print("Error: Invalid bot token!")
        except Exception as e:
            print(f"Error starting bot: {e}")
