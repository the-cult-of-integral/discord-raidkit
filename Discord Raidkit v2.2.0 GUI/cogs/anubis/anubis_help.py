"""
Discord Raidkit v2.2.0 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json

import discord
from discord.ext import commands


class AnubisHelp(commands.Cog, name='AnubisHelp module'):
    def __init__(self, bot):
        self.bot = bot
        with open("config_data.json", "r") as f:
            self.config_data = json.load(f)
    
    @commands.command(name="help")
    async def help(self, ctx):
        missing_perms = False
        author = ctx.message.author
        embed = discord.Embed(colour=discord.Color.gold())
        embed.set_author(name=f"Here's a list of my commands!")

        if not author.guild_permissions.manage_messages \
            and not author.guild_permissions.kick_members \
                and not author.guild_permissions.ban_members \
                    and not author.guild_permissions.administrator \
                        and not author.guild_permissions.mute_members:
            embed.add_field(
                name="**No permissions for moderator commands!**",
                value="You lack every permission used by the moderator commands.",
                inline=False)
            missing_perms = True
        else:
            embed.add_field(name="**Moderation:**",
                            value="My moderation commands are:", inline=False)
            if author.guild_permissions.manage_messages:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}clear [1-1000]",
                    value="Clears messages from a channel.",
                    inline=False)
            else:
                missing_perms = True
            if author.guild_permissions.kick_members:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}kick <member> [reason]",
                    value="Kicks a member from the server.",
                    inline=False)
            else:
                missing_perms = True
            if author.guild_permissions.ban_members:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}ban <member> [reason]",
                    value="Bans a member from the server.",
                    inline=False)
            else:
                missing_perms = True
            if author.guild_permissions.administrator:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}unban <member>",
                    value="Unbans a member from the server.",
                    inline=False)
            else:
                missing_perms = True
            if author.guild_permissions.mute_members:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}mute <member> [reason]",
                    value="Mutes a member on the server.",
                    inline=False)
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}unmute <member>",
                    value="Unmutes a member on the server.",
                    inline=False)
            else:
                missing_perms = True

        if not author.guild_permissions.mute_members \
            and not author.guild_permissions.administrator:
            embed.add_field(
                name="**No permissions for anti-raid commands!**",
                value="You lack every permission used by the anti-raid commands.",
                inline=False)
            missing_perms = True
        else:
            embed.add_field(name="**Anti-Raid:**",
                            value="My anti-raid commands are:", inline=False)
            if author.guild_permissions.administrator:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}db_add_member <member>",
                    value="Adds a member to my raider database.",
                    inline=False)
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}db_del_member <member>",
                    value="Removes a member from my raider database.",
                    inline=False)
            else:
                missing_perms = True
            if author.guild_permissions.mute_members:
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}lock",
                    value="Locks down current text channel during a raid.",
                    inline=False)
                embed.add_field(
                    name=f"{self.config_data.get('bot_prefix')}unlock",
                    value="Unlocks current text channel after a raid.",
                    inline=False)
            else:
                missing_perms = True

        embed.add_field(name="**Status:**",
                        value="My status commands are:", inline=False)
        embed.add_field(
            name=f"{self.config_data.get('bot_prefix')}latency",
            value="Shows you my latency in milliseconds (ms).",
            inline=False)
        embed.add_field(name="**Surfing:**",
                        value="My surfing commands are:", inline=False)
        embed.add_field(
            name=f"{self.config_data.get('bot_prefix')}define <word>",
            value="Shows you the definition of any word.",
            inline=False)

        if missing_perms:
            embed.set_footer(
                text="Notice: You are missing permissions to view certain commands.")

        await author.send(embed=embed)

