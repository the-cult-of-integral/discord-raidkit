"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

config.py handles the configuration of the program.
config.py was last updated on 21/04/23 at 01:39 UTC.
"""

import os
from typing import Any, Dict, Iterable, List

import ujson

from utils.io_utils import csv_input, typed_input

CONFIG_FILE_PATH = 'config.json'


class DRConfig:
    """A class for managing the Discord Raidkit configuration file.
    """
    __slots__ = ('config')
    
    def __init__(self, config_path: str):
        """Initializes the DRConfig object.

        Args:
            config_path (str): the path to the configuration file.
        """
        self.config = {}
        self.config = self.get_config(config_path)
    
    def get_config(self, config_path: str) -> Dict[str, str | List[str]]:
        """Gets the configuration data from the specified path.
        If the file does not exist, it will be created with data from inputs."""
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config.update(ujson.load(f))
            if self.validate_config(config):
                return config
        config.update(self.prompt_config(True))
        with open(config_path, 'w') as f:
            ujson.dump(config, f, indent=4)
        return config
    
    def validate_config(self, config: Dict) -> bool:
        """Checks whether the config is valid."""
        if not isinstance(config['app_id'], str) or not config['app_id'].strip():
            return False
        if not isinstance(config['token'], str) or not config['token'].strip():
            return False
        if not isinstance(config['prefix'], str) or not config['prefix'].strip():
            return False
        if not isinstance(config['statuses'], list) or not all([s.split() for s in config['statuses']]):
            return False
        return True

    def prompt_config(self, new: bool) -> Dict[str, str | List[str]]:
        """Gets configuration config from the user and returns it as a dictionary.
        """
        if new:
            self['app_id'] = typed_input('Enter the application ID: ', str, True, True)
            self['token'] = typed_input('Enter the Discord bot token: ', str, True, True)
            self['prefix'] = typed_input('Enter the Discord bot prefix: ', str, True, True)
            self['statuses'] = csv_input('Enter the statuses to cycle through, separated by commas: ', True, True)
            return self.config
        
        app_id = typed_input('Enter the application ID (enter nothing to not edit): ', str, False, True)
        if app_id:
            self['app_id'] = app_id
        
        token = typed_input('Enter the Discord bot token (enter nothing to not edit): ', str, False, True)
        if token:
            self['token'] = token
        
        prefix = typed_input('Enter the Discord bot prefix (enter nothing to not edit): ', str, False, True)
        if prefix:
            self['prefix'] = prefix
        
        statuses = csv_input('Enter the statuses to cycle through, separated by commas (enter nothing to not edit): ', False, True)
        if all(statuses):
            self['statuses'] = statuses
        
        with open(CONFIG_FILE_PATH, 'w') as f:
            ujson.dump(self.config, f, indent=4)
        
        return self.config
        
    
    def __getitem__(self, key) -> str | List:
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def __contains__(self, key) -> bool:
        return key in self.config

    def __len__(self) -> int:
        return len(self.config)

    def __iter__(self) -> Iterable:
        return iter(self.config)

    def __next__(self) -> Any:
        return next(self.config)

    def __str__(self) -> str:
        return str(self.config)
    
    def __repr__(self) -> str:
        return repr(self.config)
