import discord
import re
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

class Surfing(commands.Cog, name='Surfing module'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="define")
    async def define(self, ctx, *, word=""):
        word = word.strip().replace(" ", "")
        if word:
            try:
                header = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                    }
                url = f"https://www.dictionary.com/browse/{word}?s=t"
                r = requests.get(url, headers=header)
                soup = str(BeautifulSoup(r.text, "html.parser"))
                s1 = re.search('<meta content="', soup)
                s2 = re.search(' See more', soup)
                result_string = soup[s1.end():s2.start()]
                s3 = re.search(',', result_string)
                definition = (
                    result_string.replace(
                        result_string[s3.start()],
                         ':')
                         )[13 + len(word):].capitalize()
                embed = discord.Embed(
                    title=f"{word.title()}",
                    description=f'{definition}',
                    color=discord.Colour.blue()
                    )
                await ctx.send(embed=embed)
            except AttributeError:
                embed = discord.Embed(
                    title="Unknown Word",
                    description=f'"{word}" was not found.',
                    color=discord.Colour.orange()
                    )
                await ctx.send(embed=embed)
            except Exception:
                pass
        else:
            embed = discord.Embed(
                title="Notice",
                description="You must specify a word.",
                color=discord.Colour.orange()
                )
            await ctx.send(embed=embed)


