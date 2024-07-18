"""
raid_prevention.py

This namespace contains the Anubis raid prevention command cog,
which provides commands to prevent raiders from joining the server.
A part of the genuine commands included in the Anubis raider for social engineering.
"""

import asyncio
import os
import pathlib
import sqlite3
import typing

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import shared.utils.utils_io as iou
import shared.utils.utils_log as lu

DB_PATH = pathlib.Path(os.path.join('databases', 'anubis.db'))
TABLE_RAID_PREVENTION = 'RaidPrevention'
TABLE_USERS = 'Users'
COLUMN_GUILD_ID = 'guild_id'
COLUMN_LOG_CHANNEL = 'log_channel'
COLUMN_ENABLED = 'enabled'
COLUMN_USER_ID = 'user_id'
COLUMN_REASON = 'reason'


class RaidPrevention(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        if not DB_PATH.exists():
            lu.sinfo(f'{DB_PATH} does not exist, creating it now...')
            iou.mkfile(DB_PATH, None)

        self.conn = sqlite3.connect(DB_PATH)
        self.c = self.conn.cursor()
        self.create_tables()

    @app_commands.command(
    name='lock',
    description='Locks a text channel from all default role users.')
    @app_commands.describe(
        channel='The channel to lock.')
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Locks a channel for all default role users.

        Args:
            interaction (discord.Interaction): the interaction object
            channel (discord.TextChannel): the channel to lock
        """
        await interaction.response.defer(ephemeral=True)

        if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
            embed = discord.Embed(
                title='Lock',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            return

        try:
            default_role_overwrite = channel.overwrites_for(interaction.guild.default_role)

            if default_role_overwrite and default_role_overwrite.send_messages == False:
                embed = discord.Embed(
                    title='Lock',
                    description=f'{channel.mention} is already locked.',
                    color=discord.Color.blue())
            else:
                await channel.set_permissions(interaction.guild.default_role, send_messages=False)
                embed = discord.Embed(
                    title='Lock',
                    description=f'{channel.mention} has been locked.',
                    color=discord.Color.blue())

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Lock',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error locking the channel {channel.name} in {channel.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='unlock',
    description='Unlocks a channel for all default role users.')
    @app_commands.describe(
        channel='The channel to unlock.')
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Unlocks a channel for all default role users.

        Args:
            interaction (discord.Interaction): the interaction object
            channel (discord.TextChannel): the channel to unlock
        """
        await interaction.response.defer(ephemeral=True)

        if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
            embed = discord.Embed(
                title='Unlock',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            return

        try:
            default_role_overwrite = channel.overwrites_for(interaction.guild.default_role)

            if not default_role_overwrite or default_role_overwrite.send_messages == True:
                embed = discord.Embed(
                    title='Unlock',
                    description=f'{channel.mention} is already unlocked.',
                    color=discord.Color.blue())
            else:
                await channel.set_permissions(interaction.guild.default_role, send_messages=True)
                embed = discord.Embed(
                    title='Unlock',
                    description=f'{channel.mention} has been unlocked.',
                    color=discord.Color.blue())

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Unlock',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error unlocking the channel {channel.name} in {channel.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='lockdown',
    description='Locks all channels for all default role users.')
    async def lockdown(self, interaction: discord.Interaction):
        """Locks all channels for all default role users.

        Args:
            interaction (discord.Interaction): the interaction object
        """
        await interaction.response.defer(ephemeral=True)

        if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
            embed = discord.Embed(
                title='Lockdown',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            return

        try:
            old_channels = interaction.guild.text_channels
            tasks = []
            for channel in interaction.guild.text_channels:
                default_role_overwrite = channel.overwrites_for(interaction.guild.default_role)

                if not default_role_overwrite or default_role_overwrite.send_messages in [True, None]:
                    task = channel.set_permissions(interaction.guild.default_role, send_messages=False)
                    tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result, channel in zip(results, old_channels):
                if isinstance(result, Exception):
                    lu.swarning(f'There was an error locking down {channel.name} in {channel.guild.name}: {result}')
                else:
                    lu.sinfo(f'Locked down {channel.name} in {channel.guild.name}')

            embed = discord.Embed(
                title='Lockdown',
                description='All channels have been locked.',
                color=discord.Color.blue())
            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Lockdown',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error locking down {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='unlockdown',
    description='Unlocks all channels for all default role users.')
    async def unlockdown(self, interaction: discord.Interaction):
        """Unlocks all channels for all default role users.

        Args:
            interaction (discord.Interaction): the interaction object
        """
        await interaction.response.defer(ephemeral=True)

        if not (interaction.user.guild_permissions.manage_channels or interaction.user.guild_permissions.administrator):
            embed = discord.Embed(
                title='Unlockdown',
                description='You do not have permission to use this command.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            return

        old_channels = interaction.guild.text_channels
        tasks = []
        
        for channel in interaction.guild.text_channels:
            default_role_overwrite = channel.overwrites_for(interaction.guild.default_role)

            if default_role_overwrite is None or default_role_overwrite.send_messages in [False, None]:
                tasks.append(channel.set_permissions(interaction.guild.default_role, send_messages=True))

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result, channel in zip(results, old_channels):
                if isinstance(result, Exception):
                    lu.swarning(f'There was an error unlocking {channel.name} in {channel.guild.name}: {result}')
                else:
                    lu.sinfo(f'Unlocked {channel.name} in {channel.guild.name}')

            embed = discord.Embed(
                title='Unlockdown',
                description='All channels have been unlocked.',
                color=discord.Color.blue())
            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Unlockdown',
                description='I do not have permission to manage channels.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error unlocking {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='toggle',
    description='Enable or disable raid prevention for your server.')
    @app_commands.describe(
        state='Whether to enable or disable raid prevention.')
    @app_commands.choices(
        state=[
            app_commands.Choice(name='Enable', value=1),
            app_commands.Choice(name='Disable', value=0)])
    async def toggle(self, interaction: discord.Interaction, state: int):
        """Toggle raid prevention for your server.

        Args:
            interaction (discord.Interaction): the interaction object
            state (int): whether to enable or disable raid prevention
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not interaction.user.guild_permissions.administrator:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)
                return

            sql = f'''INSERT INTO {TABLE_RAID_PREVENTION} ({COLUMN_GUILD_ID}, {COLUMN_ENABLED}) 
                    VALUES (?, ?)
                    ON CONFLICT ({COLUMN_GUILD_ID}) DO UPDATE SET {COLUMN_ENABLED} = excluded.enabled;'''

            if not self.__exec_nonselect(sql, interaction.guild.id, state):
                return

            embed = discord.Embed(
                title='Raid Prevention',
                description=f'Raid prevention has been {"enabled" if state else "disabled"}.',
                color=discord.Color.blue())
            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to toggle.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error toggling raid prevention for {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='set-log-channel',
    description='Set the channel to log raid prevention messages to.')
    @app_commands.describe(
        channel='The channel to log raid prevention messages to.')
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Sets the channel to log raid prevention messages to.

        Args:
            interaction (discord.Interaction): the interaction object
            channel (discord.TextChannel): the channel to log raid prevention messages to
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not interaction.user.guild_permissions.administrator:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)
                return

            sql = f'''UPDATE {TABLE_RAID_PREVENTION} 
                        SET {COLUMN_LOG_CHANNEL} = ? 
                        WHERE {COLUMN_GUILD_ID} = ?;'''

            if not self.__exec_nonselect(sql, channel.id, interaction.guild.id):
                return

            embed = discord.Embed(
                title='Raid Prevention',
                description=f'Raid prevention log channel has been set to {channel.mention}.',
                color=discord.Color.blue())
            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to set the log channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error setting the log channel for {interaction.guild.name}: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
    name='prevent',
    description='Prevent a user from raiding.')
    @app_commands.describe(
        user='The user to prevent from raiding.',
        reason='The reason for preventing the user from raiding.')
    async def prevent(self, interaction: discord.Interaction, user: discord.Member, reason: str = ''):
        """Prevent a user from raiding.

        Args:
            interaction (discord.Interaction): tne interaction object
            user (discord.Member): the user to prevent from raiding
            reason (str, optional): the reason as to why the user is prevented. Defaults to ''.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            if not interaction.user.guild_permissions.ban_members and not interaction.user.guild_permissions.administrator:
                embed = discord.Embed(
                    title='Raid Prevention',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)
                return

            if self.check_member_prevented(user):
                embed = discord.Embed(
                    title='Raid Prevention',
                    description=f'{user.mention} is already prevented from raiding.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
                return

            sql = f'''INSERT INTO {TABLE_USERS} 
                    ({COLUMN_USER_ID}, {COLUMN_REASON}) 
                    VALUES (?, ?);'''
            if not self.__exec_nonselect(sql, user.id, reason):
                return

            embed = discord.Embed(
                title='Raid Prevention',
                description=f'{user.mention} has been prevented from raiding.',
                color=discord.Color.blue())
            if reason:
                embed.add_field(name='Reason', value=reason, inline=True)
            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to prevent {user.mention} from raiding.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'There was an error preventing {user} from raiding: {e}')
            await interaction.followup.send(f'Error: {e}')
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """The event that is called when the bot joins a guild

        Args:
            guild (discord.Guild): the guild that the bot joined
        """
        sql = f'''INSERT INTO {TABLE_RAID_PREVENTION} (
            {COLUMN_GUILD_ID}, 
            {COLUMN_ENABLED}) VALUES (?, ?);'''
        self.__exec_nonselect(sql, guild.id, True)
    
    def create_tables(self) -> bool:
        """Generates the tables for the Anubis database

        Returns:
            bool: the success of the operation
        """
        
        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_RAID_PREVENTION} (
            {COLUMN_GUILD_ID} UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            {COLUMN_LOG_CHANNEL} UNSIGNED BIG INT NOT NULL DEFAULT 0,
            {COLUMN_ENABLED} BOOLEAN NOT NULL DEFAULT FALSE);'''

        if not self.__exec_nonselect(sql):
            return False

        sql = f'''CREATE TABLE IF NOT EXISTS {TABLE_USERS} (
            {COLUMN_USER_ID} UNSIGNED BIG INT NOT NULL PRIMARY KEY,
            {COLUMN_REASON} TEXT NOT NULL DEFAULT '');'''

        if not self.__exec_nonselect(sql):
            return False

        return True

    def is_member_prevented(self, member: discord.Member) -> bool:
        """Whether or not a member is prevented from joining the server

        Args:
            member (discord.Member): the member to check

        Returns:
            bool: whether or not the member is prevented
        """
        sql = f'''SELECT {COLUMN_USER_ID} FROM {TABLE_USERS} 
                    WHERE {COLUMN_USER_ID} = ?;'''
        return self.__exec_select_one(sql, member.id) is not None
    
    def does_guild_prevent(self, guild: discord.Guild) -> bool:
        """Whether or not a guild prevents raiders from joining

        Args:
            guild (discord.Guild): the guild to check

        Returns:
            bool: whether or not the guild prevents raiders from joining
        """
        sql = f'''SELECT {COLUMN_GUILD_ID} FROM {TABLE_RAID_PREVENTION} 
                    WHERE {COLUMN_GUILD_ID} = ?;'''
        return self.__exec_select_one(sql, guild.id) is not None
    
    def get_log_channel(self, guild: discord.Guild) -> int:
        """The log channel of the guild for this cog

        Args:
            guild (discord.Guild): the guild to check

        Returns:
            int: the log channel id of the guild
        """
        if not self.does_guild_prevent(guild):
            return 0
        sql = f'''SELECT {COLUMN_LOG_CHANNEL} FROM {TABLE_RAID_PREVENTION} 
                    WHERE {COLUMN_GUILD_ID} = ?;'''
        if (data := self.__exec_select_one(sql, guild.id)) is None:
            return 0
        else:
            return data[0]
    
    def __exec_select_one(self, query: str, *args: typing.Tuple[typing.Any, ...]) -> typing.Any:
        """Returns the first row of a query

        Args:
            query (str): the query to execute

        Returns:
            typing.Any: the first row of the query
        """
        try:
            self.c.execute(query, args)
            return self.c.fetchone()  
        except Exception as e:
            lu.serror(f'Failed to execute query: {query} with args: {args} due to error: {e}')
            return None
    
    def __exec_nonselect(self, query: str, *args: typing.Tuple[typing.Any, ...]) -> bool:
        """Returns the success of a non-select query

        Args:
            query (str): the query to execute

        Returns:
            bool: the success of the query
        """
        try:
            self.c.execute(query, args)
            self.conn.commit()
            return True
        except Exception as e:
            lu.serror(f'Failed to execute query: {query} with args: {args} due to error: {e}')
            return False
    


async def setup(bot):
    await bot.add_cog(RaidPrevention(bot))
