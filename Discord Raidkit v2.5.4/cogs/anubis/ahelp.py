"""
ahelp.py

This namespace contains the Anubis help command cog,
which provides an embed help message for the genuine commands
included in the Anubis raider for social engineering.
"""

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import shared.utils.utils_log as lu


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @app_commands.command(
    name='help',
    description='Displays the help command.')
    async def help(self, interaction: discord.Interaction):
        """Sends a help embedded message to the user

        Args:
            interaction (discord.Interaction): the interaction object
        """
        try:
            await interaction.response.defer(ephemeral=True)
            missing_perms = False
            author = interaction.user
            embed = discord.Embed(color=discord.Color.gold())
            embed.set_author(name=f"Here's a list of my commands!")
            
            if not author.guild_permissions.manage_messages and not author.guild_permissions.kick_members and not \
                    author.guild_permissions.ban_members and not author.guild_permissions.administrator and not \
                    author.guild_permissions.moderate_members:
                embed.add_field(
                    name=":no_entry_sign: **No permissions for moderator commands!**",
                    value="You lack every permission used by the moderator commands.",
                    inline=False)
                missing_perms = True
            else:
                embed.add_field(
                    name=":tools: **Moderation:**",
                    value="Use these commands to manage your server:",
                    inline=False)
                if author.guild_permissions.manage_messages:
                    embed.add_field(
                        name="`clear <number>`",
                        value="Clears messages from a channel.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.kick_members:
                    embed.add_field(
                        name="`kick <member> <reason>`",
                        value="Kicks a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.ban_members:
                    embed.add_field(
                        name="`ban <member> <reason>`",
                        value="Bans a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.administrator:
                    embed.add_field(
                        name="`unban <member>`",
                        value="Unbans a member from the server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.mute_members:
                    embed.add_field(
                        name="`timeout <member> <reason>`",
                        value="Timeout a member on the server.",
                        inline=False)
                else:
                    missing_perms = True
                embed.add_field(
                    name="\u200b",
                    value="\u200b",
                    inline=False)
                
            if not author.guild_permissions.mute_members and not author.guild_permissions.administrator:
                embed.add_field(
                    name=":no_entry_sign: **No permissions for anti-raid commands!**",
                    value="You lack every permission used by the anti-raid commands.",
                    inline=False)
                missing_perms = True
            
            else:
                embed.add_field(
                    name=":shield: **Anti-Raid:**",
                    value="Use these commands to protect your server from raids:",
                    inline=False)
                if author.guild_permissions.administrator:
                    embed.add_field(
                        name="`prevent <member>`",
                        value="Adds a member to my raider database.",
                        inline=False)
                    embed.add_field(
                        name="`set-log-channel <channel>`",
                        value="Set my anti-raid log channel.",
                        inline=False)
                    embed.add_field(
                        name="`toggle <state>`",
                        value="Turn my anti-raid features on or off on your server.",
                        inline=False)
                else:
                    missing_perms = True
                if author.guild_permissions.mute_members:
                    embed.add_field(
                        name="`lock <channel>`",
                        value="Locks down a text channel during a raid.",
                        inline=False)
                    embed.add_field(
                        name="`unlock <channel>`",
                        value="Unlocks a text channel after a raid.",
                        inline=False)
                    embed.add_field(
                        name="`lockdown`",
                        value="Locks all channels during a raid.",
                        inline=False)
                    embed.add_field(
                        name="`unlockdown`",
                        value="Unlocks all text channel after a raid.",
                        inline=False)
                else:
                    missing_perms = True
                embed.add_field(
                    name="\u200b",
                    value="\u200b",
                    inline=False)
            
            embed.add_field(
                name=":surfer: **Surfing:**",
                value="Use this command to learn new words:",
                inline=False)
            
            embed.add_field(
                name="`define <word>`",
                value="Shows you the definition of any word.",
                inline=False)
            
            if missing_perms:
                embed.set_footer(
                    text="Notice: You are missing permissions to view certain commands.")
            
            await interaction.user.send(embed=embed)
            await interaction.followup.send('Help message sent! Not seeing it? Check your settings.')
            
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description='I do not have the required permissions to send embeds to this channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            lu.swarning(f'Error sending help message: {e}')
            await interaction.followup.send(f'Error: {e}')
                

async def setup(bot):
    await bot.add_cog(Help(bot))
