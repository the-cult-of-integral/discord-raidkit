"""
Discord Raidkit v2.4.4
the-cult-of-integral

Last modified: 2023-04-28 00:47
"""

import colorama as cama
import shared.shared as shared
import utils.dr_repo_utils as ru

DISCORD_RAIDKIT_ASCII = """
            .#/                                                                                 
    #########*#######                                                                           
 ############## #####                         ##   #                    #                       
%#######################                      # #      ## ### ### ### ###                       
 ####################                         # #  #   #  #   # # #   # #                       
  ############                                # #  ## ##  ### ### #   ###                       
   ##########                                 ##                                                
    &#######                                                                                    
      *#####%                                 ##       #    # #    #   #                        
        &####                                 # #  ##     ### # #     ###                       
           ###                                ##  # #  #  # # ##   #   #                        
             ###                              # # ###  ## ### # #  ##  ##                       
                ##                            # #                                               
                   #                                                                            
                     #                                                                          

"""

OSIRIS_ASCII = """
:'#######:::'######::'####:'########::'####::'######::
'##.... ##:'##... ##:. ##:: ##.... ##:. ##::'##... ##:
 ##:::: ##: ##:::..::: ##:: ##:::: ##:: ##:: ##:::..::
 ##:::: ##:. ######::: ##:: ########::: ##::. ######::
 ##:::: ##::..... ##:: ##:: ##.. ##:::: ##:::..... ##:
 ##:::: ##:'##::: ##:: ##:: ##::. ##::: ##::'##::: ##:
. #######::. ######::'####: ##:::. ##:'####:. ######::
:.......::::......:::....::..:::::..::....:::......:::

Using proxies: PROXIES_ENABLED

"""


def raider_cmds(prefix: str, bot_type: shared.BotType) -> str:
    """Return a string to display when the bot is ready.
    """
    return f"""{cama.Fore.LIGHTGREEN_EX}Welcome to Discord Raidkit's raiding utility {cama.Fore.LIGHTWHITE_EX}{ru.MY_VERSION}{cama.Fore.LIGHTGREEN_EX}!

{cama.Fore.LIGHTWHITE_EX}Bot Type: {cama.Fore.LIGHTMAGENTA_EX}{bot_type}

{cama.Fore.LIGHTBLUE_EX}{prefix}nick_all <nickname> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}changes the nickname of all members in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}msg_all <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}sends a message to all members in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}spam <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}spams a message in all channels in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}cpurge {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}deletes all channels in the server.
{cama.Fore.LIGHTBLUE_EX}{prefix}cflood <amount> <name> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}creates a specified amount of channels with a specified name.
{cama.Fore.LIGHTBLUE_EX}{prefix}raid <role_name> <nickname> <amount> <name> <message> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}role and nick all users in a server, then run cflood and spam
{cama.Fore.LIGHTBLUE_EX}{prefix}admin <member> <role_name> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}give a member a new role with administrator permissions.
{cama.Fore.LIGHTBLUE_EX}{prefix}nuke {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}completely nuke a server.
{cama.Fore.LIGHTBLUE_EX}{prefix}mass_nuke {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}completely nuke all servers the bot is in.
{cama.Fore.LIGHTBLUE_EX}{prefix}leave <server_id> {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}leave a server.
{cama.Fore.LIGHTBLUE_EX}{prefix}mass_leave {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}leave all servers the bot is in.
{cama.Fore.LIGHTBLUE_EX}{prefix}close {cama.Fore.LIGHTWHITE_EX}- {cama.Fore.LIGHTYELLOW_EX}close the bot. {cama.Fore.RED}Use this over CTRL + C!

{cama.Fore.RED}Warning {cama.Fore.LIGHTWHITE_EX}: {cama.Fore.LIGHTRED_EX}make sure your bot's role is higher than the roles of those you wish to affect.

{cama.Fore.LIGHTWHITE_EX}"""
