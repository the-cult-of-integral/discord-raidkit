"""
surfing.py

This namespace contains the Anubis surfing command cog,
which provides a command to define a word using dictionary.com.
A part of the genuine commands included in the Anubis raider for social engineering.
"""

import re

import bs4
import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands
import requests

import shared.utils.utils_log as lu


class Surfing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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


async def setup(bot):
    await bot.add_cog(Surfing(bot))
