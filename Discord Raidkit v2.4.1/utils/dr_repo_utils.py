"""
Discord Raidkit v2.4.1
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

import webbrowser

import colorama as cama
import requests

import utils.io_utils as iou

MY_VERSION = 'v2.4.0'

RELEASES_URL = 'https://github.com/the-cult-of-integral/discord-raidkit/releases/latest'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36', 
    'X-Requested-With': 'XMLHttpRequest'
}


def is_latest_version() -> bool:
    """Returns True if the latest version of Discord Raidkit matches MY_VERSION."""
    resp = requests.head(RELEASES_URL, headers=HEADERS, allow_redirects=True)
    latest_version_tag = resp.headers.get('Location', '').split('/')[-1]
    return latest_version_tag == MY_VERSION


def check_for_updates() -> None:
    """
    Checks for updates and prompts the user to open 
    the latest release in their browser if there is an update available.
    """
    print(f'{cama.Fore.LIGHTWHITE_EX}Checking for updates...{cama.Fore.RESET}')
    
    if is_latest_version():
        return
    
    choice =  iou.valid_input(
f"""{cama.Fore.LIGHTGREEN_EX}New Version Available 
{cama.Fore.LIGHTWHITE_EX}https://github.com/the-cult-of-integral/discord-raidkit/releases/latest/

{cama.Fore.LIGHTGREEN_EX}[1] Open in browser and continue
[2] Open in browser and exit
[3] Continue

>>> {cama.Fore.LIGHTWHITE_EX}""", [1, 2, 3], int, True)
    
    if choice == 1 or choice == 2:
        webbrowser.open(RELEASES_URL)
        
    if choice == 2:
        raise SystemExit
