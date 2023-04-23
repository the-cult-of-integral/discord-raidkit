import abc
import typing


class BotType(abc.ABC):
    """An abstract class to define bot types"""
    @abc.abstractmethod
    def extensions(self) -> typing.List[str]:
        """Returns a list of extensions to load"""
    
    @abc.abstractmethod
    def __str__(self) -> str:
        """Returns the bot type's name"""
