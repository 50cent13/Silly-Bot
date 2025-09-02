
import os
import discord
from discord.ext import commands
import asyncio
import random
import json
from datetime import datetime, timedelta
import aiohttp
from flask import Flask, render_template
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return 'Bot is running!', 200

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['!', '?', '.'], intents=intents, help_command=None)

user_data = {}
warnings = {}

def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f, indent=2)

@bot.event
async def on_ready():
    print(f'{bot.user} has logged in!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    global user_data
    user_data = load_user_data()

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="🤖 Bot Commands",
        description="Here are all available commands:",
        color=0x00ff00
    )
    
    embed.add_field(
        name="🎵 Music Commands",
        value="`!play <song>` - Play music\n`!stop` - Stop music\n`!skip` - Skip current song\n`!queue` - Show queue",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Fun Commands",
        value="`!meme` - Random meme\n`!joke` - Random joke\n`!8ball <question>` - Magic 8-ball\n`!roll` - Roll dice",
        inline=False
    )
    
    embed.add_field(
        name="💰 Economy Commands",
        value="`!balance` - Check balance\n`!daily` - Daily coins\n`!work` - Work for coins\n`!gamble <amount>` - Gamble coins",
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Moderation Commands",
        value="`!kick <user>` - Kick user\n`!ban <user>` - Ban user\n`!warn <user>` - Warn user\n`!clear <amount>` - Clear messages",
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Utility Commands",
        value="`!ping` - Check latency\n`!userinfo <user>` - User info\n`!serverinfo` - Server info",
        inline=False
    )
    
    await ctx.send(embed=embed)

music_queue = []
current_song = None

@bot.command()
async def play(ctx, *, song=None):
    if not song:
        await ctx.send("Please specify a song to play!")
        return
    
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel!")
        return
    
    music_queue.append(song)
    embed = discord.Embed(
        title="🎵 Added to Queue",
        description=f"Added **{song}** to the queue!",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command()
async def queue(ctx):
    if not music_queue:
        await ctx.send("Queue is empty!")
        return
    
    queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(music_queue)])
    embed = discord.Embed(
        title="🎵 Music Queue",
        description=queue_list,
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command()
async def skip(ctx):
    if music_queue:
        skipped = music_queue.pop(0)
        await ctx.send(f"⏭️ Skipped: **{skipped}**")
    else:
        await ctx.send("Nothing to skip!")

@bot.command()
async def stop(ctx):
    music_queue.clear()
    await ctx.send("⏹️ Music stopped and queue cleared!")

@bot.command()
async def meme(ctx):
    memes = [
        "https://i.imgflip.com/1bij.jpg",
        "https://i.imgflip.com/2/30b1gx.jpg",
        "https://i.imgflip.com/26am.jpg"
    ]
    embed = discord.Embed(title="🎭 Random Meme", color=0xff6b6b)
    embed.set_image(url=random.choice(memes))
    await ctx.send(embed=embed)

@bot.command()
async def joke(ctx):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What do you call a fake noodle? An impasta!",
        "Why did the math book look so sad? Because it had too many problems!"
    ]
    
    embed = discord.Embed(
        title="😂 Random Joke",
        description=random.choice(jokes),
        color=0xffd93d
    )
    await ctx.send(embed=embed)

@bot.command(name='8ball')
async def eight_ball(ctx, *, question=None):
    if not question:
        await ctx.send("Please ask a question!")
        return
    
    responses = [
        "It is certain", "Reply hazy, try again", "Don't count on it",
        "It is decidedly so", "Ask again later", "My reply is no",
        "Without a doubt", "Better not tell you now", "My sources say no",
        "Yes definitely", "Cannot predict now", "Outlook not so good",
        "You may rely on it", "Concentrate and ask again", "Very doubtful"
    ]
    
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        description=f"**Question:** {question}\n**Answer:** {random.choice(responses)}",
        color=0x000000
    )
    await ctx.send(embed=embed)

@bot.command()
async def roll(ctx, sides=6):
    result = random.randint(1, sides)
    embed = discord.Embed(
        title="🎲 Dice Roll",
        description=f"You rolled a **{result}** out of {sides}!",
        color=0x4285f4
    )
    await ctx.send(embed=embed)

def get_user_balance(user_id):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            'balance': 100,
            'last_daily': None,
            'last_work': None
        }
    return user_data[str(user_id)]['balance']

def set_user_balance(user_id, amount):
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {
            'balance': amount,
            'last_daily': None,
            'last_work': None
        }
    else:
        user_data[str(user_id)]['balance'] = amount
    save_user_data()

@bot.command()
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
    
    balance = get_user_balance(user.id)
    embed = discord.Embed(
        title="💰 Balance",
        description=f"{user.mention} has **{balance}** coins!",
        color=0xffd700
    )
    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):
    user_id = str(ctx.author.id)
    now = datetime.now()
    
    if user_id in user_data and user_data[user_id].get('last_daily'):
        last_daily = datetime.fromisoformat(user_data[user_id]['last_daily'])
        if now - last_daily < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last_daily)
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes = remainder // 60
            await ctx.send(f"You already claimed your daily reward! Try again in {hours}h {minutes}m")
            return
    
    reward = random.randint(50, 200)
    current_balance = get_user_balance(ctx.author.id)
    set_user_balance(ctx.author.id, current_balance + reward)
    
    if user_id not in user_data:
        user_data[user_id] = {'balance': current_balance + reward}
    user_data[user_id]['last_daily'] = now.isoformat()
    save_user_data()
    
    embed = discord.Embed(
        title="🎁 Daily Reward",
        description=f"You claimed **{reward}** coins!\nNew balance: **{current_balance + reward}** coins",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command()
async def work(ctx):
    user_id = str(ctx.author.id)
    now = datetime.now()
    
    if user_id in user_data and user_data[user_id].get('last_work'):
        last_work = datetime.fromisoformat(user_data[user_id]['last_work'])
        if now - last_work < timedelta(hours=1):
            remaining = timedelta(hours=1) - (now - last_work)
            minutes = remaining.seconds // 60
            await ctx.send(f"You're tired! Rest for {minutes} more minutes before working again.")
            return
    
    jobs = [
        ("programmer", 150, 300),
        ("chef", 100, 250),
        ("driver", 80, 200),
        ("teacher", 120, 280),
        ("artist", 90, 220)
    ]
    
    job, min_pay, max_pay = random.choice(jobs)
    payment = random.randint(min_pay, max_pay)
    
    current_balance = get_user_balance(ctx.author.id)
    set_user_balance(ctx.author.id, current_balance + payment)
    
    if user_id not in user_data:
        user_data[user_id] = {'balance': current_balance + payment}
    user_data[user_id]['last_work'] = now.isoformat()
    save_user_data()
    
    embed = discord.Embed(
        title="💼 Work Complete",
        description=f"You worked as a **{job}** and earned **{payment}** coins!\nNew balance: **{current_balance + payment}** coins",
        color=0x4285f4
    )
    await ctx.send(embed=embed)

@bot.command()
async def gamble(ctx, amount=None):
    if amount is None:
        await ctx.send("Please specify an amount to gamble!")
        return
    
    try:
        amount = int(amount)
        if amount <= 0:
            await ctx.send("Amount must be positive!")
            return
    except ValueError:
        await ctx.send("Please enter a valid number!")
        return
    
    current_balance = get_user_balance(ctx.author.id)
    if amount > current_balance:
        await ctx.send("You don't have enough coins!")
        return
    
    if random.random() < 0.45:  
        winnings = amount * 2
        set_user_balance(ctx.author.id, current_balance + amount)
        embed = discord.Embed(
            title="🎰 Gambling - WIN!",
            description=f"You won **{winnings}** coins!\nNew balance: **{current_balance + amount}** coins",
            color=0x00ff00
        )
    else:
        set_user_balance(ctx.author.id, current_balance - amount)
        embed = discord.Embed(
            title="🎰 Gambling - LOSS!",
            description=f"You lost **{amount}** coins!\nNew balance: **{current_balance - amount}** coins",
            color=0xff0000
        )
    
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    embed = discord.Embed(
        title="👢 Member Kicked",
        description=f"{member.mention} has been kicked.\nReason: {reason}",
        color=0xff6b6b
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="🔨 Member Banned",
        description=f"{member.mention} has been banned.\nReason: {reason}",
        color=0xff0000
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    user_id = str(member.id)
    if user_id not in warnings:
        warnings[user_id] = []
    
    warnings[user_id].append({
        'reason': reason,
        'moderator': str(ctx.author),
        'timestamp': datetime.now().isoformat()
    })
    
    embed = discord.Embed(
        title="⚠️ Member Warned",
        description=f"{member.mention} has been warned.\nReason: {reason}\nTotal warnings: {len(warnings[user_id])}",
        color=0xffa500
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    if amount > 100:
        await ctx.send("Cannot delete more than 100 messages at once!")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="🧹 Messages Cleared",
        description=f"Deleted {len(deleted) - 1} messages!",
        color=0x00ff00
    )
    
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: **{latency}ms**",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    embed = discord.Embed(
        title=f"👤 User Info - {member.display_name}",
        color=member.color
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="Roles", value=len(member.roles), inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"🏰 Server Info - {guild.name}",
        color=0x4285f4
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
    embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Created", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore command not found errors
    else:
        print(f"Error: {error}")

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN_PY")
    if not token:
        print("Error: BOT_TOKEN_PY not found in environment variables")
        print("Please set BOT_TOKEN_PY in the Secrets tab")
        exit(1)
    
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080))
    flask_thread.daemon = True
    flask_thread.start()
    
    bot.run(token)
