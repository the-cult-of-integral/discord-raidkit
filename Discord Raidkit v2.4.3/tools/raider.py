"""
Discord Raidkit v2.4.3
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

import asyncio
import itertools
import os
import typing

import aiohttp
import discord
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import nest_asyncio

import conf.config as conf
import shared.shared as shared
import ui.drui as drui
import utils.log_utils as lu

nest_asyncio.apply()


class Anubis(shared.BotType):
    """The BotType for Anubis Discord Bots"""
    def extensions(self) -> typing.List[str]:
        return [
            'cogs.anubis.moderation',
            'cogs.anubis.raid_prevention',
            'cogs.anubis.surfing',
            'cogs.anubis.ahelp',
            'cogs.shared.cmds',
            'cogs.shared.handler'
        ]
    
    def __str__(self) -> str:
        return 'Anubis'


class Qetesh(shared.BotType):
    """The BotType for Qetesh Discord Bots"""
    def extensions(self) -> typing.List[str]:
        return [
            'cogs.qetesh.nsfw',
            'cogs.shared.cmds',
            'cogs.shared.handler'
        ]
    
    def __str__(self) -> str:
        return 'Qetesh'


class Raider(commands.Bot):
    """A class to handle the creation of Discord Raidkit Discord Bots"""
    __slots__ = ('bot_type', 'clear_screen', 'prefix', 'session', 'statuses')
    
    def __init__(self, bot_type: shared.BotType, cfg: conf.DRConfig, clear_screen: bool = True):
        """Initializes a Discord Raidkit Discord Bot

        Args:
            bot_type (BotType): which bot type to create
            cfg (DRConfig): the configuration object to use
        """
        super().__init__(
            command_prefix = cfg['prefix'],
            intents = discord.Intents.all(),
            application_id = cfg['app_id']
        )
        self.bot_type: shared.BotType = bot_type
        self.prefix: str = cfg['prefix']
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.clear_screen: bool = clear_screen
        self.remove_command('help')
        if cfg['statuses']:
            self.statuses: typing.List[str] = itertools.cycle(cfg['statuses'])
    
    async def setup_hook(self):
        """A hook to load the bot's extensions"""
        tasks = [self.load_extension(ext) for ext in self.bot_type.extensions()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                lu.serror(f'Failed to load extension: {result}')
                raise result
    
    async def on_ready(self):
        """On ready event handler"""
        try:
            await self.tree.sync()
        except discord.errors.NotFound:
            lu.scritical('Failed to sync slash commands. Please check your application ID is correct.')
            raise SystemExit
        
        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(drui.raider_cmds(self.prefix, self.bot_type))
        
        if self.statuses:
            self.change_status.start()
    
    @tasks.loop(seconds=10)
    async def change_status(self):
        """A task to change the bot's status
        """
        await self.change_presence(activity=discord.Game(next(self.statuses)))
    
    async def close(self):
        """Closes the bot"""
        if self.statuses:
            self.change_status.cancel()
        await self.session.close()
        await super().close()
