import json

from default_templates import DEFAULT_TEMPLATES

def save_data():
    with open("madlibs.json", mode="w", encoding="utf-8") as write_file:
        json.dump(DEFAULT_TEMPLATES, write_file)

def get_data():
    with open("madlibs.json", mode="r", encoding="utf-8") as read_file:
        return json.load(read_file)