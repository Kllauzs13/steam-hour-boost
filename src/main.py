from steam.client import SteamClient
from stdiomask import getpass
from os import system
from time import sleep

import sys
import requests as req
from steam.core.msg import MsgProto
from steam.enums.emsg import EMsg

ascii_art = """
   ____________________    __  ___                          
  / ___/_  __/ ____/   |  /  |/  /                          
  \__ \ / / / __/ / /| | / /|_/ /                           
 ___/ // / / /___/ ___ |/ /  / /                            
/____//_/_/_____/_/ _|_/_/  /_/
    __  __ ____  __  __ __     ____  ____  ____  ___________
   / / / / __ \/ / / / __ \   / __ )/ __ \/ __ \/ ___/_  __/
  / /_/ / / / / / / / /_/ /  / __  / / / / / / /\__ \ / /   
 / __  / /_/ / /_/ / _, _/  / /_/ / /_/ / /_/ /___/ // /    
/_/ /_/\____/\____/_/ |_|  /_____/\____/\____//____//_/   

github.com/flooowd

"""

client = SteamClient()

def login():
    print(ascii_art)
    user,passw = str(input('[STB] Username: ')), getpass("[STB] Password: ")
    account_login = client.login(username=user, password=passw)
    if str(account_login) == "EResult.AccountLoginDeniedNeedTwoFactor":
        system('cls')
        login_with_steam_guard(user, passw)
        main()
    elif str(account_login) == "EResult.AccountLogonDenied":
        system('cls')
        login_with_email_auth_code(user, passw)
        main()
    elif str(account_login) == "EResult.InvalidPassword":
        system('cls')
        print('[ERROR] Invalid Login or Password.')
        login()
    elif str(account_login) == "EResult.OK":
       main()
    else:
        print("[ERROR]: " + str(account_login))
        system('pause')
        sys.exit()

def login_with_email_auth_code(username, password):
    print(ascii_art)
    code = str(input('[STB] Steam Guard Code (sent to your email): '))
    account_login = client.login(username=username, password=password, auth_code=code)
    if str(account_login) == "EResult.InvalidPassword":
        system('cls')
        print('[STB] Wrong Password\n')
        login()
    elif str(account_login) == "EResult.OK":
        system('cls')
        main()
    elif str(account_login) == "EResult.InvalidLoginAuthCode":
        system('cls')
        print('[ERROR] Invalid Steam Guard Code.')
        login_with_email_auth_code(username, password)
    else:
        print("[ERROR]: " + str(account_login))
        system('pause')
        sys.exit()


def login_with_steam_guard(username, password):
    print(ascii_art)
    code = str(input('[STB] Steam Guard Code: '))
    account_login = client.login(username=username, password=password, two_factor_code=code)
    if str(account_login) == "EResult.InvalidPassword":
        system('cls')
        print('[STB] Wrong Password\n')
        login()
    elif str(account_login) == "EResult.OK":
        system('cls')
        main()
    elif str(account_login) == "EResult.TwoFactorCodeMismatch":
        system('cls')
        print('[ERROR] Invalid Steam Guard Code.')
        login_with_steam_guard(username, password)
    else:
        print("[ERROR]: " + str(account_login))
        system('pause')
        sys.exit()

def main():
    print(ascii_art)
    print(f'[STB] Logged in as {client.user.name}')
    try:
        game_id = int(input('[STB] Game ID: '))
        custom_game_name = str(input('[STB] Custom Game Name: '))
        if game_id != "":
            system('cls')
            print(ascii_art)
            get_game_name = req.get(f"https://store.steampowered.com/api/appdetails/?appids={game_id}&filters=basic").json()
            if get_game_name == "null":
                system("cls")
                print(f'[STB] {game_id} its not a valid game id.')
                main()
            elif get_game_name[str(game_id)]["success"] == False:
                system("cls")
                print(f'[STB] {game_id} its not a valid game id.')
                main()
            else:
                game_name = str(get_game_name[str(game_id)]["data"]["name"])
            client.send(MsgProto(EMsg.ClientGamesPlayed), {'games_played': [{'game_id': game_id, 'game_extra_info': custom_game_name},]})
            system(f"title Steam Hour Boost - @flooowd - Running {game_name}")
            print(f'[STB] Game: {game_name} | Status: Running | @flooowd')
            client.run_forever()
        else:
            system('cls')
            print("[STB] Game ID can't be empty.")
            main()
    except (ValueError):
        system('cls')
        print('[STB] Game ID needs to be int.')
        main()
if __name__ in "__main__":
    system("cls && color c && title Steam Hour Boost - @flooowd")
    login()
