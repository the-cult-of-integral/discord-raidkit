"""
utils_runtime.py

This namespace contains utility functions for operations regarding the Github repository for Discord Raidkit.
"""

import requests

MY_VERSION = 'v2.5.5'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 
    'X-Requested-With': 'XMLHttpRequest'
}


def latest_version_info() -> tuple[bool, str]:
    """
    Check the latest version of the repo and return a tuple with a boolean and a string.
    
    - The boolean is True if the latest version is the same as the current version, False otherwise.
    - The string is the URL of the latest release.
    """
    rjson = requests.get('https://api.github.com/repos/the-cult-of-integral/discord-raidkit/releases/latest', headers=HEADERS).json()
    tag = rjson['tag_name']
    url = rjson['html_url']
    return (tag == MY_VERSION, url)
