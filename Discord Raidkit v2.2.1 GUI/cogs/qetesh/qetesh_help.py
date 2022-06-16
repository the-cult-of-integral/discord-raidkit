"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json

import discord
from discord.ext import commands


class QeteshHelp(commands.Cog, name='QeteshHelp module'):
    def __init__(self, bot):
        self.bot = bot
        with open("config_data.json", "r") as f:
            self.config_data = json.load(f)
    
    @commands.command(name="help")
    async def help(self, ctx):
        if ctx.message.channel.nsfw:
            embed = discord.Embed(colour=discord.Color.gold())
            embed.set_author(name=f"Here's a list of my commands!")
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}vagl", value="Display an image of vaginal sex.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}bj", value="Display an image of oral sex.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}anal", value="Display an image of anal sex.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}les", value="Display an image of lesbian sex.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}gay", value="Display an image of gay sex.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}tits", value="Display an image of tits.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}ass", value="Display an image of an ass.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}pussy", value="Display an image of a pussy.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}cock", value="Display an image of a cock.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}asian", value="Display an image of an asian.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}amateur", value="Display an image of an amateur.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}hentai", value="Display an image of hentai.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}milf", value="Display an image of a milf.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}teen", value="Display an image of a teen (18/19).", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}ebony", value="Display an image of an ebony.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}threesome", value="Display an image of a threesome.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}cartoon", value="Display an image of cartoon porn.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}creampie", value="Display an image of a creampie.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}bondage", value="Display an image of bondage.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}squirt", value="Display an image of squirting.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}neko", value="Display an image of neko.", inline=True)
            embed.add_field(name=f"{self.config_data.get('bot_prefix')}yiff", value="Display an image of yiff.", inline=True)
            await ctx.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="This is an NSFW channel only bot.",
                colour=discord.Colour.orange()
            )
            await ctx.message.channel.send(embed=embed)

