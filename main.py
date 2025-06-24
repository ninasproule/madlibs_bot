#Nina Sproule 2025
import random
import json

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


make_or_play = input("Press 1 to make your own madlib. Press 2 to play a random madlib.")
while make_or_play!="1" and make_or_play!="2":
    print("Invalid choice.")
    make_or_play = input("Press 1 to make your own madlib. Press 2 to play a random madlib.")


if make_or_play == "2": #"Play random" option
    result_madlib = ""
    title, active_template = random.choice(list(templates.items()))
    print("You Got MadLib: " + title)

    for word in active_template.split():
        if word.startswith("<"):
            user_word = input("Give me a(n) " + word[1:word.find(">")].upper() + ". ")
            result_madlib += user_word
            if word.find(">") < len(word):
                result_madlib += word[word.find(">") + 1:] #for  punctuation and such immediately after the input word
            result_madlib += " "
        else:
            result_madlib += word
            result_madlib += " "


    print(title + ": " + result_madlib)

if make_or_play == "1": #"Make your own" option
    print("To make your own madlib, type a story. Wherever you want the player to enter a word, put the type of word inside <>, like <NOUN> or <ADJECTIVE>.")
    #example = input("Do you want to see an example? (y/n)")

    new_template = input()
    #check is this correct?

    new_title = input("What would you like to title this madlib? ")
    templates[new_title] = new_template
    jsonWrite()

