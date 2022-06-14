"""
Discord Raidkit v2.1.0 by the-cult-of-integral
"The legitimate raidkit"
Last updated: 14/06/2022
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup


def get_latest_release() -> str:
    """Returns the latest release of Discord Raidkit

    Returns:
        str: a.b.c (e.g. 2.0.1)
    """
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    url = f"\
https://github.com/the-cult-of-integral/discord-raidkit/releases/latest"
    r = requests.get(url, headers=headers)
    soup = str(BeautifulSoup(r.text, 'html.parser'))
    latest_release = re.search(
        r"Release Discord Raidkit v(\d.\d.\d)", soup).group(1)
    return latest_release
        

def do_config_setup(config_path) -> dict:
    """Performs the initial check and setup for Discord Raidkit configuration.

    Args:
        config_path (str): path to configuration JSON file.

    Returns:
        dict: the contents of the configuration JSON file as a dict.
    """
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        temp = {"token": "", "prefix": "", "theme": "dark"}
        with open(config_path, "w") as f:
            json.dump(temp, f, indent=4)
        return temp


def write_config(config_path, token=None, prefix=None, theme=None) -> None:
    temp = do_config_setup(config_path)
    if token:
        temp["token"] = token
    if prefix:
        temp["prefix"] = prefix
    if theme:
        temp["theme"] = theme
    with open(config_path, "w") as f:
        json.dump(temp, f, indent=4)
    return

