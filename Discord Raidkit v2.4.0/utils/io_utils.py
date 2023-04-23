import os
import pathlib
import time
import typing

import colorama as cama

import utils.log_utils as lu

T = typing.TypeVar('T')


def _print_error_and_delay(msg: str, clear_screen: bool = True) -> None:
    print(f'{cama.Fore.LIGHTRED_EX}\n{msg}\n{cama.Fore.RESET}')
    if clear_screen:
        time.sleep(2)


def valid_input(prompt: str, valid_inputs: typing.List[T], input_type: typing.Type[T], clear_screen: bool = True) -> T:
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
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        try:
            converted_input = input_type(user_input)
        except ValueError:
            _print_error_and_delay(
                f'The string input could not be converted to the type {input_type.__name__}', 
                clear_screen)
        else:
            if converted_input in valid_inputs:
                return converted_input
            else:
                _print_error_and_delay(f'The string input must be one of {valid_inputs}',
                                        clear_screen)


def typed_input(prompt: str, input_type: typing.Type[T], must_be_truthy: bool, clear_screen: bool = True) -> T:
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
        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(prompt, end='')
        user_input = input()
        try:
            typed_input = input_type(user_input)
        except ValueError:
            _print_error_and_delay(
                f'The string input could not be converted to the type {input_type.__name__}', 
                clear_screen)
        else:
            if must_be_truthy and not typed_input:
                _print_error_and_delay('The input given must be truthy', clear_screen)
            else:
                return typed_input


def csv_input(prompt: str, all_must_be_truthy: bool, clear_screen: bool = True) -> typing.List[str]:
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
        values = input().split(',')
        if all_must_be_truthy and not all(values):
            _print_error_and_delay('Not all values were truthy',
                                    clear_screen)
        else:
            return values


def mkfile(file_path: str | pathlib.Path, content: T = None, clear_screen: bool = True) -> bool:
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
            file_path.write_text(str(content))
        return True
    except ValueError:
        lu.serror(f'The {type(content).__name__} input could not be converted to a string')
        _print_error_and_delay(f'The {type(content).__name__} input could not be converted to a string', clear_screen)
        return False
    except FileNotFoundError:
        lu.serror(f'The file could not be created at the given path {file_path}')
        _print_error_and_delay(f'The file could not be created at the given path {file_path}', clear_screen)
        return False
    except PermissionError:
        lu.serror(f'Permission error while creating file at {file_path}')
        _print_error_and_delay(f'Permission error while creating file at {file_path}', clear_screen)
        return False
    except Exception as e:
        lu.serror(f'An error occurred while creating file at {file_path}: {e}')
        _print_error_and_delay(f'An error occurred while creating file at {file_path}: {e}', clear_screen)
        return False
