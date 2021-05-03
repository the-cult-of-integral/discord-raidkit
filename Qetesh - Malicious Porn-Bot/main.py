# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).


# Modules.

import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from cogs.qetesh_methods import DATA, check_for_run_settings, write_temp, check_for_servers, display_start_error, display_title_screen, search_for_updates
from colorama import Fore, init
init()


# Check for basic files needed and write the temp file.

DATA = check_for_run_settings()
write_temp()
check_for_servers()


# Sets the bot prefix to the prefix specified in the JSON file.

if DATA.get("prefix").strip().replace(" ", "") == "":
    display_start_error("No prefix!")
else:
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=DATA.get("prefix"), intents=intents)


# Status' to be cycled continously as the bot runs.
# You add or change these status' here - make sure to have at least one.

status = cycle(['with myself!', f'{DATA.get("prefix")}help for commands!'])


# Removes the default help command (Help command is replaced by an embed
# further down in the code).

bot.remove_command('help')


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
    elif isinstance(error, commands.NSFWChannelRequired):
        embed = discord.Embed(
            title="Error",
            description=f"**You must be in a NSFW channel to use this command.**",
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
@commands.is_nsfw()
async def help(ctx):
    embed = discord.Embed(colour=discord.Color.gold())
    embed.set_author(name=f"Here's a list of my commands!")
    embed.add_field(name=f"{DATA.get('prefix')}vagl", value="Display an image of vaginal sex.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}oral", value="Display an image of oral sex.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}anal", value="Display an image of anal sex.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}les", value="Display an image of lesbian sex.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}gay", value="Display an image of gay sex.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}tits", value="Display an image of tits.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}ass", value="Display an image of an ass.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}pussy", value="Display an image of a pussy.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}cock", value="Display an image of a cock.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}asian", value="Display an image of an asian.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}amateur", value="Display an image of an amateur.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}hentai", value="Display an image of hentai.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}milf", value="Display an image of a milf.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}teen", value="Display an image of a teen (18/19).", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}ebony", value="Display an image of an ebony.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}threesome", value="Display an image of a threesome.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}cartoon", value="Display an image of cartoon porn.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}creampie", value="Display an image of a creampie.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}bondage", value="Display an image of bondage.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}squirt", value="Display an image of squirting.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}neko", value="Display an image of neko.", inline=True)
    embed.add_field(name=f"{DATA.get('prefix')}yiff", value="Display an image of yiff.", inline=True)
    await ctx.message.channel.send(embed=embed)
    return


# Search for updates.

search_for_updates()
os.system('cls')
print(f"{Fore.LIGHTGREEN_EX}Loading Qetesh - please wait.{Fore.RESET}")

# Cycle through status every ten seconds.
# Change this value to however long you want each status to last (integer).


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# Search the "Cogs" folder for Cogs.

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and "qetesh" not in filename:
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        continue

# Run the bot using the token specified in the JSON file.

try:
    bot.run(DATA.get("bot_token"))
except BaseException as e:
    display_start_error(e)

# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
