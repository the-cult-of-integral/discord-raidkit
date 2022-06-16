"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Clear messages.

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, n=10):
        if n < 1:
            embed = discord.Embed(
                title="Issue",
                description=f"You must specify a real amount.",
                color=discord.Colour.orange())
            await ctx.send(embed=embed)
        elif n > 1000:
            embed = discord.Embed(
                title="Issue",
                description=f"The limit is 1000.",
                color=discord.Colour.orange())
            await ctx.send(embed=embed)
        else:
            try:
                await ctx.channel.purge(limit=n)
            except ValueError:
                embed = discord.Embed(
                    title="Issue",
                    description=f"You must specify a real amount.",
                    color=discord.Colour.orange())
                await ctx.send(embed=embed)
        return

    # Kick a member.

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member kicked",
            description=f"{member.mention} has been kicked.",
            color=discord.Colour.blue())
        await ctx.send(embed=embed)
        return

    # Ban a member.

    @commands.command()
    @commands.has_guild_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member banned",
            description=f"{member.mention} has been banned.",
            color=discord.Colour.blue())
        await ctx.send(embed=embed)
        return

    # Unban a member.

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        ID = ctx.message.guild.id
        g = discord.utils.get(self.bot.guilds, id=ID)
        banned_users = await g.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (
                    member_name, member_discriminator):
                await g.unban(user)
                embed = discord.Embed(
                    title="Member unbanned",
                    description=f"{user.mention} has been unbanned.",
                    color=discord.Colour.blue())
                await ctx.send(embed=embed)
                return

    # Mute a member.

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        ID = ctx.message.guild.id
        g = discord.utils.get(self.bot.guilds, id=ID)
        if member.guild_permissions.administrator or member.guild_permissions.manage_roles or member.guild_permissions.manage_permissions:
            embed = discord.Embed(
                title="Issue",
                description=f"You can not mute this member.",
                color=discord.Colour.orange())
            await ctx.send(embed=embed)
            return
        else:
            role = discord.utils.find(
                lambda r: r.name == 'bot muted', g.roles)
            if role in member.roles:
                embed = discord.Embed(
                    title="Issue",
                    description=f"{member.mention} is already muted.",
                    color=discord.Colour.orange())
                await ctx.send(embed=embed)
                return
            else:
                if discord.utils.get(g.roles, name="bot muted"):
                    role = discord.utils.get(
                        member.guild.roles, name="bot muted")
                    await discord.Member.add_roles(member, role)
                    member.guild_permissions.send_messages = False
                else:
                    permissions = discord.Permissions(
                        send_messages=False, read_messages=True)
                    await g.create_role(name="bot muted", permissions=permissions)
                    role = discord.utils.get(
                        member.guild.roles, name="bot muted")
                    await discord.Member.add_roles(member, role)
                    member.guild_permissions.send_messages = False

                embed = discord.Embed(
                    title="Member muted",
                    description=f"{member.mention} has been muted.",
                    color=discord.Colour.blue())
                await ctx.send(embed=embed)
                return

    # Unmute a member.

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        ID = ctx.message.guild.id
        g = discord.utils.get(self.bot.guilds, id=ID)
        role = discord.utils.find(
            lambda r: r.name == 'bot muted', g.roles)
        if role not in member.roles:
            if member.guild_permissions.send_messages:
                embed = discord.Embed(
                    title="Issue",
                    description=f"{member.mention} is not muted.",
                    color=discord.Colour.orange())
                await ctx.send(embed=embed)
                return
            else:
                role = discord.utils.get(member.guild.roles, name="bot muted")
                await discord.Member.remove_roles(member, role)
                member.guild_permissions.send_messages = True

                embed = discord.Embed(
                    title="Member unmuted",
                    description=f"{member.mention} has been unmuted.",
                    color=discord.Colour.blue())
                await ctx.send(embed=embed)
                return
        else:
            role = discord.utils.get(member.guild.roles, name="bot muted")
            await discord.Member.remove_roles(member, role)
            member.guild_permissions.send_messages = True

            embed = discord.Embed(
                title="Member unmuted",
                description=f"{member.mention} has been unmuted.",
                color=discord.Colour.blue())
            await ctx.send(embed=embed)
            return


def setup(bot) -> None:
    bot.add_cog(Moderation(bot))
    return

