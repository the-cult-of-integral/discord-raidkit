# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).


# Modules.

import discord
import os
import json
import asyncpg
import random as r
import requests
import re
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from itertools import cycle
from cogs.anubis_methods import DATA, check_for_run_settings, write_temp, check_for_servers, display_start_error, display_title_screen, search_for_updates
from colorama import Style, Back, Fore, init
init()


# Check for basic files needed and write the temp file.

DATA = check_for_run_settings()
write_temp()
check_for_servers()


# Sets the bot prefix to the prefix specified in the JSON file.

if DATA.get("prefix").strip().replace(" ", "") == "":
    display_start_error()
else:
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=DATA.get("prefix"), intents=intents)


# Status' to be cycled continously as the bot runs.
# You add or change these status' here - make sure to have at least one.

status = cycle(['against raiders!', f'{DATA.get("prefix")}help for commands!'])


# Removes the default help command (Help command is replaced by an embed
# further down in the code).

bot.remove_command('help')


# Creates the database pool from the postresql database "levels_db" set up
# in the installation (See README.md).

async def create_db_pool():
    try:
        bot.pg_con = await asyncpg.create_pool(database="levels_db", user="postgres", password=DATA.get("postgresql_password"))
    except BaseException:
        display_start_error()


# Load/Unload/Reload: Used for messing with Cogs.

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(
        title="Extension loaded",
        description=f"{extension} has been loaded.",
        color=discord.Colour.green())
    await ctx.send(embed=embed)


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    embed = discord.Embed(
        title="Extension unloaded",
        description=f"{extension} has been unloaded.",
        color=discord.Colour.green())
    await ctx.send(embed=embed)


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(
        title="Extension reloaded",
        description=f"{extension} has been reloaded.",
        color=discord.Colour.green())
    await ctx.send(embed=embed)


# On ready.

@bot.event
async def on_ready():
    change_status.start()
    display_title_screen()


# On joining a server.

@bot.event
async def on_guild_join(guild):
    with open('cogs/servers.txt', 'a') as f:
        f.write(str(guild.id) + "\n")
        f.close()


# On error (error handling).

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Error",
            description=f"**Command does not exist.**",
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error",
            description=f"**Permission denied.**",
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="Error",
            description=f"**You must be the owner of the bot to use this command.**",
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="Error",
            description=f"**Access denied.**",
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        print(error)


# Help embed.

@bot.command()
async def help(ctx):
    missing_perms = False
    author = ctx.message.author
    embed = discord.Embed(colour=discord.Color.gold())
    embed.set_author(name=f"Here's a list of my commands!")

    if not author.guild_permissions.manage_messages and not author.guild_permissions.kick_members and not author.guild_permissions.ban_members and not author.guild_permissions.administrator and not author.guild_permissions.mute_members:
        embed.add_field(
            name="**No permissions for moderator commands!**",
            value="You lack every permission used by the moderator commands.",
            inline=False)
        missing_perms = True
    else:
        embed.add_field(name="**Moderation:**",
                        value="My moderation commands are:", inline=False)
        if author.guild_permissions.manage_messages:
            embed.add_field(
                name=f"{DATA.get('prefix')}clear [1-1000]",
                value="Clears messages from a channel.",
                inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.kick_members:
            embed.add_field(
                name=f"{DATA.get('prefix')}kick <member> [reason]",
                value="Kicks a member from the server.",
                inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.ban_members:
            embed.add_field(
                name=f"{DATA.get('prefix')}ban <member> [reason]",
                value="Bans a member from the server.",
                inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.administrator:
            embed.add_field(
                name=f"{DATA.get('prefix')}unban <member>",
                value="Unbans a member from the server.",
                inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.mute_members:
            embed.add_field(
                name=f"{DATA.get('prefix')}mute <member> [reason]",
                value="Mutes a member on the server.",
                inline=False)
            embed.add_field(
                name=f"{DATA.get('prefix')}unmute <member>",
                value="Unmutes a member on the server.",
                inline=False)
        else:
            missing_perms = True

    if not author.guild_permissions.mute_members and not author.guild_permissions.administrator:
        embed.add_field(
            name="**No permissions for anti-raid commands!**",
            value="You lack every permission used by the anti-raid commands.",
            inline=False)
        missing_perms = True
    else:
        embed.add_field(name="**Anti-Raid:**",
                        value="My anti-raid commands are:", inline=False)
        if author.guild_permissions.administrator:
            embed.add_field(
                name=f"{DATA.get('prefix')}db_add_member <member>",
                value="Adds a member to my raider database.",
                inline=False)
            embed.add_field(
                name=f"{DATA.get('prefix')}db_del_member <member>",
                value="Removes a member from my raider database.",
                inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.mute_members:
            embed.add_field(
                name=f"{DATA.get('prefix')}lock",
                value="Locks down current text channel during a raid.",
                inline=False)
            embed.add_field(
                name=f"{DATA.get('prefix')}unlock",
                value="Unlocks current text channel after a raid.",
                inline=False)
        else:
            missing_perms = True

    embed.add_field(name="**Levelling:**",
                    value="My levelling commands are:", inline=False)
    embed.add_field(name=f"{DATA.get('prefix')}level",
                    value="Shows your current level and XP.", inline=False)
    embed.add_field(name=f"{DATA.get('prefix')}dailyxp",
                    value="Gives you your daily XP.", inline=False)
    embed.add_field(name="**Status:**",
                    value="My status commands are:", inline=False)
    embed.add_field(
        name=f"{DATA.get('prefix')}latency",
        value="Shows you my latency in milliseconds (ms).",
        inline=False)
    embed.add_field(name="**Surfing:**",
                    value="My surfing commands are:", inline=False)
    embed.add_field(
        name=f"{DATA.get('prefix')}define <word>",
        value="Shows you the definition of any word.",
        inline=False)

    if missing_perms:
        embed.set_footer(
            text="Notice: You are missing permissions to view certain commands.")

    await author.send(embed=embed)


# Search for updates.

search_for_updates()
os.system('cls')
print(f"{Fore.LIGHTGREEN_EX}Loading Anubis - please wait.{Fore.RESET}")

# Cycle through status every ten seconds.
# Change this value to however long you want each status to last (integer).


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# Search the "Cogs" folder for Cogs.

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and "anubis" not in filename:
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        continue


# Asycio loop.

bot.loop.run_until_complete(create_db_pool())

# Run the bot using the token specified in the JSON file.

try:
    bot.run(DATA.get("token"))
except BaseException:
    display_start_error()

# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
