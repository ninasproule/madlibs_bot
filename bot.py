# python bot.py
import os

import discord
import random
import asyncio
import json

from discord import Reaction, Member, User
from discord.ext import commands
from dotenv import load_dotenv


the_babysitter = "The boys can watch an hour of <adjective> television before turning off the <plural-noun> in their room. Make sure they do not watch any violent <plural-noun> or adult <plural-noun>. If there are any phone <plural-noun>, do not identify yourself as the <noun>-sitter. Take a message. Write it <adverb> on the <noun> provided."
the_miner = "Once upon a time, a miner named Thabo worked in a big <PLACE>. Every day, he woke up early to <VERB> for shiny diamonds deep in the ground. Thabo’s helmet was <ADJECTIVE>, and his boots were covered in dirt. He used his pickaxe to <VERB> through the tough rock, <CONJUNCTION> he never gave up. One day, Thabo found a diamond that sparkled so brightly it made the <PLACE> look magical. He was excited <CONJUNCTION> a little nervous because it was the biggest diamond he had ever seen. He placed the diamond in his bag <ADVERB> so it wouldn’t get scratched. When Thabo returned to the surface, he shared the news with his team, <CONJUNCTION> everyone cheered. They knew their hard work had paid off, and Thabo felt <ADJECTIVE> as he walked home."
wedding_vows = "I, <MOVIE-CHARACTER-NAME>, choose you, <TV-CHARACTER-NAME>, to be my spouse for life. Together, we’ll face the ups and <PLURAL-DIRECTION>, always by each other’s side. I offer you my <BODY-PART> and <BODY-ORGAN> as a safe haven filled with love and <NOUN>. I promise to stay <ADJECTIVE> and devoted to you. Like this never-ending <SHAPE>, my love for you will endure <AMOUNT-OF-TIME>. Just as this ring is made of <ADJECTIVE> material, my commitment to you will never <VERB>. With this ring, I <VERB> you."

templates = {"The Babysitter":the_babysitter,
             "The Miner":the_miner,
             "Wedding Vows":wedding_vows}

def jsonWrite():
    with open("madlib_temps.json", mode="w", encoding="utf-8") as write_file:
        json.dump(templates, write_file)

def jsonRead():
    with open("madlib_temps.json", mode="r", encoding="utf-8") as read_file:
        saved_madlibs = json.load(read_file)
    return saved_madlibs


templates = jsonRead()


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


    if instructed:  # make new madlib
        confirmed = False

        while confirmed == False:
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


        if confirmed == True:
            await ctx.send("What would you like to title this madlib?")
            title = await bot.wait_for('message', check=check)
            new_title = str(title.content)

            await ctx.send("Madlib registered!")

            templates[new_title] = new_template
            jsonWrite()

    elif not instructed: #view instructions
        await ctx.send("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")
        #example
        await new_madlib(ctx)

    #TODO: cancel option
    #TODO: example when enter 2
    #TODO: change all options to emojis
    #await message.add_reaction("1️⃣")
    #await message.add_reaction("2️⃣")

#1️⃣
# 2️⃣

#TODO: ignore case of title
@bot.command()
async def play(ctx, *args):
    async def playMadlib(title):
        def check(m):
            return m.content is not None and m.author == ctx.author

        result_madlib = ""
        active_template = templates[title]
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

        await ctx.send(title + ":\n" + result_madlib)

    if len(args) == 0: #play random madlib
        await playMadlib(random.choice(list(templates.keys())))

    elif len(args) < 1: #too many words TODO: make it accept that
        await ctx.send("Please enter the full madlib title in quotes, like this:\n`$play \"The Babysitter\"`")

    else: #play specific madlib
        if args[0] not in templates.keys(): #invalid title
            await ctx.send("Please enter a valid madlib title. Use `$list` to see all of the available madlibs.")

        else: #valid title
            await playMadlib(args[0])


@bot.command(name='list') #list titles of all madlibs
async def list_titles(ctx):
    titles = [str(key) for key in templates.keys()]
    await ctx.send("__Available madlibs:__\n"+", ".join(titles))



bot.run(TOKEN)
