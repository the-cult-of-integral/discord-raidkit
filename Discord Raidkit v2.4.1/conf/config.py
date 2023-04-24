"""
Discord Raidkit v2.4.1
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

import pathlib
import typing

import ujson

import utils.io_utils as iou
import utils.log_utils as lu

DEF_CONFIG_FILE_PATH = pathlib.Path('config.json')


class DRConfig:
    """A class to handle the Discord Raidkit configuration
    """
    __slots__ = ('clear_screen', 'config', 'path')
    
    def __init__(self, config_file_path: pathlib.Path = pathlib.Path(DEF_CONFIG_FILE_PATH), clear_screen: bool = True):
        """Initializes the DRConfig class

        Args:
            config_file_path (pathlib.Path): the path to the config file
            clear_screen (bool): whether to allow methods of this class to clear the screen
        """
        self.clear_screen: bool = clear_screen
        self.path: pathlib.Path = config_file_path
        self.config: typing.Dict[str, str | typing.List[str]] = {}
        self.config = self.load_config(config_file_path)
    
    def load_config(self, config_file_path: pathlib.Path) -> typing.Dict[str, str | typing.List[str]]:
        """Loads the config file from the given Path.
        
        If the file does not exist, it will be created 
        and the user will be prompted for the config values.

        Args:
            config_file_path (Path): the path to the config file

        Raises:
            ValueError: raised if the config file is not a JSON file

        Returns:
            Dict[str, str | List[str]]: the config dictionary
        """
        if not config_file_path.suffix == '.json':
            lu.scritical('The config file must be a JSON file')
            raise ValueError('The config file must be a JSON file')
        
        config = {}
        if config_file_path.exists():
            with open(config_file_path, 'r') as config_file:
                config.update(ujson.load(config_file))
            if self.validate_config(config):
                return config
        config.update(self.prompt_config(True))
        with open(config_file_path, 'w') as config_file:
            ujson.dump(config, config_file, indent=4)
        return config
    
    def validate_config(self, config: typing.Dict[str, str | typing.List[str]]) -> bool:
        """Checks whether the given config dictionary is valid

        Args:
            config (Dict[str, str  |  List[str]]): the config dictionary

        Returns:
            bool: True if the config is valid, False otherwise
        """
        if not isinstance(config['app_id'], str) or not config['app_id'].strip():
            return False
        if not isinstance(config['token'], str) or not config['token'].strip():
            return False
        if not isinstance(config['prefix'], str) or not config['prefix'].strip():
            return False
        if not isinstance(config['statuses'], list) or not all([s.split() for s in config['statuses']]):
            return False
        return True
    
    def prompt_config(self, empty: bool = False) -> typing.Dict[str, str | typing.List[str]]:
        """Prompts the user for configuration values

        Args:
            empty (bool, optional): whether you are prompting for empty configuration. 
            Defaults to False.

        Returns:
            Dict[str, str | List[str]]: the config dictionary
        """
        if empty:
            lu.sinfo('No config file found, prompting for config values')
            self['app_id'] = iou.typed_input('Enter the application ID: ', str, True, self.clear_screen)
            self['token'] = iou.typed_input('Enter the bot token: ', str, True, self.clear_screen)
            self['prefix'] = iou.typed_input('Enter the bot prefix: ', str, True, self.clear_screen)
            self['statuses'] = iou.csv_input('Enter the bot statuses: ', True, self.clear_screen)
            return self.config
        
        if app_id := iou.typed_input('Enter the application ID: ', str, False, self.clear_screen):
            self['app_id'] = app_id
        if token := iou.typed_input('Enter the bot token: ', str, False, self.clear_screen):
            self['token'] = token
        if prefix := iou.typed_input('Enter the bot prefix: ', str, False, self.clear_screen):
            self['prefix'] = prefix
        if all(statuses := iou.csv_input('Enter the bot statuses: ', False, self.clear_screen)):
            self['statuses'] = statuses
        
        with open(self.path, 'w') as config_file:
            ujson.dump(self.config, config_file, indent=4)
        
        return self.config

    def __getitem__(self, key) -> str | typing.List[str]:
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def __contains__(self, key) -> bool:
        return key in self.config

    def __len__(self) -> int:
        return len(self.config)

    def __iter__(self) -> typing.Iterable:
        return iter(self.config)

    def __next__(self) -> typing.Any:
        return next(self.config)

    def __str__(self) -> str:
        return str(self.config)
    
    def __repr__(self) -> str:
        return repr(self.config)
