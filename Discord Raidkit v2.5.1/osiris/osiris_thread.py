"""
osiris_thread.py

This namespace contains the OsirisThread class, a QThread that Osiris runs on.

It is effectively the main class for Osiris, and is responsible for
invoking Osiris' coroutines found in the osiris_coroutines namespace.
"""

import asyncio
from PyQt6.QtCore import QThread, pyqtSignal

import osiris.osiris_coroutines as oc
from shared.dr.dr_config import DRConfig
from shared.dr.dr_types import EO_Commands


class OsirisThread(QThread):
    """The QThread that Osiris runs on.
    """

    signal_append_oterminal = pyqtSignal(str)  # For appending to the Osiris terminal.
    signal_refresh_running_commands_view = pyqtSignal(int)  # For refreshing the running commands view.
    signal_spy_running = pyqtSignal(bool)  # For updating the controls.
    signal_login_running = pyqtSignal(bool)  # For updating the controls.
    signal_nuke_running = pyqtSignal(bool)  # For updating the controls.

    def __init__(self, config: DRConfig):
        super().__init__()
        self.config = config
        self.osiris_loop = asyncio.new_event_loop()

        self.running_commands_names = []
        self.running_commands_tasks = []

    def invoke_command(self, command: str, **kwargs):
        match command:
            case EO_Commands.SPY.value:
                coroutine = oc.spy(**kwargs)
            case EO_Commands.LOGIN.value:
                coroutine = oc.login(**kwargs)
            case EO_Commands.NUKE.value:
                coroutine = oc.nuke(**kwargs)
        
        if coroutine:
            new_task = asyncio.run_coroutine_threadsafe(coroutine, self.osiris_loop)
            self.running_commands_tasks.append(new_task)
    
    def run(self):
        asyncio.set_event_loop(self.osiris_loop)
        self.osiris_loop.run_forever()
