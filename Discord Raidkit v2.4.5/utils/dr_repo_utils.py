"""
Discord Raidkit v2.4.5
the-cult-of-integral

Last modified: 2024-04-07 05:19
"""

import webbrowser

import colorama as cama
import requests

import utils.io_utils as iou

MY_VERSION = 'v2.4.5'

RELEASES_URL = 'https://github.com/the-cult-of-integral/discord-raidkit/releases/latest'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 
    'X-Requested-With': 'XMLHttpRequest'
}


def get_latest_version_tag() -> str:
    """Returns the latest version tag from the GitHub API."""
    return requests.get('https://api.github.com/repos/the-cult-of-integral/discord-raidkit/releases/latest', headers=HEADERS).json()['tag_name']

def check_for_updates() -> None:
    """
    Checks for updates and prompts the user to open 
    the latest release in their browser if there is an update available.
    """
    print(f'{cama.Fore.LIGHTWHITE_EX}Checking for updates...{cama.Fore.RESET}')
    
    if (tag := get_latest_version_tag()) == MY_VERSION:
        return
    
    choice =  iou.valid_input(
f"""{cama.Fore.LIGHTGREEN_EX}New Version Available 
{cama.Fore.LIGHTWHITE_EX}https://github.com/the-cult-of-integral/discord-raidkit/releases/{tag}/

{cama.Fore.LIGHTGREEN_EX}[1] Open in browser and continue
[2] Open in browser and exit
[3] Continue

>>> {cama.Fore.LIGHTWHITE_EX}""", [1, 2, 3], int)
    
    if choice == 1 or choice == 2:
        webbrowser.open(RELEASES_URL)
        
    if choice == 2:
        raise SystemExit
