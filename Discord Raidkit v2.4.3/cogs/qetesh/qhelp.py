"""
Discord Raidkit v2.4.3
the-cult-of-integral

Last modified: 2023-04-24 21:08
"""

import discord
import discord.app_commands as app_commands
import discord.ext.commands as commands

import tools.raider as rd
import utils.log_utils as lu


class Help(commands.Cog):
    def __init__(self, bot: rd.Raider):
        self.bot: rd.Raider = bot
        return

    @app_commands.command(
        name='help',
        description='Displays the help command.')
    async def help(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            embed = discord.Embed(
                title='Commands',
                color=discord.Color.gold())

            embed.add_field(
                name='see', value='View an image from an image category', inline=True)
            embed.add_field(
                name='toggle-cmd', value='Toggle whether a command is enabled', inline=True)
            embed.add_field(name='toggle-only-nsfw',
                            value='Toggle whether NSFW commands are restricted to NSFW channels', inline=True)

            await interaction.followup.send(embed=embed)

        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Action Forbidden',
                description='I do not have the required permissions to send embeds to this channel.',
                color=discord.Color.brand_red())
            await interaction.followup.send(embed=embed)

        except Exception as e:
            lu.swarning(f'Error sending help message: {e}')
            await interaction.followup.send(f'Error: {e}')

        return


async def setup(bot: rd.Raider):
    await bot.add_cog(Help(bot))
