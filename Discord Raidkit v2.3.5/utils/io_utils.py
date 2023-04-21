"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

io_utils.py provides many i/o methods for the program.
io_utils.py was last updated on 20/04/23 at 21:20 UTC.
"""

import os
import time
from pathlib import Path
from typing import Any, Iterable, List

from colorama import Fore

import utils.log_utils as lu

lu.init()


def valid_input(prompt: str, valid_inputs: Iterable[str], clear_screen: bool) -> str:
    """Prompts the user with a message and accepts input from a list of valid inputs.

    Args:
        prompt (str): the message to display to the user.
        valid_inputs (Iterqble): an iterable of valid inputs.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        str: the user's input.
    """
    while True:
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        if user_input in valid_inputs:
            return user_input
        else:
            print(f'{Fore.LIGHTRED_EX}\nInvalid input. Please try again.{Fore.RESET}')
            if clear_screen:
                time.sleep(1)


def typed_input(prompt: str, input_type: type, must_be_truthy: bool, clear_screen: bool) -> Any:
    """
    Prompts the user with a message and accepts input of the specified type.
    If the input is invalid, the function will prompt the user again.

    Args:
        prompt (str): the message to display to the user.
        input_type (type): the type to convert the user's input to.
        must_be_truthy (bool): whether to require the input to be truthy.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        Any: the user's input, converted to the specified type.

    """
    while True:
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        try:
            typed_input = input_type(user_input)
            if must_be_truthy and not typed_input:
                raise ValueError
        except ValueError:
            print(f'{Fore.LIGHTRED_EX}\nInvalid input. Please try again.{Fore.RESET}')
            if clear_screen:
                time.sleep(1)
        else:
            return typed_input


def csv_input(prompt: str, all_must_be_truthy: bool, clear_screen: bool) -> List[str]:
    """Prompts the user with a message and accepts a comma-separated list of values.

    Args:
        prompt (str): the message to display to the user.
        all_must_be_truthy (bool): whether to require all values to be truthy.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        list: the user's input, converted to a list of values.
    """
    while True:
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        value = input().split(',')
        if all_must_be_truthy and not all(value):
            print(f'{Fore.LIGHTRED_EX}\nInvalid input. Please try again.{Fore.RESET}')
            if clear_screen:
                time.sleep(1)
        else:
            return value


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
        lu.serror(lu.F_IO_UTILS, 'mkfile', f'Uncaught error: {e}')
        return False
