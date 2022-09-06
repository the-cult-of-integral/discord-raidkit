"""
Discord Raidkit v2.3.1 — "The trojan horse of discord raiding"
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

display.py handles the user interface aspect of Discord Raidkit, showing any information to the user.
display.py was last updated on 06/09/22 at 18:18.
"""

from colorama import Back, Fore, Style, init

from constants import CURRENT_VERSION
from utils import clear

init()

THEMES = {
    "default": {
        "primary": Fore.CYAN,
        "secondary": Fore.BLUE,
        "tertiary": Fore.GREEN,
        "important": [Fore.LIGHTRED_EX, Back.RED]
    },
    "fire": {
        "primary": Fore.YELLOW,
        "secondary": Fore.LIGHTRED_EX,
        "tertiary": Fore.RED,
        "important": [Fore.LIGHTBLUE_EX, Back.BLUE]
    },
    "storm": {
        "primary": Fore.BLUE,
        "secondary": Fore.CYAN,
        "tertiary": Fore.YELLOW,
        "important": [Fore.LIGHTMAGENTA_EX, Back.MAGENTA]
    },
    "magic": {
        "primary": Fore.LIGHTMAGENTA_EX,
        "secondary": Fore.YELLOW,
        "tertiary": Fore.MAGENTA,
        "important": [Fore.GREEN, Back.GREEN]
    }
}


def change_brightness(brightness: str = '') -> None:
    if brightness == 'bright':
        print(Style.BRIGHT)
    elif brightness == 'dim':
        print(Style.DIM)
    else:
        print(Style.NORMAL)
    return


def validate_theme(theme: str) -> str:
    if theme not in THEMES.keys():
        return 'default'
    else:
        return theme


def show_main_raidkit(theme: str, prefix: str, hint: str = '') -> None:
    clear()
    theme = validate_theme(theme)
    print(f'''{THEMES[theme]["secondary"]}
Discord Raidkit {CURRENT_VERSION}
© 2022 the-cult-of-integral

{THEMES[theme]["tertiary"]}
██████╗  █████╗ ██╗██████╗ ██╗  ██╗██╗████████╗
██╔══██╗██╔══██╗██║██╔══██╗██║ ██╔╝██║╚══██╔══╝
██████╔╝███████║██║██║  ██║█████╔╝ ██║   ██║   
██╔══██╗██╔══██║██║██║  ██║██╔═██╗ ██║   ██║   
██║  ██║██║  ██║██║██████╔╝██║  ██╗██║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   
                                               
{THEMES[theme]["primary"]}{prefix}nick_all <nickname> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}nickname every user in a server to <nickname>
{THEMES[theme]["primary"]}{prefix}msg_all <message> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}message every user in a server with <message>
{THEMES[theme]["primary"]}{prefix}spam <message> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}spam message every text channel in a server with <message>
{THEMES[theme]["primary"]}{prefix}cpurge {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}delete every channel in a server
{THEMES[theme]["primary"]}{prefix}cflood <amount> <name> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}create <amount> text channels named <name>
{THEMES[theme]["primary"]}{prefix}raid <role name> <nickname> <amount> <name> <message> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}role and nick all users in a server, then run cflood and spam
{THEMES[theme]["primary"]}{prefix}admin <member> <role name> {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}give a user an admin role named <role name>; by default, the user is the command issuer
{THEMES[theme]["primary"]}{prefix}nuke {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}ball all members, then delete all channels, roles, emojis, and stickers,
{THEMES[theme]["primary"]}{prefix}mass nuke{THEMES[theme]["tertiary"]} - {THEMES[theme]["secondary"]}nuke every server the bot is currently in, one by one
{THEMES[theme]["primary"]}{prefix}leave <server name | server id>{THEMES[theme]["tertiary"]} - {THEMES[theme]["secondary"]}get the bot to leave a server by its name or id
{THEMES[theme]["primary"]}{prefix}mass leave {THEMES[theme]["tertiary"]}- {THEMES[theme]["secondary"]}get the bot to leave every server it is in

{THEMES[theme]["important"][0]}{hint}

{THEMES[theme]["important"][1]}{Fore.LIGHTWHITE_EX}Warning: make sure your bot's role is higher than any roles you wish to affect!{Back.RESET}''')
    return


def show_sync_msg(theme: str) -> None:
    clear()
    theme = validate_theme(theme)
    print(f'''
{THEMES[theme]["primary"]}Syncing Bot Tree; please wait...
{THEMES[theme]["secondary"]}(For Raidkits spanning a large number of servers, this may take from several minutes to hours. . .)''')
    return


def show_welcome_menu(theme: str) -> None:
    clear()
    theme = validate_theme(theme)
    print(f'''{THEMES[theme]["secondary"]}Welcome to Discord Raidkit {CURRENT_VERSION}!

{THEMES[theme]["primary"]}This program is a collection of tools for discord, including raiders and account hackers.
This program is maintained by https://github.com/the-cult-of-integral and is open source! {THEMES[theme]["important"][0]}

{THEMES[theme]["secondary"]}This program is licensed under the GNU General Public License v2.0.



[{THEMES[theme]["primary"]}1{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Anubis - a malicious discord bot that contains many helpful moderation commands for trust.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}2{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Qetesh - a malicious discord bot that contains many NSFW commands for trust.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}3{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Osiris - generate token grabbers, find information about a token, log into accounts, and nuke accounts.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}4{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Theme - change program theme.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}5{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Exit.


{THEMES[theme]["primary"]}Please select an option: {Fore.RESET}''', end='')
    return


def show_invalid_token(theme: str) -> None:
    clear()
    theme = validate_theme(theme)

    print(f'''{THEMES[theme]["important"][0]}An invalid token has been provided.

{THEMES[theme]["primary"]}This program will now exit, as discord does not allow bots to reconnect after a connection failure until the program is restarted.

{THEMES[theme]["secondary"]}Convinced your token is right? Submit an issue at {THEMES[theme]["tertiary"]}https://github.com/the-cult-of-integral/discord-raidkit/issues {THEMES[theme]["secondary"]}.

{Fore.RESET}''')
    return


def show_osiris_screen(theme: str, hint: str) -> None:
    clear()
    theme = validate_theme(theme)

    print(f'''{THEMES[theme]["secondary"]}
Discord Raidkit {CURRENT_VERSION}
© 2022 the-cult-of-integral

{THEMES[theme]["tertiary"]}
 ██████╗ ███████╗██╗██████╗ ██╗███████╗
██╔═══██╗██╔════╝██║██╔══██╗██║██╔════╝
██║   ██║███████╗██║██████╔╝██║███████╗
██║   ██║╚════██║██║██╔══██╗██║╚════██║
╚██████╔╝███████║██║██║  ██║██║███████║
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                       

{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}1{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Generate a user authentication token grabber.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}2{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Find information about a user by user authentication token.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}3{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Log into a user account by user authentication token.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}4{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Remove all friends from a user account.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}5{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Nuke a user account by user authentication token.
{THEMES[theme]["secondary"]}[{THEMES[theme]["primary"]}6{THEMES[theme]["secondary"]}] {THEMES[theme]["tertiary"]}Exit.

{THEMES[theme]["important"][0]}{hint}

{THEMES[theme]["primary"]}Please select an option: {Fore.RESET}''', end='')

    return


def show_cfg_screen(config: dict) -> None:
    """
    Display the configuration screen.
    """
    clear()

    theme = validate_theme(config["theme"])

    screen = f'''{THEMES[theme]["secondary"]}
Discord Raidkit {CURRENT_VERSION}
© 2022 the-cult-of-integral

{THEMES[theme]["tertiary"]}
 ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ 

{THEMES[theme]["important"][0]}* configuration shared between Anubis and Qetesh !

{THEMES[theme]["primary"]}
[1] Token '''

    if a := config["token"]:
        screen += f'{THEMES[theme]["secondary"]}<set>{THEMES[theme]["primary"]}'
    else:
        screen += f'{THEMES[theme]["important"][0]}<not set!>{THEMES[theme]["primary"]}'

    screen += f'''
[2] App ID '''

    if b := config["app_id"]:
        screen += f'{THEMES[theme]["secondary"]}<set>{THEMES[theme]["primary"]}'
    else:
        screen += f'{THEMES[theme]["important"][0]}<not set!>{THEMES[theme]["primary"]}'

    screen += f'''
[3] Prefix '''

    if c := config["prefix"]:
        screen += f'{THEMES[theme]["secondary"]}<set>{THEMES[theme]["primary"]}'
    else:
        screen += f'{THEMES[theme]["important"][0]}<not set!>{THEMES[theme]["primary"]}'

    screen += f'''
[4] Statuses '''
    if d := all(s for s in config["statuses"]):
        screen += f'{THEMES[theme]["secondary"]}<set>{THEMES[theme]["primary"]}'
    else:
        screen += f'{THEMES[theme]["important"][0]}<not set!>{THEMES[theme]["primary"]}'

    screen += f'''
[5] Verbose '''

    if e := str(config["verbose"]):
        screen += f'{THEMES[theme]["secondary"]}<set>'
    else:
        screen += f'{THEMES[theme]["important"][0]}<not set!>'

    if a and b and c and d and e:
        screen += f'''{THEMES[theme]["primary"]}

[6] Continue
[7] Exit

{Fore.RESET}'''
    else:
        screen += f'''{Fore.LIGHTBLACK_EX}

[6] <configuration not ready>{THEMES[theme]["primary"]}
[7] Exit

{Fore.RESET}'''
    print(screen)
    return
