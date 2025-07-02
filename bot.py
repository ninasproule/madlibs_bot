#!/usr/bin/env python3

import os
import random
import re
from string import capwords

import discord
from discord.ext import commands
from dotenv import load_dotenv

from storage import get_data, save_data

load_dotenv()

TEMPLATES = get_data()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '&'
CANCEL_WORD = PREFIX + "cancel"
TIMEOUT_SECONDS = 60
TITLES_PER_PAGE = 3


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    game = discord.Game("your madlibs!\n&help to get started")
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(name="new")
async def new_madlib(ctx):
    """user create new madlib template"""

    def check(m):
        return m.content is not None and m.author == ctx.author
    def check_reacts(reaction, user):
        return user == ctx.author and (str(reaction) == "✅" or str(reaction) == "❌")
    def check_number_reacts(reaction, user):
        return user == ctx.author and (str(reaction) == "1️⃣" or str(reaction) == "2️⃣" or str(reaction) == "3️⃣")

    embed = discord.Embed(
        title="Create New Madlib",
        description="1️⃣ — Make your own madlib\n\n2️⃣ — View instructions\n\n3️⃣ — Cancel",
        colour=discord.Colour.green()
    )
    selection = await ctx.send(embed=embed)
    await selection.add_reaction("1️⃣")
    await selection.add_reaction("2️⃣")
    await selection.add_reaction("3️⃣")

    instructed = False
    reaction = await bot.wait_for("reaction_add", check=check_number_reacts, timeout=TIMEOUT_SECONDS)
    if str(reaction[0]) == "1️⃣":
        instructed = True
    elif str(reaction[0]) == "2️⃣":
        instructed = False
    elif str(reaction[0]) == "3️⃣":
        await cancel(ctx)
        return

    # make new madlib
    if instructed:
        confirmed = False

        while not confirmed:
            await ctx.send("Go ahead and type your madlib!")
            madlib = await bot.wait_for('message', check=check, timeout=TIMEOUT_SECONDS)
            new_template = str(madlib.content)

            if new_template == CANCEL_WORD:
                return

            embed = discord.Embed(
                title="Your Madlib Preview",
                description=madlib.content,
                colour=discord.Colour.orange()
            )
            await ctx.send(embed=embed)

            confirmation_embed = discord.Embed(
                title="Confirmation",
                description="Is this madlib correct?\n\n✅ - Yes, save it\n\n❌ - No, let me try again",
                colour=discord.Colour.yellow()
            )
            confirmation = await ctx.send(embed=confirmation_embed)
            await confirmation.add_reaction("✅")
            await confirmation.add_reaction("❌")

            reaction = await bot.wait_for("reaction_add", check=check_reacts, timeout=TIMEOUT_SECONDS)
            if str(reaction[0]) =="✅":
                confirmed = True
            elif str(reaction[0]) == "❌":
                confirmed = False


        if confirmed:
            await ctx.send("What would you like to title this madlib?")
            title = await bot.wait_for('message', check=check, timeout=TIMEOUT_SECONDS)
            new_title = str(title.content).lower()

            if new_title == CANCEL_WORD:
                return

            await ctx.send("Madlib registered!")

            TEMPLATES[new_title] = new_template
            save_data(TEMPLATES)

    #view instructions
    elif not instructed:
        instructions_embed = discord.Embed(
            title="How to Create a Madlib",
            description="To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside `<>`, like `<NOUN>` or `<ADJECTIVE>`.",
            colour=discord.Colour.blue()
        )
        instructions_embed.add_field(
            name="Example:",
            value="Once upon a time, there was a `<noun>`. It was very `<adjective>` and always `<past tense verb>` `<adverb>`",
            inline=False
        )
        await ctx.send(embed=instructions_embed)
        await new_madlib(ctx)

    #TODO: cancel option


@bot.command()
async def play(ctx, *args):
    """play a madlib- random if no args given, otherwise, args are the title of madlib to play"""

    async def play_madlib(title):
        def check(m):
            return m.content is not None and m.author == ctx.author

        result_madlib = ""
        active_template = TEMPLATES[title]
        await ctx.send("You Got MadLib: " + capwords(title))

        for chunk in re.split(r'(<.*?>)', active_template):
            if chunk.startswith("<"):
                await ctx.send(str(ctx.author.mention) + ": give me a(n) " + chunk.lstrip("<").rstrip(">").upper())
                user_input = await bot.wait_for('message', check=check, timeout=TIMEOUT_SECONDS)
                user_word = str(user_input.content)

                if user_word == CANCEL_WORD:
                    return

                result_madlib += user_word
            else:
                result_madlib += chunk

        embed = discord.Embed(title=capwords(title), description=result_madlib, colour=discord.Colour.blue())
        await ctx.send(embed=embed)

    #play random madlib
    if len(args) == 0:
        await play_madlib(random.choice(list(TEMPLATES.keys())))
        return

    args = " ".join(args).lower()

    #play specific madlib
    if not (args in TEMPLATES.keys()):
        await ctx.send(f"Please enter a valid madlib title. Use `{PREFIX}list` to see all of the available madlibs.")

    else:
        await play_madlib(args)


@bot.command(name='list')
async def list_titles(ctx):
    """list titles of all madlibs"""

    titles = [str(key) for key in TEMPLATES.keys()]
    titles.sort()

    def chunk_list(source, chunk_size):
        return [source[i:i + chunk_size] for i in range(0, len(source), chunk_size)]
    pages = chunk_list(titles, TITLES_PER_PAGE)

    def check_reacts(reaction, user):
        return user != discord.Member.bot and (str(reaction) == "⬅️" or str(reaction) == "➡️")

    def create_embed(pagenum):
        titles = [capwords(title) for title in pages[pagenum]]
        embed = discord.Embed(title="Available Madlibs:", description="\n".join(titles), colour=discord.Colour.blue())
        embed.set_footer(text="Page " + str(pagenum+1) + "/" + str(len(pages)))
        return embed

    #send initial embed
    current_page = 0
    embed = create_embed(current_page)
    message = await ctx.send(embed=embed)
    await message.add_reaction("⬅️")
    await message.add_reaction("➡️")

    #handle pagination
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=check_reacts, timeout=TIMEOUT_SECONDS)

            if str(reaction) == "⬅️" and current_page > 0:
                current_page -= 1
                embed = create_embed(current_page)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            elif str(reaction) == "➡️" and current_page < len(pages) - 1:
                current_page += 1
                embed = create_embed(current_page)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)

            else:
                #remove reaction if it's not a valid page change
                await message.remove_reaction(reaction, user)

        except:
            #timeout or other error, stop pagination
            break


@bot.command()
async def cancel(ctx):
    """Handle cancel command - cancels any running madlib operations"""
    embed = discord.Embed(
        title="Cancelled",
        description="Any running madlib operations have been cancelled.",
        colour=discord.Colour.red()
    )
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    """Display all available commands and their descriptions"""

    embed = discord.Embed(
        title="MadLibs Bot Commands",
        description="Here are all the available commands:",
        colour=discord.Colour.purple()
    )

    embed.add_field(
        name=f"{PREFIX}play [title]",
        value="Play a madlib! Use without title for random, or specify a title to play a specific one.",
        inline=False
    )

    embed.add_field(
        name=f"{PREFIX}new",
        value="Create a new madlib template. Follow the prompts to add your own story!",
        inline=False
    )

    embed.add_field(
        name=f"{PREFIX}list",
        value="View all available madlib titles in a paged list.",
        inline=False
    )

    embed.add_field(
        name=f"{PREFIX}cancel",
        value="Cancel any currently running madlib operations.",
        inline=False
    )

    embed.add_field(
        name=f"{PREFIX}help",
        value="Show this help message with all available commands.",
        inline=False
    )

    embed.set_footer(text="Use these commands to have fun with madlibs!")

    await ctx.send(embed=embed)


bot.run(TOKEN)
