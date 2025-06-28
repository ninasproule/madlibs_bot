import json
import os.path

from default_templates import DEFAULT_TEMPLATES

MADLIBS_FILEPATH = "madlibs.json"

def save_data(templates):
    with open(MADLIBS_FILEPATH, mode="w", encoding="utf-8") as f:
        json.dump(templates, f)

def get_data():
    if os.path.isfile(MADLIBS_FILEPATH):
        with open(MADLIBS_FILEPATH, mode="r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_data(DEFAULT_TEMPLATES)
        return DEFAULT_TEMPLATES