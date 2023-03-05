"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

surfing.py stores the surfing commands for Anubis.
surfing.py was last updated on 05/03/23 at 20:50 UTC.
"""

import logging
import re

import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

from utils import init_logger

init_logger()


class Surfing(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return

    @app_commands.command(
        name='define',
        description='Defines a word.')
    @app_commands.describe(
        word='The word to define.')
    async def define(self, interaction: discord.Interaction, word: str) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            word = word.lower()
            if not word.strip().replace(" ", ""):
                embed = discord.Embed(
                    title="Issue",
                    description="You must specify a word.",
                    color=discord.Color.orange())
                await interaction.followup.send(embed=embed)
            try:
                url = f'https://www.dictionary.com/browse/{word}'
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                definition = soup.find('div', class_='css-1o58fj8 e1hk9ate4').find('span').text
                definition = re.sub(r'\s+', ' ', definition).strip()

                embed = discord.Embed(
                    title=f"{word.title()}",
                    description=f'{definition}',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)

            except AttributeError:
                embed = discord.Embed(
                    title="Issue",
                    description=f'"{word}" was not found.',
                    color=discord.Color.orange())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to send embeds to this channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in surfing.py - define(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Surfing(bot))
