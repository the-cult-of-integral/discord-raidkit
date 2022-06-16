"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json

import discord
from discord.ext import commands


def get_current_prefix() -> str:
    """Get the current bot prefix

    Returns:
        str: the current bot prefix
    """
    try:
        with open("config_data.json", "r") as f:
            data = json.load(f)
        return data["bot_prefix"]
    except:
        raise KeyError("No bot prefix set")


class QHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_nsfw()
    async def help(self, ctx) -> None:
        embed = discord.Embed(colour=discord.Color.gold())
        embed.set_author(name=f"Here's a list of my commands!")
        embed.add_field(name=f"{get_current_prefix()}vagl", value="Display an image of vaginal sex.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}oral", value="Display an image of oral sex.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}anal", value="Display an image of anal sex.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}les", value="Display an image of lesbian sex.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}gay", value="Display an image of gay sex.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}tits", value="Display an image of tits.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}ass", value="Display an image of an ass.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}pussy", value="Display an image of a pussy.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}cock", value="Display an image of a cock.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}asian", value="Display an image of an asian.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}amateur", value="Display an image of an amateur.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}hentai", value="Display an image of hentai.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}milf", value="Display an image of a milf.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}teen", value="Display an image of a teen (18/19).", inline=True)
        embed.add_field(name=f"{get_current_prefix()}ebony", value="Display an image of an ebony.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}threesome", value="Display an image of a threesome.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}cartoon", value="Display an image of cartoon porn.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}creampie", value="Display an image of a creampie.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}bondage", value="Display an image of bondage.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}squirt", value="Display an image of squirting.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}neko", value="Display an image of neko.", inline=True)
        embed.add_field(name=f"{get_current_prefix()}yiff", value="Display an image of yiff.", inline=True)
        await ctx.message.channel.send(embed=embed)
        return


def setup(bot) -> None:
    bot.add_cog(QHelp(bot))
    return

