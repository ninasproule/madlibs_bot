#!/usr/bin/env python3

import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from storage import get_data, save_data

load_dotenv()

TEMPLATES = get_data()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


#TODO: allow <Multiple Words>
@bot.command(name="new")
async def new_madlib(ctx):
    def check(m):
        return m.content is not None and m.author == ctx.author
    def checkReact(reaction, user):
        return user == ctx.author and (str(reaction) == "✅" or str(reaction) == "❌")
    def checkOneTwo(reaction, user):
        return user == ctx.author and (str(reaction) == "1️⃣" or str(reaction) == "2️⃣")

    selection = await ctx.send("Select 1 to make your own madlib, 2 to view instructions.")
    await selection.add_reaction("1️⃣")
    await selection.add_reaction("2️⃣")

    instructed = False
    reaction = await bot.wait_for("reaction_add", check=checkOneTwo)
    if str(reaction[0]) == "1️⃣":
        instructed = True
    elif str(reaction[0]) == "2️⃣":
        instructed = False

    # make new madlib
    if instructed:
        confirmed = False

        while not confirmed:
            await ctx.send("Go ahead and type your madlib!")
            madlib = await bot.wait_for('message', check=check)
            new_template = str(madlib.content)

            await ctx.send("Here is your madlib:\n\n" + madlib.content)
            confirmation = await ctx.send("Is this correct?")
            await confirmation.add_reaction("✅")
            await confirmation.add_reaction("❌")

            reaction = await bot.wait_for("reaction_add", check=checkReact)
            if str(reaction[0]) =="✅":
                confirmed = True
            elif str(reaction[0]) == "❌":
                confirmed = False


        if confirmed:
            await ctx.send("What would you like to title this madlib?")
            title = await bot.wait_for('message', check=check)
            new_title = str(title.content)

            await ctx.send("Madlib registered!")

            TEMPLATES[new_title] = new_template
            save_data()

    elif not instructed: #view instructions
        await ctx.send("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")
        await ctx.send("Here's an example!\nOnce upon a time, there was a <noun>. It was very <adjective> and always <past-tense-verb> <adverb>")
        await new_madlib(ctx)

    #TODO: cancel option

#TODO: clean up past messages?

#TODO: ignore case of title
@bot.command()
async def play(ctx, *args):
    async def playMadlib(title):
        def check(m):
            return m.content is not None and m.author == ctx.author

        result_madlib = ""
        active_template = TEMPLATES[title]
        await ctx.send("You Got MadLib: " + title)

        for word in active_template.split():
            if word.startswith("<"):
                await ctx.send(str(ctx.author.mention) + ": give me a(n) " + word[1:word.find(">")].upper() + ". ")
                user_input = await bot.wait_for('message', check=check)
                user_word = str(user_input.content)

                result_madlib += user_word
                if word.find(">") < len(word):
                    result_madlib += word[
                                     word.find(">") + 1:]  # for  punctuation and such immediately after the input word
                result_madlib += " "
            else:
                result_madlib += word
                result_madlib += " "

        embed = discord.Embed(title=title, description=result_madlib, colour=discord.Colour.blue())
        await ctx.send(embed=embed)

    if len(args) == 0: #play random madlib
        await playMadlib(random.choice(list(TEMPLATES.keys())))

    elif len(args) < 1: #too many words TODO: make it accept that
        await ctx.send("Please enter the full madlib title in quotes, like this:\n`$play \"The Babysitter\"`")

    else: #play specific madlib
        if args[0] not in TEMPLATES.keys(): #invalid title
            await ctx.send("Please enter a valid madlib title. Use `$list` to see all of the available madlibs.")

        else: #valid title
            await playMadlib(args[0])


@bot.command(name='list')
async def list_titles(ctx):
    """list titles of all madlibs"""
    titles = [str(key) for key in TEMPLATES.keys()]
    titles.sort()

    def slice_per(source, step):
        return [source[i::step] for i in range(step)]
    pages = slice_per(titles, 3)
    def checkReact(reaction, user):
        return user != discord.Member.bot and (str(reaction) == "⬅️" or str(reaction) == "➡️")

    async def listEmbed(pagenum):
        titles = pages[pagenum]
        embed = discord.Embed(title="Available Madlibs:", description="\n".join(titles), colour=discord.Colour.blue())
        embed.set_footer(text="Page " + str(pagenum+1) + "/" + str(len(pages)))

        async def flipPage(pagenum):
            reaction = await bot.wait_for("reaction_add", check=checkReact)
            if (str(reaction[0]) == "⬅️" and pagenum == 0) or (str(reaction[0]) == "➡️" and pagenum == len(pages)-1):
                await flipPage(pagenum)

            elif str(reaction[0]) == "⬅️":
                await list.delete()
                await listEmbed(pagenum-1)

            elif str(reaction[0]) == "➡️":
                await list.delete()
                await listEmbed(pagenum+1)

        list = await ctx.send(embed=embed)
        await list.add_reaction("⬅️")
        await list.add_reaction("➡️")
        await flipPage(pagenum)

    await listEmbed(0)


bot.run(TOKEN)
