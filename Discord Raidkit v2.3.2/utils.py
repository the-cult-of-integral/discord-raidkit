"""
utils.py contains useful utility functions.
utils.py was last updated on 18/09/22 at 12:26.
"""

import logging
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init()

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


def clear() -> None:
    """A shortcut for os.system('cls' if os.name == 'nt' else 'clear')
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def check_update(version: str) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 "
                      "Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = f"https://github.com/the-cult-of-integral/discord-raidkit/releases/latest"
    clear()
    print(f"{Fore.BLUE}Checking for updates. . .")
    r = requests.get(url, headers=headers)
    clear()
    soup = str(BeautifulSoup(r.text, "html.parser"))
    s1 = re.search("<title>", soup)
    s2 = re.search("·", soup)
    result = soup[s1.end():s2.start()]
    if version not in result:
        s1 = re.search('originating_url":"', soup)
        s2 = re.search('","user_id":null', soup)
        update_link = soup[s1.end():s2.start()]
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f"""
███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                                  
{Fore.LIGHTRED_EX}There has been a brand new update to the discord raidkit.
{Fore.LIGHTBLUE_EX}{update_link}


{Fore.RESET}Enter anything to continue: """.replace("█", f"{Fore.YELLOW}█{Fore.LIGHTGREEN_EX}"), end='')
        input()
        return
