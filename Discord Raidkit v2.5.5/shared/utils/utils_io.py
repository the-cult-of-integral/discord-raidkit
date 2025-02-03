"""
utils_io.py

This namespace contains utility functions for input/output operations.
"""

import pathlib
import shared.utils.utils_log as lu


def mkfile(file_path: str | pathlib.Path, content = None, encoding: str = 'utf-8') -> bool:
    """Make a file if it doesn't exist, including any missing directories in the file_path.
    
    Args:
        file_path (str | pathlib.Path): the path to the file to be created.
        content (T, optional): the content to be written to the file. Defaults to None.
        encoding (str, optional): the encoding of the file. Defaults to 'utf-8'.
        
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
        return False
    except FileNotFoundError:
        lu.serror(f'The file could not be created at the given path {file_path}')
        return False
    except PermissionError:
        lu.serror(f'Permission error while creating file at {file_path}')
        return False
    except Exception as e:
        lu.serror(f'An error occurred while creating file at {file_path}: {e}')
        return False
