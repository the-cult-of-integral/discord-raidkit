"""
Discord Raidkit v2.2.0 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import re

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class Surfing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def define(self, ctx, *, word=f""):
        if word.strip().replace(" ", "") != "":
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
                    color=discord.Colour.blue())
                await ctx.send(embed=embed)
            except AttributeError:
                embed = discord.Embed(
                    title="Issue",
                    description=f'"{word}" was not found.',
                    color=discord.Colour.orange())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Issue",
                description="You must specify a word.",
                color=discord.Colour.orange())
            await ctx.send(embed=embed)


def setup(bot) -> None:
    bot.add_cog(Surfing(bot))
    return

