# python bot.py
import os
import discord
import random

from discord.ext import commands
from dotenv import load_dotenv



intents = discord.Intents.default()
intents.message_content = True
#intents.all = True

client = discord.Client(intents=intents)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('Pong!')

"""bot = commands.Bot(intents=intents,command_prefix='!')

@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

"""
client.run(TOKEN)
