# Scripted by K. Catterall.

# Modules
import discord
from discord.ext import commands


class RaidPrevention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add a member from an "anti-raid database".

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def db_add_member(self, ctx, member: discord.Member, *, reason=None):
        try:
            embed = discord.Embed(
                title="Member added", description=f"{member.mention} has been added to the database.", color=discord.Color.blue())
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Issue", description=f"{member} is not currently on this server.", color=discord.Color.orange())
            await ctx.send(embed=embed)

    # Remove a member from an "anti-raid database".

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def db_del_member(self, ctx, member: discord.Member, *, reason=None):
        try:
            embed = discord.Embed(
                title="Member removed", description=f"{member.mention} has been removed from the database.", color=discord.Color.blue())
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Issue", description=f"{member} is not currently on this server.", color=discord.Color.orange())
            await ctx.send(embed=embed)

    # Lock a channel.

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(
                send_messages=False)}
            await channel.edit(overwrites=overwrites)
            embed = discord.Embed(
                title="Channel locked", description=f"{channel.name} has been locked down.", color=discord.Color.blue())
            await ctx.send(embed=embed)
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            embed = discord.Embed(
                title="Channel locked", description=f"{channel.name} has been locked down.", color=discord.Color.blue())
            await ctx.send(embed=embed)

    # Unlock a channel.

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)}
            await channel.edit(overwrites=overwrites)
            embed = discord.Embed(
                title="Channel unlocked", description=f"{channel.name} has been unlocked.", color=discord.Color.blue())
            await ctx.send(embed=embed)
        elif channel.overwrites[ctx.guild.default_role].send_messages == None or channel.overwrites[ctx.guild.default_role].send_messages == False:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            embed = discord.Embed(
                title="Channel unlocked", description=f"{channel.name} has been unlocked.", color=discord.Color.blue())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(RaidPrevention(bot))


# Scripted by K. Catterall.
