"""
moderation.py

This namespace contains the Anubis moderation command cog,
which provides commands for managing members in a Discord server.
A part of the genuine commands included in the Anubis raider for social engineering.
"""

import datetime

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import shared.utils.utils_log as lu


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
    name='clear',
    description='Clears a number of latest messages from a text channel.')
    @app_commands.describe(
        number='The number of messages to clear.')
    async def clear(self, interaction: discord.Interaction, number: int):
        """Clear a number of messages from a text channel.

        Args:
            interaction (discord.Interaction): the interaction object
            number (int): the number of messages to clear

        Raises:
            discord.errors.Forbidden: no permission to clear messages
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator):
                raise discord.errors.Forbidden(f'You do not have permission to use this command.')

            deleted_messages = await interaction.channel.purge(limit=number)

            embed = discord.Embed(
                title='Clear',
                description=f'{interaction.channel.mention} has been cleared by {len(deleted_messages)} messages.',
                color=discord.Color.blue())

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden as e:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to clear {interaction.channel.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error while clearing messages: {e}')
            await interaction.followup.send(f'Error: {e}')
    
    @app_commands.command(
        name='timeout',
        description='Timeout a user for a number of minutes, with an optional message.')
    @app_commands.describe(
        member='The member to timeout.',
        minutes='The number of minutes to timeout the member for.',
        reason='The reason for the timeout.',
        send_message='Whether to send a message to the member with the reason.')
    @app_commands.choices(
        send_message=[
            app_commands.Choice(name='Yes', value=1),
            app_commands.Choice(name='No', value=0)
        ])
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, 
                      minutes: int, reason: str, send_message: int):
        """Timeout a member for a number of minutes, with an optional message.

        Args:
            interaction (discord.Interaction): the interaction object
            member (discord.Member): the member to timeout
            minutes (int): the number of minutes to timeout the member for
            reason (str): the reason for the timeout
            send_message (int): whether to send a message to the member with the reason

        Raises:
            discord.errors.Forbidden: no permission to timeout members
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not (interaction.user.guild_permissions.moderate_members or interaction.user.guild_permissions.administrator):
                raise discord.errors.Forbidden(f'You do not have permission to use this command.')

            await member.timeout(datetime.timedelta(minutes=minutes), reason=reason)

            embed = discord.Embed(
                title='Timeout',
                description=f'{member.mention} has been timed out for {minutes} minutes.',
                color=discord.Color.blue())

            if reason:
                embed.add_field(name='Reason', value=reason, inline=True)

            await interaction.followup.send(embed=embed)

            if send_message:
                message_embed = discord.Embed(
                    title='Timeout',
                    description=f'You have been timed out for {minutes} minutes.',
                    color=discord.Color.blue())
                if reason:
                    message_embed.add_field(name='Reason', value=reason, inline=True)
                message_embed.set_footer(text=f'Server: {interaction.guild.name}')

                await member.send(embed=message_embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to timeout {member.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error while timing out member: {e}')
            await interaction.followup.send(f'Error: {e}')

    @app_commands.command(
        name='kick',
        description='Kick a user from the server.')
    @app_commands.describe(
        member='The member to kick.',
        reason='The reason for the kick.',
        send_message='Whether to send a message to the member with the reason.')
    @app_commands.choices(
        send_message=[
            app_commands.Choice(name='Yes', value=1),
            app_commands.Choice(name='No', value=0)
        ])
    async def kick(self, interaction: discord.Interaction, member: discord.Member, 
                   reason: str, send_message: int):
        """Kick a member from the server.

        Args:
            interaction (discord.Interaction): the interaction object
            member (discord.Member): the member to kick
            reason (str): the reason for the kick
            send_message (int): whether to send a message to the member with the reason

        Raises:
            discord.errors.Forbidden: no permission to kick members
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not (interaction.user.guild_permissions.kick_members or interaction.user.guild_permissions.administrator):
                raise discord.errors.Forbidden(f'You do not have permission to use this command.')

            await member.kick(reason=reason)

            embed = discord.Embed(
                title='Kick',
                description=f'{member.mention} has been kicked from {interaction.guild.name}.',
                color=discord.Color.blue())

            if reason:
                embed.add_field(name='Reason', value=reason, inline=True)

            await interaction.followup.send(embed=embed)

            if send_message:
                message_embed = discord.Embed(
                    title='Kick',
                    description=f'You have been kicked from {interaction.guild.name}.',
                    color=discord.Color.blue())
                if reason:
                    message_embed.add_field(name='Reason', value=reason, inline=True)
                message_embed.set_footer(text=f'Server: {interaction.guild.name}')

                await member.send(embed=message_embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to kick {member.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error while kicking member: {e}')
            await interaction.followup.send(f'Error: {e}')
    
    @app_commands.command(
        name='ban',
        description='Ban a user from the server.')
    @app_commands.describe(
        member='The member to ban.',
        reason='The reason for the ban.',
        send_message='Whether to send a message to the member with the reason.')
    @app_commands.choices(
        send_message=[
            app_commands.Choice(name='Yes', value=1),
            app_commands.Choice(name='No', value=0)
        ])
    async def ban(self, interaction: discord.Interaction, member: discord.Member, 
                  reason: str, send_message: int):
        """Bans a member from the server.

        Args:
            interaction (discord.Interaction): the interaction object
            member (discord.Member): the member to ban
            reason (str): the reason for the ban
            send_message (int): whether to send a message to the member with the reason

        Raises:
            discord.errors.Forbidden: no permission to ban members
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not (interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator):
                raise discord.errors.Forbidden(f'You do not have permission to use this command.')

            await member.ban(reason=reason)

            embed = discord.Embed(
                title='Ban',
                description=f'{member.mention} has been banned from {interaction.guild.name}.',
                color=discord.Color.blue())

            if reason:
                embed.add_field(name='Reason', value=reason, inline=True)

            await interaction.followup.send(embed=embed)

            if send_message:
                message_embed = discord.Embed(
                    title='Ban',
                    description=f'You have been banned from {interaction.guild.name}.',
                    color=discord.Color.blue())
                if reason:
                    message_embed.add_field(name='Reason', value=reason, inline=True)
                message_embed.set_footer(text=f'Server: {interaction.guild.name}')

                await member.send(embed=message_embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to ban {member.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error while banning member: {e}')
            await interaction.followup.send(f'Error: {e}')
    
    @app_commands.command(
        name='unban',
        description='Unban a user from the server.')
    @app_commands.describe(
        member='The member to unban.',
        reason='The reason for the unban.')
    async def unban(self, interaction: discord.Interaction, member: discord.Member, 
                    reason: str):
        """Unbans a member from the server.

        Args:
            interaction (discord.Interaction): the interaction object
            member (discord.Member): the member to unban
            reason (str): the reason for the unban

        Raises:
            discord.errors.Forbidden: no permission to unban members
        """
        try:
            await interaction.response.defer(ephemeral=True)

            if not (interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator):
                raise discord.errors.Forbidden(f'You do not have permission to use this command.')

            await interaction.guild.unban(member, reason=reason)

            embed = discord.Embed(
                title='Unban',
                description=f'{member.mention} has been unbanned from {interaction.guild.name}.',
                color=discord.Color.blue())

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description=f'I do not have the required permissions to unban {member.mention}.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error while unbanning member: {e}')
            await interaction.followup.send(f'Error: {e}')

            
async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
