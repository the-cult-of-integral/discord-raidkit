# Scripted by Catterall (https://github.com/Catterall).
# Thoth under the GNU General Public Liscense v2 (1991).


# Modules

import json
import os
import random as r
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
from colorama import Fore, Style, init
init(convert=True)
exit_num = r.randint(1, 9999)


def clear():
    os.system('cls')


def search_for_updates():
    THIS_VERSION = "1.5.2"

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    url = f"https://github.com/Catterall/discord-raidkit/releases/latest"

    os.system('cls')
    print("Searching for updates.")
    r = requests.get(url, headers=header)
    os.system('cls')
    soup = str(BeautifulSoup(r.text, 'html.parser'))
    s1 = re.search('<title>', soup)
    s2 = re.search('·', soup)
    result_string = soup[s1.end():s2.start()]
    if THIS_VERSION not in result_string:
        s3 = re.search('originating_url":"', soup)
        s4 = re.search('","user_id":null', soup)
        update_link = soup[s3.end():s4.start()]
        print(Style.BRIGHT + Fore.LIGHTYELLOW_EX + f'''



                   ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                   ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                   ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                   ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                   ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                   ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝


              {Fore.LIGHTRED_EX}Human. There has been a brand new update to the discord raidkit. You can find the update here:

                              {Fore.LIGHTBLUE_EX}{update_link}

                                              {Fore.WHITE}(Enter anything to continue) '''.replace('█', f'{Fore.YELLOW}█{Fore.LIGHTGREEN_EX}'), end=f"\n\n{' '*59}")
        input()
        return


# Add an account to the hitlist.

def add_account():
    clear()

    def get_information_AT(new=True, existing=False):
        global exit_num
        name = ""
        discriminator = ""
        token = ""
        code = ""
        str_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        valid_token_chars = [
            'a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '.',
            '-']

        while not name:
            print(
                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's discord name ({Fore.LIGHTRED_EX}do not include the "
                f"#XXXX{Fore.LIGHTMAGENTA_EX}).")
            name = input(
                f"{Fore.LIGHTMAGENTA_EX}\nAlternatively, you can type '{Fore.LIGHTCYAN_EX}_thoth-exit_{exit_num}_{Fore.LIGHTMAGENTA_EX}' to return to the main screen.\n\n"
                f"{Fore.LIGHTRED_EX}Once you proceed past this step, you will not be able to return to the main screen until "
                f"you complete this option:\n{Fore.BLUE}")
            if not name:
                clear()
                print(f"{Fore.LIGHTRED_EX}You must provide a name.")
                sleep(2)
                clear()
            elif name == f'_thoth-exit_{exit_num}_':
                main()
            else:
                clear()
                break

        while not discriminator:
            discriminator = input(
                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's discriminator ({Fore.LIGHTCYAN_EX}the four-digit "
                f"number after the #{Fore.LIGHTMAGENTA_EX}): {Fore.BLUE}")
            if len(discriminator) != 4:
                discriminator = ""
            for num in discriminator:
                if num not in str_numbers:
                    discriminator = ""
                    break
            if not discriminator:
                clear()
                print(f"{Fore.LIGHTRED_EX}You must provide a valid discriminator.")
                sleep(2)
                clear()
            else:
                clear()
                break

        while True:
            failure = False
            token = input(
                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's token ({Fore.LIGHTCYAN_EX}If you do not know this, "
                f"enter nothing{Fore.LIGHTMAGENTA_EX}): {Fore.BLUE}")
            for char in token.lower():
                if char not in valid_token_chars:
                    failure = True
            if len(token) != 59 and token:
                failure = True
            if not token and not failure:
                token = "N/A"
                clear()
                break
            elif token and not failure:
                clear()
                break
            else:
                clear()
                print(
                    f"{Fore.LIGHTRED_EX}You must provide either a valid token, or nothing if you do not know it.")
                sleep(3)
                clear()

        while not code:
            code = input(
                f"{Fore.LIGHTMAGENTA_EX}Finally, please enter a code. This code will be used to display the "
                f"target's information at a later date with\noption [4] or to check whether the target is saved with option [5]:"
                f" {Fore.BLUE}")
            if not code:
                clear()
                print(
                    f"{Fore.RED}You must provide a code to be used as a reference point in the future.")
                sleep(3)
                clear()
            else:
                clear()
                print(
                    f"{Fore.LIGHTRED_EX}Notice: {Fore.LIGHTGREEN_EX}\nIf you lose this code, or can not remember which "
                    f"account the code is linked too,\nyou can read the json file to find out with option [6].\n\n")
                sleep(2)
                end = input(
                    f"{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
                break
        if new:
            target = {"targets": [
                {"code": code, "name": name, "discriminator": discriminator, "token": token}]}
            json.dump(target, f, indent=4)

        if existing:
            target = {"code": code, "name": name,
                      "discriminator": discriminator, "token": token}

            def write_json(data):
                with open('accounts.json', 'w') as f:
                    json.dump(data, f, indent=4)

            with open('accounts.json') as json_file:
                data = json.load(json_file)
                temp = data["targets"]
                temp.append(target)
            write_json(data)

    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
            get_information_AT(new=False, existing=True)

    else:
        get_information_AT(new=False, existing=True)


# Remove an account from the hitlist.

def del_account():
    clear()
    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
        print(f"{Fore.LIGHTRED_EX}accounts.json file not found{Fore.WHITE} - {Fore.LIGHTRED_EX}generated a new file!")
        sleep(3)
        main()

    code = ""
    global exit_num

    while not code:
        print(f"{Fore.LIGHTMAGENTA_EX}Please enter the reference code of your target.")
        code = input(
            f"{Fore.LIGHTMAGENTA_EX}\nAlternatively, you can type '{Fore.LIGHTCYAN_EX}_thoth-exit_{exit_num}_{Fore.LIGHTMAGENTA_EX}' to return to the main screen.\n\n"
            f"{Fore.LIGHTRED_EX}Once you proceed past this step, you will not be able to return to the main screen until "
            f"you complete this option:\n{Fore.BLUE}")
        if not code:
            clear()
            print(f"{Fore.LIGHTRED_EX}You must provide a reference code.")
            sleep(2)
            clear()
        if code == f'_thoth-exit_{exit_num}_':
            main()
        if code and code != f'_thoth-exit_{exit_num}_':
            with open('accounts.json') as f:
                data = json.load(f)
                clear()
                accounts = data['targets']
                i = -1
                found = False
                for account in accounts:
                    if account["code"] == code:
                        i += 1
                        found = True
                        break
                    else:
                        i += 1
            if found:
                del accounts[i]
                os.remove('accounts.json')
                target = {"targets": accounts}
                with open('accounts.json', 'w') as f:
                    json.dump(target, f, indent=4)
                print(
                    f"{Fore.LIGHTMAGENTA_EX}The target has been removed successfully.")
                sleep(2)
            else:
                print(
                    f"{Fore.LIGHTRED_EX}The specified target was not found in accounts.json.")
                sleep(2)
                del_account()

    end = input(
        f"\n\n{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
    main()


# Edit an account's details in the histlist.

def edit_account():
    str_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    valid_token_chars = [
        'a',
        'b',
        'c',
        'd',
        'e',
        'f',
        'g',
        'h',
        'i',
        'j',
        'k',
        'l',
        'm',
        'n',
        'o',
        'p',
        'q',
        'r',
        's',
        't',
        'u',
        'v',
        'w',
        'x',
        'y',
        'z',
        '0',
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '.']
    clear()
    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
        print(f"{Fore.LIGHTRED_EX}accounts.json file not found{Fore.WHITE} - {Fore.LIGHTRED_EX}generated a new file!")
        sleep(3)
        main()

    code = ""
    old_code = ""
    old_name = ""
    old_discriminator = ""
    old_token = ""
    new_code = ""
    new_name = ""
    new_discriminator = ""
    new_token = ""
    global exit_num

    while not code:
        print(f"{Fore.LIGHTMAGENTA_EX}Please enter the reference code of your target.")
        code = input(
            f"{Fore.LIGHTMAGENTA_EX}\nAlternatively, you can type '{Fore.LIGHTCYAN_EX}_thoth-exit_{exit_num}_{Fore.LIGHTMAGENTA_EX}' to return to the main screen.\n\n"
            f"{Fore.LIGHTRED_EX}Once you proceed past this step, you will not be able to return to the main screen until "
            f"you complete this option:\n{Fore.BLUE}")
        if not code:
            clear()
            print(f"{Fore.LIGHTRED_EX}You must provide a reference code.")
            sleep(2)
            clear()
        if code == f'_thoth-exit_{exit_num}_':
            main()
        if code and code != f'_thoth-exit_{exit_num}_':
            with open('accounts.json') as f:
                data = json.load(f)
                clear()
                accounts = data['targets']
                i = -1
                found = False
                for account in accounts:
                    if account["code"] == code:
                        i += 1
                        found = True
                        break
                    else:
                        i += 1
            if found:
                old_code = accounts[i]["code"]
                old_name = accounts[i]["name"]
                old_discriminator = accounts[i]["discriminator"]
                old_token = accounts[i]["token"]

                while True:
                    option = input(
                        f"{Fore.LIGHTMAGENTA_EX}Do you want to change your target's code? [Y/N]: {Fore.BLUE}").lower()
                    if option == 'y':
                        clear()
                        while not new_code:
                            new_code = input(
                                f"{Fore.LIGHTMAGENTA_EX}Please enter a new code: {Fore.BLUE}")
                            if not new_code:
                                clear()
                                print(
                                    f"{Fore.RED}You must provide a code to be used as a reference point in the future.")
                                sleep(3)
                                clear()
                            else:
                                clear()
                                break
                        break

                    elif option == 'n':
                        clear()
                        break
                    else:
                        clear()
                        print(f"{Fore.LIGHTRED_EX}Enter either Y or N.")
                        sleep(2)
                        clear()

                while True:
                    option = input(
                        f"{Fore.LIGHTMAGENTA_EX}Do you want to change your target's discord name? [Y/N]: {Fore.BLUE}").lower()
                    if option == 'y':
                        clear()
                        while not new_name:
                            new_name = input(
                                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's discord name ({Fore.LIGHTRED_EX}do not include the "
                                f"#XXXX{Fore.LIGHTMAGENTA_EX}):")
                            if not new_name:
                                clear()
                                print(
                                    f"{Fore.LIGHTRED_EX}You must provide a name.")
                                sleep(2)
                                clear()
                            else:
                                clear()
                                break
                        break

                    elif option == 'n':
                        clear()
                        break
                    else:
                        clear()
                        print(f"{Fore.LIGHTRED_EX}Enter either Y or N.")
                        sleep(2)
                        clear()

                while True:
                    option = input(
                        f"{Fore.LIGHTMAGENTA_EX}Do you want to change your target's discord discriminator? [Y/N]: {Fore.BLUE}").lower()
                    if option == 'y':
                        clear()
                        while not new_discriminator:
                            new_discriminator = input(
                                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's discriminator ({Fore.LIGHTCYAN_EX}the four-digit "
                                f"number after the #{Fore.LIGHTMAGENTA_EX}): {Fore.BLUE}")
                            if len(new_discriminator) != 4:
                                new_discriminator = ""
                            for num in new_discriminator:
                                if num not in str_numbers:
                                    new_discriminator = ""
                                    break
                            if not new_discriminator:
                                clear()
                                print(
                                    f"{Fore.LIGHTRED_EX}You must provide a valid discriminator.")
                                sleep(2)
                                clear()
                            else:
                                clear()
                                break
                        break

                    elif option == 'n':
                        clear()
                        break
                    else:
                        clear()
                        print(f"{Fore.LIGHTRED_EX}Enter either Y or N.")
                        sleep(2)
                        clear()

                while True:
                    option = input(
                        f"{Fore.LIGHTMAGENTA_EX}Do you want to change your target's token? [Y/N]: {Fore.BLUE}").lower()
                    if option == 'y':
                        clear()
                        while True:
                            failure = False
                            new_token = input(
                                f"{Fore.LIGHTMAGENTA_EX}Please enter your target's token ({Fore.LIGHTCYAN_EX}If you do not know this, "
                                f"enter nothing{Fore.LIGHTMAGENTA_EX}): {Fore.BLUE}")
                            for char in new_token.lower():
                                if char not in valid_token_chars:
                                    failure = True
                            if len(new_token) != 59 and new_token:
                                failure = True
                            if not new_token and not failure:
                                new_token = "N/A"
                                clear()
                                break
                            elif new_token and not failure:
                                clear()
                                break
                            else:
                                clear()
                                print(
                                    f"{Fore.LIGHTRED_EX}You must provide either a valid token, or nothing if you do not know it.")
                                sleep(3)
                                clear()
                        break

                    elif option == 'n':
                        clear()
                        break
                    else:
                        clear()
                        print(f"{Fore.LIGHTRED_EX}Enter either Y or N.")
                        sleep(2)
                        clear()

                new_account = {}
                if new_code:
                    new_account["code"] = new_code
                else:
                    new_account["code"] = old_code

                if new_name:
                    new_account["name"] = new_name
                else:
                    new_account["name"] = old_name

                if new_discriminator:
                    new_account["discriminator"] = new_discriminator
                else:
                    new_account["discriminator"] = old_discriminator

                if new_token:
                    new_account["token"] = new_token
                else:
                    new_account["token"] = old_token

                del accounts[i]

                accounts.append(new_account)
                os.remove('accounts.json')
                target = {"targets": accounts}
                with open('accounts.json', 'w') as f:
                    json.dump(target, f, indent=4)
                print(
                    f"{Fore.LIGHTMAGENTA_EX}The target has been edited successfully.")
                sleep(2)
            else:
                print(
                    f"{Fore.LIGHTRED_EX}The specified target was not found in accounts.json.")
                sleep(2)
                edit_account()

    end = input(
        f"\n\n{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
    main()


# Display an account from the hitlist.

def display_account():
    clear()
    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
        print(f"{Fore.LIGHTRED_EX}accounts.json file not found{Fore.WHITE} - {Fore.LIGHTRED_EX}generated a new file!")
        sleep(3)
        main()

    code = ""
    global exit_num

    while not code:
        print(f"{Fore.LIGHTMAGENTA_EX}Please enter the reference code of your target.")
        code = input(
            f"{Fore.LIGHTMAGENTA_EX}\nAlternatively, you can type '{Fore.LIGHTCYAN_EX}_thoth-exit_{exit_num}_{Fore.LIGHTMAGENTA_EX}' to return to the main screen.\n\n"
            f"{Fore.LIGHTRED_EX}Once you proceed past this step, you will not be able to return to the main screen until "
            f"you complete this option:\n{Fore.BLUE}")
        if not code:
            clear()
            print(f"{Fore.LIGHTRED_EX}You must provide a reference code.")
            sleep(2)
            clear()
        if code == f'_thoth-exit_{exit_num}_':
            main()
        if code and code != f'_thoth-exit_{exit_num}_':
            with open('accounts.json') as f:
                data = json.load(f)
                clear()
                accounts = data['targets']
                i = -1
                found = False
                for account in accounts:
                    if account["code"] == code:
                        i += 1
                        found = True
                        break
                    else:
                        i += 1
            if found:
                code = accounts[i]["code"]
                name = accounts[i]["name"]
                discriminator = accounts[i]["discriminator"]
                token = accounts[i]["token"]
                print(f"{Fore.LIGHTMAGENTA_EX}Account \"{code}\":\n")
                print(f"{Fore.LIGHTMAGENTA_EX}Code: {Fore.BLUE}{code}")
                print(f"{Fore.LIGHTMAGENTA_EX}Name: {Fore.BLUE}{name}")
                print(
                    f"{Fore.LIGHTMAGENTA_EX}Discriminator: {Fore.BLUE}{discriminator}")
                print(f"{Fore.LIGHTMAGENTA_EX}Token: {Fore.BLUE}{token}")
            else:
                print(
                    f"{Fore.LIGHTRED_EX}The specified target was not found in accounts.json.")
                sleep(2)
                display_account()

    end = input(
        f"\n\n{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
    main()


# Check if an account is in the hitlist.

def check_account():
    clear()
    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
        print(f"{Fore.LIGHTRED_EX}accounts.json file not found{Fore.WHITE} - {Fore.LIGHTRED_EX}generated a new file!")
        sleep(3)
        main()

    code = ""
    global exit_num

    while not code:
        print(f"{Fore.LIGHTMAGENTA_EX}Please enter the reference code of your target.")
        code = input(
            f"{Fore.LIGHTMAGENTA_EX}\nAlternatively, you can type '{Fore.LIGHTCYAN_EX}_thoth-exit_{exit_num}_{Fore.LIGHTMAGENTA_EX}' to return to the main screen.\n\n"
            f"{Fore.LIGHTRED_EX}Once you proceed past this step, you will not be able to return to the main screen until "
            f"you complete this option:\n{Fore.BLUE}")
        if not code:
            clear()
            print(f"{Fore.LIGHTRED_EX}You must provide a reference code.")
            sleep(2)
            clear()
        if code == f'_thoth-exit_{exit_num}_':
            main()
        if code and code != f'_thoth-exit_{exit_num}_':
            with open('accounts.json') as f:
                data = json.load(f)
                clear()
                accounts = data['targets']
                i = -1
                found = False
                for account in accounts:
                    if account["code"] == code:
                        i += 1
                        found = True
                        break
                    else:
                        i += 1
            if found:
                print(
                    f"{Fore.LIGHTGREEN_EX}The specified target was found in accounts.json.")
                sleep(1)
            else:
                print(
                    f"{Fore.LIGHTRED_EX}The specified target was not found in accounts.json.")
                sleep(1)

    end = input(
        f"\n\n{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
    main()


# View the JSON file containing accounts in a custom JSON viewer.

def view_json():
    clear()
    if not os.path.isfile('accounts.json'):
        with open('accounts.json', 'w') as f:
            x = {"targets": []}
            json.dump(x, f, indent=4)
            f.close()
        print(f"{Fore.LIGHTRED_EX}accounts.json file not found{Fore.WHITE} - {Fore.LIGHTRED_EX}generated a new file!")
        sleep(3)
        main()

    with open('accounts.json', 'r') as f:
        data = json.load(f)
        print(f"{Fore.LIGHTMAGENTA_EX}Viewing accounts.json file.\n\n")
        test = str(json.dumps(data, indent=4, sort_keys=True))
        print(
            test.replace(
                "{",
                Fore.YELLOW +
                "{" +
                Fore.RESET).replace(
                "}",
                Fore.YELLOW +
                "}" +
                Fore.RESET).replace(
                "[",
                Fore.LIGHTMAGENTA_EX +
                "[" +
                Fore.RESET).replace(
                    "]",
                    Fore.LIGHTMAGENTA_EX +
                    "]" +
                    Fore.RESET).replace(
                        ",",
                        Fore.BLUE +
                        "," +
                        Fore.RESET).replace(
                            ":",
                            Fore.LIGHTCYAN_EX +
                            ":" +
                            Fore.RESET).replace(
                                '"',
                                Fore.LIGHTGREEN_EX +
                                '"'))

    end = input(
        f"\n\n{Fore.BLUE}Press the return key to continue. . . {Fore.WHITE}")
    main()


def getBanner():
    banner = Style.BRIGHT + f'''


                                      ████████╗██╗  ██╗ ██████╗ ████████╗██╗  ██╗
                                      ╚══██╔══╝██║  ██║██╔═══██╗╚══██╔══╝██║  ██║
                                         ██║   ███████║██║   ██║   ██║   ███████║
                                         ██║   ██╔══██║██║   ██║   ██║   ██╔══██║
                                         ██║   ██║  ██║╚██████╔╝   ██║   ██║  ██║
                                         ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝'''.replace('█', f'{Fore.WHITE}█{Fore.LIGHTMAGENTA_EX}') + f'''



{Fore.LIGHTCYAN_EX}Please choose one of the available options:

{Fore.BLUE}[1] {Fore.LIGHTMAGENTA_EX}Add an account to the list of targets.
{Fore.BLUE}[2] {Fore.LIGHTMAGENTA_EX}Remove an account from the list of targets.
{Fore.BLUE}[3] {Fore.LIGHTMAGENTA_EX}Edit an account within the list of targets.
{Fore.BLUE}[4] {Fore.LIGHTMAGENTA_EX}Display an account from the list of targets.
{Fore.BLUE}[5] {Fore.LIGHTMAGENTA_EX}Check if an account is in the list of targets.
{Fore.BLUE}[6] {Fore.LIGHTMAGENTA_EX}View the list of targets.
{Fore.BLUE}[7] {Fore.LIGHTMAGENTA_EX}Exit.

{Fore.LIGHTBLUE_EX}Thoth created by Catterall (View for full guide): https://www.github.com/Catterall/discord-raidkit{Style.RESET_ALL}
'''
    return banner


def main():
    while True:
        clear()
        print(getBanner())
        choice = str(input(
            f'{Fore.LIGHTBLUE_EX}[{Fore.LIGHTCYAN_EX}>>>{Fore.LIGHTBLUE_EX}] {Fore.MAGENTA}Choice: {Fore.BLUE}'))
        if choice == '1':
            add_account()
        elif choice == '2':
            del_account()
        elif choice == '3':
            edit_account()
        elif choice == '4':
            display_account()
        elif choice == '5':
            check_account()
        elif choice == '6':
            view_json()
        elif choice == '7':
            choice = str(input(
                f'{Fore.LIGHTBLUE_EX}[{Fore.LIGHTCYAN_EX}>>>{Fore.LIGHTBLUE_EX}] {Fore.MAGENTA}Are you sure you want to exit? (Y to confirm): {Fore.BLUE}'))
            if choice.upper() == 'Y':
                Style.RESET_ALL
                clear()
                os._exit(0)
            else:
                continue
        else:
            clear()
            continue


if __name__ == "__main__":
    search_for_updates()
    clear()
    main()

# Scripted by Catterall (https://github.com/Catterall).
# Thoth under the GNU General Public Liscense v2 (1991).
