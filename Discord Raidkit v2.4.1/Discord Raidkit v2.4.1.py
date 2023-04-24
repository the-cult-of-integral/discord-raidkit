"""
Discord Raidkit v2.4.1
the-cult-of-integral

Last modified: 2023-04-24 21:07
"""

import asyncio.proactor_events as ape
import logging
import os

import colorama as cama
import discord
import nest_asyncio

import conf.config as conf
import tools.osiris as osiris
import tools.raider as rd
import ui.drui as drui
import utils.async_utils as au
import utils.dr_repo_utils as ru
import utils.log_utils as lu

nest_asyncio.apply()


def run_option(option_id: int, clear_screen: bool) -> None:
    """Run the selected option from the main menu.

    Args:
        option_id (int): the option id to run
        clear_screen (bool, optional): whether to clear the screen. Defaults to True.

    Raises:
        SystemExit: exit the program if an unknown error is raised
    """
    if option_id in {1, 2}:
        logger = logging.getLogger('discord')
        logger.handlers = []
        cfg = conf.DRConfig(clear_screen=clear_screen)
        match option_id:
            case 1: 
                bot_type = rd.Anubis()
            case 2: 
                bot_type = rd.Qetesh()
        try:
            rd.Raider(bot_type, cfg, clear_screen).run(cfg['token'])
        except (discord.errors.HTTPException, discord.errors.LoginFailure):
            if clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            lu.serror(f'Bot failed to login to Discord with token: {cfg["token"]}')
            print('Please check your Discord Bot token is correct and try again.\n')
            print('Enter anything to continue: ', end='')
            input()
        except discord.errors.PrivilegedIntentsRequired:
            if clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            lu.serror('Bot failed to login to Discord due to missing privileged intents.')
            print('Please enable the following intents in the Discord Developer Portal\n')
            print('Enter anything to continue: ', end='')
            input()
        except Exception as e:
            lu.scritical(f'Bot failed to login to Discord with error: {e}')
            raise SystemExit
    elif option_id == 3:
        osiris.Osiris(clear_screen).run()

        
def main(clear_screen: bool):
    """Run the main menu and run the selected option.

    Args:
        clear_screen (bool, optional): whether to clear the screen. Defaults to True.
    """
    ru.check_for_updates()
    while True:
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        option_id = drui.main_menu()
        if option_id == 5:
            break
        run_option(option_id, clear_screen)


if __name__ == '__main__':
    au.silence_event_loop_closed_exception(ape._ProactorBasePipeTransport.__del__)
    lu.init()
    cama.init()
    try:
        clear_screen = True
        os.system('cls' if os.name == 'nt' else 'clear')
        main(clear_screen)
    finally:
        cama.deinit()
