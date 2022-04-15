import discord
from discord.ext import commands


class BotErrAndConfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Error",
                description=f"**Command does not exist.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description=f"**Permission denied.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description=f"**You must be the owner of the bot to use this command.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Error",
                description=f"**Access denied.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        else:
            print(f"Ignoring exception in command: {ctx.command}")
    
    # Load/Unload/Reload: Used for messing with Cogs.

    @commands.command(name="load", hidden=True)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        embed = discord.Embed(
            title="Extension loaded",
            description=f"{extension} has been loaded.",
            color=discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name="unload", hidden=True)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        embed = discord.Embed(
            title="Extension unloaded",
            description=f"{extension} has been unloaded.",
            color=discord.Colour.green())
        await ctx.send(embed=embed)

    @commands.command(name="reload", hidden=True)
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        embed = discord.Embed(
            title="Extension reloaded",
            description=f"{extension} has been reloaded.",
            color=discord.Colour.green())
        await ctx.send(embed=embed)


