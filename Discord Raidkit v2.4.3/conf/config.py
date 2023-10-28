"""
Discord Raidkit v2.4.3
the-cult-of-integral

Last modified: 2023-04-29 18:16
"""

import os
import pathlib
import re
import typing

import colorama as cama
import ujson
import utils.io_utils as iou
import utils.log_utils as lu

DEF_CONFIG_FILE_PATH = pathlib.Path('config.json')
DEF_PROXY_FILE_PATH = pathlib.Path('proxies.json')


class DRConfig:
    """A class to handle the Discord Raidkit configuration
    """
    __slots__ = ('clear_screen', 'config', 'path')
    
    def __init__(self, config_file_path: pathlib.Path = pathlib.Path(DEF_CONFIG_FILE_PATH)):
        """Initializes the DRConfig class

        Args:
            config_file_path (pathlib.Path): the path to the config file
            clear_screen (bool): whether to allow methods of this class to clear the screen
        """
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
            self['app_id'] = iou.typed_input('Enter the application ID: ', str, True)
            self['token'] = iou.typed_input('Enter the bot token: ', str, True)
            self['prefix'] = iou.typed_input('Enter the bot prefix: ', str, True)
            self['statuses'] = iou.csv_input('Enter the bot statuses: ', True)
            return self.config
        
        if app_id := iou.typed_input('Enter the application ID: ', str, False):
            self['app_id'] = app_id
        if token := iou.typed_input('Enter the bot token: ', str, False):
            self['token'] = token
        if prefix := iou.typed_input('Enter the bot prefix: ', str, False):
            self['prefix'] = prefix
        if all(statuses := iou.csv_input('Enter the bot statuses: ', False)):
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


class ProxyConfig:
    """A class to manage proxy configurations.
    """
    __slots__ = ('path',)

    PROTOCOLS = ('https', 'http')

    def __init__(self, proxy_file_path: pathlib.Path = pathlib.Path(DEF_PROXY_FILE_PATH)):
        """Initialize the ProxyConfig with a specified file path.
        """
        self.path: pathlib.Path = proxy_file_path
        self.__init_proxy_file()

    def __init_proxy_file(self) -> None:
        """Initialize the proxy file with default values if it doesn't exist.
        """
        if not self.path.exists():
            self.__write_to_proxy_file({'is_using_proxies': False, 'http': [], 'https': []})

    def __write_to_proxy_file(self, data: dict) -> None:
        """Write the given data to the proxy file.
        """
        with open(self.path, 'w') as proxy_file:
            ujson.dump(data, proxy_file, indent=4)

    def __read_from_proxy_file(self) -> dict:
        """Read the data from the proxy file and return it as a dictionary.
        """
        with open(self.path, 'r') as proxy_file:
            return ujson.load(proxy_file)

    def run_proxy_editor(self) -> None:
        """Run the proxy editor, which allows for interactive editing of the proxy settings.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        self.__init_proxy_file()
        opts = [
            iou.MenuOption('View Proxies', 'View the proxies in the proxy collection', self.view_proxies),
            iou.MenuOption('Toggle Proxies', 'Toggle whether requests should use proxies', self.toggle_proxies),
            iou.MenuOption('Add HTTP', 'Add a HTTP proxy to the proxy collection', self.add_http_proxy),
            iou.MenuOption('Add HTTPS', 'Add a HTTPS proxy to the proxy collection', self.add_https_proxy),
            iou.MenuOption('Remove HTTP', 'Remove a HTTP proxy from the proxy collection', self.remove_http_proxy),
            iou.MenuOption('Remove HTTPS', 'Remove a HTTPS proxy from the proxy collection', self.remove_https_proxy),
            iou.MenuOption('Clear HTTP', 'Clear the HTTP proxy collection', self.clear_http_proxies),
            iou.MenuOption('Clear HTTPS', 'Clear the HTTPS proxy collection', self.clear_https_proxies),
            iou.MenuOption('Clear All', 'Clear the proxy collection', self.clear_all_proxies),
            iou.MenuOption('Back', 'Leave the proxy menu', lambda: iou.EXIT)
        ]
        menu = iou.NumberedMenu(
            'Proxy Editor\n\n',
            opts,
            pcolor=cama.Fore.MAGENTA,
            scolor=cama.Fore.LIGHTMAGENTA_EX,
            auto_append_exit=False,
            do_name_and_desc=False
        )
        menu.run()

    def is_using_proxies(self) -> bool:
        """Returns a boolean indicating whether the system is currently set to use proxies.
        """
        return self.__read_from_proxy_file()['is_using_proxies']

    def view_proxies(self) -> str:
        """Prints the current list of HTTP and HTTPS proxies, and then returns an empty string.
        """
        proxies = self.__read_from_proxy_file()
        print(f'{cama.Fore.MAGENTA}HTTP Proxies:\n{cama.Fore.LIGHTMAGENTA_EX}' + '\n'.join(proxies['http']) +
              f'\n\n{cama.Fore.MAGENTA}HTTPS Proxies:\n{cama.Fore.LIGHTMAGENTA_EX}' + '\n'.join(proxies['https']))
        input(f'\n\n{cama.Fore.LIGHTWHITE_EX}Enter anything to go back: ')
        return ''

    def toggle_proxies(self) -> str:
        """Toggles the use of proxies on or off and returns a message indicating the new state.
        """
        proxies = self.__read_from_proxy_file()
        proxies['is_using_proxies'] = not proxies['is_using_proxies']
        self.__write_to_proxy_file(proxies)
        return f'Proxies are now {"enabled" if proxies["is_using_proxies"] else "disabled"}'
    
    def __add_proxy(self, protocol: str) -> str:
        """Add a proxy of the given protocol (HTTP or HTTPS) and return a status message.
        """
        proxy = iou.typed_input(f'Enter the {protocol.upper()} proxy to add: ', str, False)
        if not proxy:
            return ''
        if not self.validate_proxy(proxy):
            return f'Invalid {protocol.upper()} proxy format: {proxy}\nFormat should be: <ip>:<port>'
        proxies = self.__read_from_proxy_file()
        proxies[protocol].append(proxy)
        self.__write_to_proxy_file(proxies)
        return f'Added {protocol.upper()} proxy: {proxy}'

    def add_http_proxy(self) -> str:
        return self.__add_proxy('http')

    def add_https_proxy(self) -> str:
        return self.__add_proxy('https')

    def __remove_proxy(self, protocol: str) -> str:
        """Rremove a proxy of the given protocol (HTTP or HTTPS) and return a status message.
        """
        proxy = iou.typed_input(f'Enter the {protocol.upper()} proxy to remove: ', str, False)
        if not proxy:
            return ''
        proxies = self.__read_from_proxy_file()
        if proxy in proxies[protocol]:
            proxies[protocol].remove(proxy)
            self.__write_to_proxy_file(proxies)
            return f'Removed {protocol.upper()} proxy: {proxy}'
        return f'Proxy not found: {proxy}'

    def remove_http_proxy(self) -> str:
        return self.__remove_proxy('http')

    def remove_https_proxy(self) -> str:
        return self.__remove_proxy('https')

    def __clear_proxies(self, protocol: str) -> str:
        """Clear all proxies of the given protocol (HTTP or HTTPS) and return a status message.
        """
        response = iou.valid_input(f'Are you sure you want to clear the {protocol.upper()} proxies? (y/n): ', ['y', 'n'], str)
        if response == 'n':
            return ''
        proxies = self.__read_from_proxy_file()
        proxies[protocol].clear()
        self.__write_to_proxy_file(proxies)
        return f'Cleared {protocol.upper()} proxies'

    def clear_http_proxies(self) -> str:
        return self.__clear_proxies('http')

    def clear_https_proxies(self) -> str:
        return self.__clear_proxies('https')

    def clear_all_proxies(self) -> str:
        response = iou.valid_input('Are you sure you want to clear all of the proxies? (y/n): ', ['y', 'n'], str)
        if response == 'n':
            return ''
        self.__write_to_proxy_file({'is_using_proxies': False, 'http': [], 'https': []})
        return 'Cleared all proxies'
    
    @staticmethod
    def validate_proxy(proxy: str) -> bool:
        """Validate a given proxy. Return True if it is properly formatted, False otherwise.
        """
        proxy_pattern = re.compile(
            r'^'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
            r':'
            r'[0-9]{1,5}'
            r'$'
        )
        return bool(proxy_pattern.match(proxy))
