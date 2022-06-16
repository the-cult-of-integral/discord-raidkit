"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import discord
from discord.ext import commands


class Status(commands.Cog, name='Status module'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="latency")
    async def latency(self, ctx):
        embed = discord.Embed(
            title="Latency",
            description=f'Latency: {round(self.bot.latency*1000)}ms.',
            color=discord.Colour.blue()
            )
        await ctx.send(embed=embed)

