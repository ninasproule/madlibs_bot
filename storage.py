import json

from default_templates import TEMPLATES

def jsonWrite():
    with open("madlib_temps.json", mode="w", encoding="utf-8") as write_file:
        json.dump(TEMPLATES, write_file)

def jsonRead():
    with open("madlib_temps.json", mode="r", encoding="utf-8") as read_file:
        saved_madlibs = json.load(read_file)
    return saved_madlibs