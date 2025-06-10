
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
        # Write to shared file for Rust bot to read
        with open("shared.txt", "w") as f:
            f.write("Python bot received a ping command!")
        
        await ctx.send("Ping received! Message saved to shared.txt for Rust bot.")
        print("Ping command executed successfully")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
        print(f"Error in ping command: {e}")

@bot.command()
async def check_rust(ctx):
    """Check for messages from Rust bot"""
    try:
        with open("shared.txt", "r") as f:
            content = f.read()
            if "Rust bot received ping" in content:
                await ctx.send(f"Rust bot says: {content}")
            else:
                await ctx.send("No recent messages from Rust bot.")
    except FileNotFoundError:
        await ctx.send("No shared file found. Rust bot hasn't sent any messages yet.")
    except Exception as e:
        await ctx.send(f"Error reading shared file: {str(e)}")

@bot.command()
async def hello(ctx):
    """Greet the user"""
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def dual_status(ctx):
    """Show the status of both bots"""
    try:
        with open("shared.txt", "r") as f:
            content = f.read()
            await ctx.send(f"Shared communication file contains: {content}")
    except FileNotFoundError:
        await ctx.send("No communication file found yet.")
    except Exception as e:
        await ctx.send(f"Error checking status: {str(e)}")

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
