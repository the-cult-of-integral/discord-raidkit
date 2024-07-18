"""
utils_runtime.py

This namespace contains utility functions for runtime operations.
"""

import os
import sys


def is_running_as_executable():
    _, ext = os.path.splitext(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0])
    return ext.lower() in ('.exe', '')
