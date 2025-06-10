
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("BOT_TOKEN_PY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Python bot logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    """Python bot responds and writes to shared.txt"""
    message = f"Python bot received ping from {ctx.author} at {ctx.message.created_at}"
    
    with open("shared.txt", "w") as f:
        f.write(message)
    
    await ctx.send("Ping received! Message passed to Rust bot via shared.txt")
    print(f"Python bot: {message}")

@bot.command()
async def check_rust(ctx):
    """Python bot reads messages from Rust bot"""
    try:
        with open("shared.txt", "r") as f:
            content = f.read().strip()
        
        if content:
            if content.startswith("Rust bot"):
                await ctx.send(f"Message from Rust bot: {content}")
            else:
                await ctx.send("No Rust bot messages found in shared file")
        else:
            await ctx.send("Shared file is empty")
    except FileNotFoundError:
        await ctx.send("Shared file not found")

@bot.command()
async def dual_status(ctx):
    """Shows current shared communication status"""
    try:
        with open("shared.txt", "r") as f:
            content = f.read().strip()
        
        if content:
            await ctx.send(f"Shared communication status: Active\nCurrent message: {content}")
        else:
            await ctx.send("Shared communication status: Empty")
    except FileNotFoundError:
        await ctx.send("Shared communication status: File not found")

@bot.command()
async def hello(ctx):
    """Simple greeting"""
    await ctx.send(f"Hello {ctx.author.mention}! I'm the Python bot in the dual bot system.")

if __name__ == "__main__":
    if not token:
        print("Error: BOT_TOKEN_PY not found in environment variables")
        print("Please set BOT_TOKEN_PY in the Secrets tab")
    else:
        bot.run(token)
