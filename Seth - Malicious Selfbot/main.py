# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).


# Modules.

import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from cogs.seth_methods import DATA, check_for_run_settings, write_temp, check_for_servers, display_start_error, display_title_screen, search_for_updates
from colorama import Fore, init
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
    bot = commands.Bot(command_prefix=DATA.get("prefix"), self_bot=True, intents=intents)

bot.remove_command('help')


# Load/Unload/Reload: Used for messing with Cogs.

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    print(f"{Fore.WHITE}{extension} {Fore.LIGHTGREEN_EX}has been loaded.")
    return


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    print(f"{Fore.WHITE}{extension} {Fore.LIGHTGREEN_EX}has been unloaded.")
    return


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print(f"{Fore.WHITE}{extension} {Fore.LIGHTGREEN_EX}has been reloaded.")
    return


# On ready.

@bot.event
async def on_ready():
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
        print(f"{Fore.LIGHTRED_EX}Command does not exist.")
    elif isinstance(error, commands.MissingPermissions):
        print(f"{Fore.LIGHTRED_EX}Permission denied.")
    elif isinstance(error, commands.CheckFailure):
        print(f"{Fore.LIGHTRED_EX}Access denied.")
    else:
        print(f"{Fore.LIGHTRED_EX}{error}")


# Search for updates.

search_for_updates()
os.system('cls')
print(f"{Fore.LIGHTGREEN_EX}Loading Seth - please wait.{Fore.RESET}")

# Cycle through status every ten seconds.
# Change this value to however long you want each status to last (integer).


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


# Search the "Cogs" folder for Cogs.

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and "seth" not in filename:
        bot.load_extension(f'cogs.{filename[:-3]}')
    else:
        continue


# Run the bot using the token specified in the JSON file.

try:
    bot.run(DATA.get("user_token"), bot=False)
except BaseException:
    display_start_error()

# Scripted by Catterall (https://github.com/Catterall).
# Bot under the GNU General Public Liscense v2 (1991).
