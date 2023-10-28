"""
Discord Raidkit v2.4.3
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

import re

import bs4
import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands
import requests

import tools.raider as rd
import utils.log_utils as lu


class Surfing(commands.Cog):
    def __init__(self, bot: rd.Raider):
        self.bot: rd.Raider = bot
    
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
                soup = bs4.BeautifulSoup(page.content, 'html.parser')
                definition = soup.find('span', class_='one-click-content css-nnyc96 e1q3nk1v1').text
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
            lu.swarning(f'There was an error when defining the word "{word}": {e}')
            await interaction.followup.send(f'Error: {e}')


async def setup(bot: rd.Raider):
    await bot.add_cog(Surfing(bot))
