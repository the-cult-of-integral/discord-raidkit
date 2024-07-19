"""
dr_config.py

This namespace is used to manage configuration values 
used throughout the application.
"""

import os
import ujson
import shared.dr.dr_types as dr_types

CONFIG_PATH = 'config.json'

DEFAULT_CONFIG = {
    "Application": {
        "DoStartupVersionCheck": True,
        "DoNotShowHorusCloseMessage": False,
    },
    "Horus": {
        "Token": "",
        "ApplicationID": "",
        "Prefix": "",
        "Stauses": [],
        "InitialPresence": {
            "ActivityName": "",
            "ActivityURL": "",   
            "ActivityType": dr_types.ED_Activities.PLAYING.value,
            "StatusType": dr_types.ED_Statuses.ONLINE.value         
        },
        "AutoInvisibleOnMaliciousAction": True,
        "RaiderType": dr_types.EH_Raiders.ANUBIS.value
    },
    "Osiris": {
        "Token": ""
    }
}


class CfgApplication:
    """For configuration values related to the application itself.
    """
    def __init__(self, config: dict):
        self._config = config
    
    @property
    def do_startup_version_check(self) -> bool:
        """Whether to check for updates on startup or not.
        """
        return self._config.get('DoStartupVersionCheck', DEFAULT_CONFIG['Application']['DoStartupVersionCheck'])
    
    @do_startup_version_check.setter
    def do_startup_version_check(self, value: bool):
        self._config['DoStartupVersionCheck'] = value

    @property
    def do_not_show_horus_close_message(self) -> bool:
        """Whether to show the Horus close message or not.
        """
        return self._config.get('DoNotShowHorusCloseMessage', DEFAULT_CONFIG['Application']['DoNotShowHorusCloseMessage'])
    
    @do_not_show_horus_close_message.setter
    def do_not_show_horus_close_message(self, value: bool):
        self._config['DoNotShowHorusCloseMessage'] = value
    

class CfgInitialPresence:
    """For configuration values related to the Horus's initial presence.
    """
    def __init__(self, config: dict):
        self._config = config
    
    @property
    def activity_name(self) -> str:
        """The name of the activity.
        """
        return self._config.get('ActivityName', DEFAULT_CONFIG['Horus']['InitialPresence']['ActivityName'])
    
    @activity_name.setter
    def activity_name(self, value: str):
        self._config['ActivityName'] = value
    
    @property
    def activity_url(self) -> str:
        """The URL of the activity.
        """
        return self._config.get('ActivityURL', DEFAULT_CONFIG['Horus']['InitialPresence']['ActivityURL'])
    
    @activity_url.setter
    def activity_url(self, value: str):
        self._config['ActivityURL'] = value
    
    @property
    def activity_type(self) -> int:
        """The type of the activity.
        """
        return self._config.get('ActivityType', DEFAULT_CONFIG['Horus']['InitialPresence']['ActivityType'])
    
    @activity_type.setter
    def activity_type(self, value: int):
        self._config['ActivityType'] = value
    
    @property
    def status_type(self) -> int:
        """The type of the status.
        """
        return self._config.get('StatusType', DEFAULT_CONFIG['Horus']['InitialPresence']['StatusType'])
    
    @status_type.setter
    def status_type(self, value: int):
        self._config['StatusType'] = value


class CfgHorus:
    """For configuration values related to Horus.
    """
    def __init__(self, config: dict):
        self._config = config
        self._initial_presence = CfgInitialPresence(self._config["InitialPresence"])
    
    @property
    def token(self) -> str:
        """The bot token.
        """
        return self._config.get('Token', DEFAULT_CONFIG['Horus']['Token'])
    
    @token.setter
    def token(self, value: str):
        self._config['Token'] = value
    
    @property
    def application_id(self) -> str:
        """The application ID.
        """
        return self._config.get('ApplicationID', DEFAULT_CONFIG['Horus']['ApplicationID'])

    @application_id.setter
    def application_id(self, value: str):
        self._config['ApplicationID'] = value
    
    @property
    def prefix(self) -> str:
        """The bot's prefix.
        """
        return self._config.get('Prefix', DEFAULT_CONFIG['Horus']['Prefix'])
    
    @prefix.setter
    def prefix(self, value: str):
        self._config['Prefix'] = value
    
    @property
    def statuses(self) -> list:
        """The statuses.
        """
        return self._config.get('Statuses', DEFAULT_CONFIG['Horus']['Stauses'])
    
    @statuses.setter
    def statuses(self, value: list):
        self._config['Statuses'] = value
    
    @property
    def initial_presence(self) -> CfgInitialPresence:
        """The initial presence.
        """
        return CfgInitialPresence(self._config)
    
    @property
    def auto_invisible_on_malicious_action(self) -> bool:
        """Whether to go invisible on malicious action or not.
        """
        return self._config.get('AutoInvisibleOnMaliciousAction', DEFAULT_CONFIG['Horus']['AutoInvisibleOnMaliciousAction'])
    
    @auto_invisible_on_malicious_action.setter
    def auto_invisible_on_malicious_action(self, value: bool):
        self._config['AutoInvisibleOnMaliciousAction'] = value

    @property
    def raider_type(self) -> int:
        """The raider type.
        """
        return self._config.get('RaiderType', DEFAULT_CONFIG['Horus']['RaiderType'])
    
    @raider_type.setter
    def raider_type(self, value: int):
        self._config['RaiderType'] = value
    

class CfgOsiris:
    """For configuration values related to Osiris.
    """
    def __init__(self, config: dict):
        self._config = config
    
    @property
    def token(self) -> str:
        """The user token.
        """
        return self._config.get('Token', DEFAULT_CONFIG['Osiris']['Token'])
    
    @token.setter
    def token(self, value: str):
        self._config['Token'] = value


class DRConfig:
    """A wrapper around the Discord Raidkit configuration JSON.
    """
    def __init__(self, config_path=None):
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                self._config = ujson.load(file)
        else:
            with open(config_path, 'w') as file:
                ujson.dump(DEFAULT_CONFIG, file, indent=4)
            self._config = DEFAULT_CONFIG
        
        self.application = CfgApplication(self._config["Application"])
        self.horus = CfgHorus(self._config["Horus"])
        self.osiris = CfgOsiris(self._config["Osiris"])

    def save_to_file(self, path):
        """Save the configuration to a file.
        """
        with open(path, 'w') as file:
            ujson.dump(self._config, file, indent=4)

    def __str__(self):
        return ujson.dumps(self._config, indent=4)
