import json
from argparse import ArgumentParser
from pathlib import Path
from pprint import pprint

import requests
from django.conf import settings
from django.core.management import BaseCommand

EMOJI_DATA_URL = "https://raw.githubusercontent.com/iamcal/emoji-data/master/emoji.json"

EMOJI_MAP_PY = Path(settings.BASE_DIR).joinpath("p2kitchen/emojis.py")


def get_emoji_data():
    cached_emojis = Path(settings.BASE_DIR).joinpath(".emojidata.json")
    if cached_emojis.exists():
        with cached_emojis.open("r") as fp:
            emoji_data = json.load(fp)
    else:
        res = requests.get(EMOJI_DATA_URL)
        with cached_emojis.open("w") as fp:
            fp.write(res.text)
        emoji_data = res.json()
    return emoji_data


class Command(BaseCommand):
    """Generates a mapping from emoji short names, used by slack, to unicode strings"""

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, dry_run, *args, **options):
        emoji_data = get_emoji_data()

        emoji_map = {}
        for e in emoji_data:
            for name in e["short_names"]:
                # Split unified hex codepoints by -, parse as hex integers, lookup unicode character and join together
                emoji_map[name] = "".join([chr(int(c, 16)) for c in e["unified"].split("-")])

        if dry_run:
            pprint(emoji_map)
        else:
            with EMOJI_MAP_PY.open("w") as fp:
                fp.write("EMOJI_MAP = {\n")
                lines = [f'    "{short_name}": "{emoji}",\n' for short_name, emoji in emoji_map.items()]
                fp.writelines(lines)
                fp.write("}\n")
