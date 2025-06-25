# python bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.interactions import InteractionResponse

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')



"""def num_emoji_check(reaction, user):
    return str(reaction.emoji) in ['1️⃣', '2️⃣'] and user != bot.user
"""


@bot.command()
async def new(ctx):
    await ctx.send("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")
    message = await ctx.send("Select 1 to make your own madlib, Select 2 to see an example.")
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")

#1️⃣
# 2️⃣
#def check(r, u):
        #return str(r.emoji) == str(emoji) and r.message.id == message.id

   # reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)



bot.run(TOKEN)
