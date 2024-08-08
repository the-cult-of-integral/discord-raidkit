"""
handler.py

This namespace contains the error handler cog,
which provides an error handler for the bot.
"""

import discord
import discord.ext as dext


class Handler(dext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @dext.commands.Cog.listener()
    async def on_command_error(self, ctx: dext.commands.Context, error: dext.commands.CommandError):
        if isinstance(error, dext.commands.CommandNotFound):
            embed = discord.Embed(
                title='Error',
                description='**Command does not exist.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, dext.commands.MissingPermissions):
            embed = discord.Embed(
                title='Error',
                description='**Permission denied.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, dext.commands.NotOwner):
            embed = discord.Embed(
                title='Error',
                description='**You must be the owner of the bot to use this command.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, dext.commands.NSFWChannelRequired):
            embed = discord.Embed(
                title='Error',
                description='**This command can only be used in NSFW channels.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        elif isinstance(error, dext.commands.CheckFailure):
            embed = discord.Embed(
                title='Error',
                description='**Access denied.**',
                color=discord.Color.brand_red())
            await ctx.send(embed=embed)
        else:
            pass


async def setup(bot):
    await bot.add_cog(Handler(bot))
