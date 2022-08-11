'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding" 
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

surfing.py contains all surfing commands for the Anubis raidkit.
surfing.py was last updated on 11/08/22 at 13:37.
'''

import logging
import re

import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


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
            if word.strip().replace(" ", ""):
                try:
                    header = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                        "X-Requested-With": "XMLHttpRequest"}
                    url = f"https://www.dictionary.com/browse/{word}?s=t"
                    r = requests.get(url, headers=header)
                    soup = str(BeautifulSoup(r.text, 'html.parser'))
                    s1 = re.search('<meta content="', soup)
                    s2 = re.search(' See more', soup)
                    result_string = soup[s1.end():s2.start()]
                    s3 = re.search(',', result_string)
                    definition = (result_string.replace(result_string[s3.start()], ':'))[
                        13 + len(word):].capitalize()

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
            else:
                embed = discord.Embed(
                    title="Issue",
                    description="You must specify a word.",
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
    return
