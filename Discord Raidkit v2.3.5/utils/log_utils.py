"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

log_utils.py handles logging within the program.
log_utils.py was last updated on 20/04/23 at 20:21 UTC.
"""

import logging

F_MAIN = 'main.py'
F__DRUI = 'drui.py'
F_CONFIG = 'config.py'
F_IO_UTILS = '/utils/io_utils.py'
F_OSIRIS = '/tools/osiris.py'
F_RAIDER = '/tools/raider.py'
F_AHELP = '/cogs/anubis/ahelp.py'
F_MODERATION = '/cogs/anubis/moderation.py'
F_RAID_PREVENTION = '/cogs/anubis/raid_prevention.py'
F_SURFING = '/cogs/anubis/surfing.py'
F_NSFW = '/cogs/qetesh/nsfw.py'
F_QHELP = '/cogs/qetesh/qhelp.py'
F_CMDS = '/cogs/shared/cmds.py'
F_HANDLER = '/cogs/shared/handler.py'


def init():
    """Initialize the logger."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(message)s',
                        filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


def sdebug(file_path: str, function: str, message: str):
    """Standard debug message format for Discord Raidkit"""
    logging.debug(f'{file_path} - {function} - {message}')


def sinfo(file_path: str, function: str, message: str):
    """Standard info message format for Discord Raidkit"""
    logging.info(f'{file_path} - {function} - {message}')


def swarning(file_path: str, function: str, message: str):
    """Standard warning message format for Discord Raidkit"""
    logging.warning(f'{file_path} - {function} - {message}')


def serror(file_path: str, function: str, message: str):
    """Standard error message format for Discord Raidkit"""
    logging.error(f'{file_path} - {function} - {message}')


def scritical(file_path: str, function: str, message: str):
    """Standard critical message format for Discord Raidkit"""
    logging.critical(f'{file_path} - {function} - {message}')
