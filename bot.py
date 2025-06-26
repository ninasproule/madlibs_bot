# python bot.py
import os
import discord
import random
import asyncio
import json
from discord.ext import commands
from dotenv import load_dotenv
from discord.interactions import InteractionResponse

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


@bot.command()
async def new(ctx):
    def check(m):
        return m.content is not None and m.author == ctx.author

    await ctx.send("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")
    await ctx.send("Type 1 to make your own madlib, Type 2 to see an example.")

    message = await bot.wait_for('message', check=check)

    if message.content.startswith("1"):  # make new madlib
        await message.channel.send("Go ahead and type your madlib! All in one message, please.")
        madlib = await bot.wait_for('message', check=check)
        new_template = str(madlib.content)

        #await ctx.send("Here is your madlib:\n" + madlib.content + "\nIs this correct?")
        #confirm = await bot.wait_for('message', check=check())

        """def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('👍')"""

        await ctx.send("What would you like to title this madlib?")
        title = await bot.wait_for('message', check=check)
        new_title = str(title.content)

        await ctx.send("Madlib registered!")

        templates[new_title] = new_template
        jsonWrite()


    #await message.add_reaction("1️⃣")
    #await message.add_reaction("2️⃣")

#1️⃣
# 2️⃣


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
                await ctx.send("Give me a(n) " + word[1:word.find(">")].upper() + ". ")
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
        if args[0] not in templates.keys():
            await ctx.send("Please enter a valid madlib title. Use `$list` to see all of the available madlibs.")

        else:
            await playMadlib(args[0])




bot.run(TOKEN)
