# python bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

"""@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)"""

@bot.command()
async def new(ctx):
    await ctx.send("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")


bot.run(TOKEN)
