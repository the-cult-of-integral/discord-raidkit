"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

dr_repo_utils.py handles the program's interactions with the Discord Raidkit GitHub repository.
dr_repo_utils.py was last updated on 20/04/23 at 21:21 UTC.
"""

import webbrowser

import requests
from colorama import Fore

from utils.io_utils import valid_input

MY_VERSION = 'v2.3.5'
RELEASES_URL = 'https://github.com/the-cult-of-integral/discord-raidkit/releases/latest'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 
    'X-Requested-With': 'XMLHttpRequest'
}


def is_latest_version() -> bool:
    """Returns the latest version of Discord Raidkit."""
    resp = requests.get(RELEASES_URL, headers=HEADERS, stream=False)
    return resp.url.split('/')[-1] == MY_VERSION


def check_for_updates() -> None:
    """
    Checks for updates and prompts the user to update.
    if there is an update available.
    """
    print(f'{Fore.LIGHTWHITE_EX}Checking for updates...{Fore.RESET}')
    
    if is_latest_version():
        return
    
    choice =  valid_input(
f"""{Fore.LIGHTGREEN_EX}New Version Available 
{Fore.LIGHTWHITE_EX}https://github.com/the-cult-of-integral/discord-raidkit/releases/latest/

{Fore.LIGHTGREEN_EX}[1] Open in browser and continue
[2] Open in browser and exit
[3] Continue

>>> {Fore.LIGHTWHITE_EX}""", {'1', '2', '3'}, True)
        
    match choice:
        case '1':
            webbrowser.open(RELEASES_URL)
        case '2':
            webbrowser.open(RELEASES_URL)
            raise SystemExit
        case '3':
            pass
