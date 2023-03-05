"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

raid_prevention.py stores the raid prevention commands for Anubis.
raid_prevention.py was last updated on 05/03/23 at 20:49 UTC.
"""

import logging
import os
import sqlite3

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils import init_logger, mkfile

init_logger()

DB_PATH = os.path.join('databases', 'anubis.db')


class RaidPrevention(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        if not os.path.exists(DB_PATH):
            logging.info(f'{DB_PATH} does not exist. Creating...')
            mkfile(DB_PATH)

        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
        self.create_tables()
        return

    @app_commands.command(
        name='lock',
        description='Locks a text channel from all default role users.')
    @app_commands.describe(
        channel='The channel to lock.')
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator:

                if interaction.guild.default_role not in channel.overwrites:
                    overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(
                        send_messages=False)}
                    await channel.edit(overwrites=overwrites)

                    embed = discord.Embed(
                        title='Lock',
                        description=f'{channel.mention} has been locked.',
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)

                elif channel.overwrites[interaction.guild.default_role].send_messages or \
                        channel.overwrites[interaction.guild.default_role] is None:
                    overwrites = channel.overwrites[interaction.guild.default_role]
                    overwrites.send_messages = False
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

                    embed = discord.Embed(
                        title='Lock',
                        description=f'{channel.mention} has been locked.',
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Lock',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Lock',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - lock(): {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='unlock',
        description='Unlocks a channel for all default role users.')
    @app_commands.describe(
        channel='The channel to unlock.')
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator:

                if interaction.guild.default_role not in channel.overwrites:
                    overwrites = {
                        interaction.guild.default_role: discord.PermissionOverwrite(
                            send_messages=True)}
                    await channel.edit(overwrites=overwrites)

                    embed = discord.Embed(
                        title="Channel unlocked",
                        description=f"{channel.name} has been unlocked.",
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)

                elif channel.overwrites[interaction.guild.default_role].send_messages is None or \
                        not channel.overwrites[interaction.guild.default_role].send_messages:
                    overwrites = channel.overwrites[interaction.guild.default_role]
                    overwrites.send_messages = True
                    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

                    embed = discord.Embed(
                        title="Channel unlocked",
                        description=f"{channel.name} has been unlocked.",
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Unlock',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Unlock',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - unlock(): {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='lockdown',
        description='Locks all channels for all default role users.')
    async def lockdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator:

                for channel in interaction.guild.text_channels:
                    if interaction.guild.default_role not in channel.overwrites:
                        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(
                            send_messages=False)}
                        await channel.edit(overwrites=overwrites)

                    elif channel.overwrites[interaction.guild.default_role].send_messages or \
                            channel.overwrites[interaction.guild.default_role] is None:
                        overwrites = channel.overwrites[interaction.guild.default_role]
                        overwrites.send_messages = False
                        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

                embed = discord.Embed(
                    title='Lockdown',
                    description='All channels have been locked.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)

            else:
                embed = discord.Embed(
                    title='Lockdown',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Lockdown',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - lockdown(): {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='unlockdown',
        description='Unlocks all channels for all default role users.')
    async def unlockdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        try:
            if interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator:

                for channel in interaction.guild.text_channels:
                    if interaction.guild.default_role not in channel.overwrites:
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(
                                send_messages=True)}
                        await channel.edit(overwrites=overwrites)

                    elif channel.overwrites[interaction.guild.default_role].send_messages is None or \
                            not channel.overwrites[interaction.guild.default_role].send_messages:
                        overwrites = channel.overwrites[interaction.guild.default_role]
                        overwrites.send_messages = True
                        await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)

                embed = discord.Embed(
                    title='Unlockdown',
                    description='All channels have been unlocked.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)

            else:
                embed = discord.Embed(
                    title='Unlockdown',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Unlockdown',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - unlockdown(): {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='toggle',
        description='Enable or disable raid prevention for your server.')
    @app_commands.describe(
        state='Whether to enable or disable raid prevention.')
    @app_commands.choices(
        state=[
            Choice(name='Enable', value=1),
            Choice(name='Disable', value=0)])
    async def toggle(self, interaction: discord.Interaction, state: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.administrator:
                if state == 1:
                    sql = '''INSERT INTO RaidPrevention (guild_id, enabled)
                        VALUES (?, ?);'''
                    if not self.__exec_nonselect(sql, interaction.guild.id, True):
                        return
                elif state == 0:
                    sql = '''DELETE FROM RaidPrevention WHERE guild_id = ?;'''
                    if not self.__exec_nonselect(sql, interaction.guild.id):
                        return
                else:
                    return
                embed = discord.Embed(
                    title='Raid Prevention',
                    description=f'Raid prevention has been {state == 1 and "enabled" or "disabled"}.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to toggle.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - toggle(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return

    @app_commands.command(
        name='set-log-channel',
        description='Set the channel to log raid prevention messages to.')
    @app_commands.describe(
        channel='The channel to log raid prevention messages to.')
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.administrator:
                sql = '''UPDATE RaidPrevention SET log_channel = ? WHERE guild_id = ?;'''

                if not self.__exec_nonselect(sql, channel.id, interaction.guild.id):
                    return

                embed = discord.Embed(
                    title='Raid Prevention',
                    description=f'Raid prevention log channel has been set to {channel.mention}.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to set the log channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - set_log_channel(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return

    @app_commands.command(
        name='prevent',
        description='Prevent a user from raiding.')
    @app_commands.describe(
        user='The user to prevent from raiding.',
        reason='The reason for preventing the user from raiding.')
    async def prevent(self, interaction: discord.Interaction, user: discord.Member, reason: str = '') -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator:
                if self.check_member_prevented(user):
                    embed = discord.Embed(
                        title='Raid Prevention',
                        description=f'{user.mention} is already prevented from raiding.',
                        color=discord.Color.blue())
                    await interaction.followup.send(embed=embed)
                    return
                sql = '''INSERT INTO Users (user_id, reason) VALUES (?, ?);'''
                if not self.__exec_nonselect(sql, user.id, reason):
                    return
                embed = discord.Embed(
                    title='Raid Prevention',
                    description=f'{user.mention} has been prevented from raiding.',
                    color=discord.Color.blue())
                if reason:
                    embed.add_field(name='Reason', value=reason, inline=True)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to prevent {user.mention} from raiding.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - prevent(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        sql = '''INSERT INTO RaidPrevention (guild_id, enabled) VALUES (?, ?);'''
        self.__exec_nonselect(sql, guild.id, True)
        return

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if self.check_guild_prevented(member.guild):
            if self.check_member_prevented(member):
                await member.kick()
                if channel_id := self.get_log_channel(member.guild):
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        embed = discord.Embed(
                            title='Raid Prevention',
                            description=f'{member.mention} has been kicked for raid prevention.',
                            color=discord.Color.blue())
                        await channel.send(embed=embed)
        return

    def create_tables(self) -> bool:
        sql = '''CREATE TABLE IF NOT EXISTS RaidPrevention (
            guild_id UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            log_channel UNSIGNED BIG INT NOT NULL DEFAULT 0,
            enabled BOOLEAN NOT NULL DEFAULT FALSE);'''
        if not self.__exec_nonselect(sql):
            return False

        sql = '''CREATE TABLE IF NOT EXISTS Users (
            user_id UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            reason TEXT NOT NULL DEFAULT '');'''
        if not self.__exec_nonselect(sql):
            return False

        return True

    def check_member_prevented(self, member: discord.Member) -> bool:
        sql = '''SELECT user_id FROM Users WHERE user_id = ?;'''
        self.__exec_select(sql, member.id)
        return self.c.fetchone() is not None

    def check_guild_prevented(self, guild: discord.Guild) -> bool:
        sql = '''SELECT guild_id FROM RaidPrevention WHERE guild_id = ?;'''
        self.__exec_select(sql, guild.id)
        return self.c.fetchone() is not None

    def get_log_channel(self, guild: discord.Guild) -> int:
        sql = '''SELECT log_channel FROM RaidPrevention WHERE guild_id = ?;'''
        self.__exec_select(sql, guild.id)
        return self.c.fetchone()[0]

    def __exec_select(self, query: str, *args) -> bool:
        try:
            self.c.execute(query, args)
            return True
        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - __exec_select(): {e}')
            return False

    def __exec_nonselect(self, query: str, *args) -> bool:
        try:
            self.c.execute(query, args)
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(
                f'Error in raid_prevention.py - __exec_nonselect(): {e}')
            return False


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RaidPrevention(bot))
