"""
Discord Raidkit v2.4.4
the-cult-of-integral

Last modified: 2023-11-04 21:38
"""

import os
import pathlib
import time
import typing

import colorama as cama

import utils.log_utils as lu

T = typing.TypeVar('T')
EXIT = 'exit'


class MenuOption:
    """A menu option. This is used to create numbered menus."""
    __slots__ = ('name', 'description', 'func', 'args', 'kwargs', 'condition')

    def __init__(self, name: str, description: str, func: typing.Callable[..., str], *args, condition: typing.Callable[[], bool] = None, **kwargs):
        """Create a menu option.

        Args:
            name (str): the name of the option to be displayed in the menu.
            description (str): the description of the option to be displayed when the user selects it.
            func (typing.Callable[..., str]): the function to be called when the user selects the option.
            args: Additional arguments to pass to the function.
            condition: a callable that returns a bool; determines if option is visible in a Menu object.
            kwargs: Additional keyword arguments to pass to the function.
        """
        self.name = name
        self.description = description
        self.func = func
        self.args = args
        self.condition = condition
        self.kwargs = kwargs

    def is_available(self) -> bool:
        if callable(self.condition):
            return self.condition()
        return True
    
    def call_func(self):
        """Call the function with the stored arguments and keyword arguments."""
        return self.func(*self.args, **self.kwargs)


class NumberedMenu:
    """A numbered menu. This is used to create menus with MenuOption instances."""
    __slots__ = ('name', 'options', 'do_name_and_desc', 'pcolor', 'scolor', 'current_visible_options')

    def __init__(self, name: str, options: typing.List[MenuOption], 
                do_name_and_desc: bool = True, pcolor: str = cama.Fore.WHITE, 
                scolor: str = cama.Fore.WHITE, auto_append_exit: bool = True):
        """Create a numbered menu.

        Args:
            name (str): the name of the menu to be displayed at the top.
            options (typing.List[MenuOption]): the options to be displayed in the menu.
            do_name_and_desc (bool, optional): whether to display the name and description of the selected option. Defaults to True.
            pcolor (str, optional): the primary color of the menu. Defaults to cama.Fore.WHITE.
            scolor (str, optional): the secondary color of the menu. Defaults to cama.Fore.WHITE.
        """
        self.name = name
        self.options = options
        if auto_append_exit:
            self.options.append(MenuOption('Exit', 'Exit the program', lambda: EXIT))
        if not self.options:
            raise ValueError('options cannot be empty')
        self.do_name_and_desc = do_name_and_desc
        self.pcolor = pcolor
        self.scolor = scolor
        self.current_visible_options = [opt for opt in self.options if opt.is_available()]

    def run(self) -> None:
        hint = ''
        while True:
            hint = self._do_menu_cycle(hint)
            if hint == EXIT:
                break
        os.system('cls' if os.name == 'nt' else 'clear')

    def _do_menu_cycle(self, hint: str = '') -> str:
        os.system('cls' if os.name == 'nt' else 'clear')
        self.__print_menu()
        hint = self.__get_user_choice(hint)
        return hint

    def __print_menu(self) -> None:
        columns, _ = os.get_terminal_size()

        lines = self.name.split('\n')
        for line in lines:
            line_len = len(line)
            padding = (columns - line_len) // 2
            print(f"{self.scolor}{' ' * padding}{line}{' ' * padding}{self.scolor}")

        self.current_visible_options = [opt for opt in self.options if opt.is_available()]
        
        for i, option in enumerate(self.current_visible_options, 1):
            option_str = f"{self.pcolor}[{self.scolor}{i}{self.pcolor}] {option.name} {cama.Fore.LIGHTWHITE_EX}- {self.pcolor}{option.description}"
            option_len = len(option_str)
            if option_len > columns:
                option_str = f"{option_str[:columns-3]}..."
            print(f"{self.scolor}{option_str}")


    def __get_user_choice(self, hint: str) -> str:
        hint = hint if hint else ''
        print(f'\n\n{self.scolor}{hint}\n\n')
        print(f'{cama.Fore.LIGHTWHITE_EX}>>> {self.scolor}', end='')

        try:
            choice = int(input())
        except ValueError:
            return f'{cama.Fore.LIGHTRED_EX}Please enter an integer in the range of the menu options.'
        
        if not 1 <= choice <= len(self.current_visible_options):
            return f'{cama.Fore.LIGHTRED_EX}Please enter an integer in the range of the menu options.'
        
        option = self.current_visible_options[choice - 1]
        os.system('cls' if os.name == 'nt' else 'clear')
        if self.do_name_and_desc:
            print(f'\n{self.pcolor}> {option.name}\n\n{self.scolor} * {option.description}\n\n')
        return option.call_func()


def _print_error_and_delay(msg: str) -> None:
    print(f'{cama.Fore.LIGHTRED_EX}\n{msg}\n')
    time.sleep(2)


def valid_input(prompt: str, valid_inputs: typing.List[T], input_type: typing.Type[T]) -> T:
    """Prompts the user with a message and accepts input from a list of valid inputs.

    Args:
        prompt (str): the message to display to the user.
        valid_inputs (List[T]): a list of valid inputs of type T.
        input_type (Type[T]): the type of the valid inputs.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        T: the user's input, converted to type T.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        try:
            converted_input = input_type(user_input)
        except ValueError:
            _print_error_and_delay(f'The string input could not be converted to the type {input_type.__name__}')
        else:
            if converted_input in valid_inputs:
                return converted_input
            else:
                _print_error_and_delay(f'The string input must be one of {valid_inputs}')


def typed_input(prompt: str, input_type: typing.Type[T], must_be_truthy: bool) -> T:
    """
    Prompts the user with a message and accepts input of the specified type.
    If the input is invalid, the function will prompt the user again.

    Args:
        prompt (str): the message to display to the user.
        input_type (Type[T]): the type to convert the user's input to.
        must_be_truthy (bool): whether to require the input to be truthy.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        T: the user's input, converted to type T.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        try:
            typed_input = input_type(user_input)
        except ValueError:
            _print_error_and_delay(
                f'The string input could not be converted to the type {input_type.__name__}')
        else:
            if must_be_truthy and not typed_input:
                _print_error_and_delay('The input given must be truthy')
            else:
                return typed_input


def csv_input(prompt: str, all_must_be_truthy: bool) -> typing.List[str]:
    """Prompts the user with a message and accepts a comma-separated list of values.

    Args:
        prompt (str): the message to display to the user.
        all_must_be_truthy (bool): whether to require all values to be truthy.
        clear_screen (bool): whether to clear the screen before prompting the user.

    Returns:
        list: the user's input, converted to a list of values.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        values = input().split(',')
        if all_must_be_truthy and not all(values):
            _print_error_and_delay('Not all values were truthy')
        else:
            return values


def mkfile(file_path: str | pathlib.Path, content: T = None, encoding: str = 'utf-8') -> bool:
    """Make a file if it doesn't exist, including any missing directories in the file_path.
    
    Args:
        file_path (str | pathlib.Path): the path to the file to be created.
        content (T, optional): the content to be written to the file. Defaults to None.
        clear_screen (bool, optional): whether to clear the screen upon an exception. Defaults to True.
        
    Returns:
        bool: True if no errors were raised, False otherwise.
    """
    try:
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        if content is not None:
            file_path.write_text(str(content), encoding=encoding)
        return True
    except ValueError:
        lu.serror(f'The {type(content).__name__} input could not be converted to a string')
        _print_error_and_delay(f'The {type(content).__name__} input could not be converted to a string')
        return False
    except FileNotFoundError:
        lu.serror(f'The file could not be created at the given path {file_path}')
        _print_error_and_delay(f'The file could not be created at the given path {file_path}')
        return False
    except PermissionError:
        lu.serror(f'Permission error while creating file at {file_path}')
        _print_error_and_delay(f'Permission error while creating file at {file_path}')
        return False
    except Exception as e:
        lu.serror(f'An error occurred while creating file at {file_path}: {e}')
        _print_error_and_delay(f'An error occurred while creating file at {file_path}: {e}')
        return False
