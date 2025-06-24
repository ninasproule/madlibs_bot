#Nina Sproule 2025

template = "The boys can watch an hour of <adjective> television before turning off the <pluralnoun> in their room. Make sure they do not watch any violent <pluralnoun> or adult <pluralnoun>. If there are any phone <pluralnoun>, do not identify yourself as the <noun>-sitter. Take a message. Write it <adverb> on the <noun> provided."

madlib = ""

for word in template.split():
    if word.startswith("<"):
        user_word = input("Give me a(n) " + word[1:word.find(">")]+ ". ")
        madlib += user_word
        if word.find(">") < len(word):
            madlib += word[word.find(">")+1:] #for  punctuation and such immediately after the input word
        madlib += " "
    else:
        madlib += word
        madlib += " "

print(madlib)