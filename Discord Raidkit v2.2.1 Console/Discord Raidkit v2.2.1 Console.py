"""
Discord Raidkit v2.2.1 by the-cult-of-integral
"The trojan horse of discord raiding"
Last updated: 16/06/2022
"""

import asyncio
from utils.dr_c_utils import *


async def main() -> None:
    
    while True:
        clear()
        show_dr_options()
        choice = input()

        if choice == "1":
            clear()
            show_config()
            pause()

        elif choice == "2":
            clear()
            bot_token = get_config("bot token")
            write_config("bot_token", bot_token)
            pause()
        
        elif choice == "3":
            clear()
            bot_prefix = get_config("bot prefix")
            write_config("bot_prefix", bot_prefix)
            pause()

        elif choice == "4":
            clear()
            auth_token = get_config("auth token")
            write_config("auth_token", auth_token)
            pause()

        elif choice == "5":
            clear()
            dr_config = init_config()
            result = await run_dr_client("Anubis", dr_config)
            print(f"\n{result}\n\n")
            pause()
        
        elif choice == "6":
            clear()
            dr_config = init_config()
            result = await run_dr_client("Qetesh", dr_config)
            print(f"\n{result}\n\n")
            pause()

        elif choice == "7":
            clear()
            dr_config = init_config()
            run_osiris(dr_config["auth_token"])

        elif choice == "8":
            clear()
            view_dr_github("README")
        
        elif choice == "9":
            clear()
            view_dr_github("Wiki")
        
        elif choice == "10":
            clear()
            view_dr_github("Issues")
        
        elif choice == "11":
            clear()
            view_dr_github("License")

        elif choice == "12":
            clear()
            break

    return


if __name__ == "__main__":
    init_config()
    check_update()
    pause()
    loop = asyncio.get_event_loop().run_until_complete(main())
