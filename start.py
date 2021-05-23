import lib.modes as m
from lib.base import clearText as ct
from time import sleep

if __name__ == "__main__":
    while True:
        print("1: SINGLEPLAYER")
        print("2: MULTIPLAYER")
        print("")
        Selected = input("Select: ")

        if Selected == "1": # SINGLE PLAYER
            sp = m.singleplayer()
            sp.Start()
            ct()
        elif Selected == "2": # MULTI PLAYER 
            ct()
            while True:
                print("1: HOST")
                print("2: CONNECT")
                print("3: BACK")
                print("")
                Selected = input("Select: ")
                if Selected == "1":
                    multiplayer = m.multiplayer()
                    
                    try:
                        ip= input(f"enter IP: ")
                        print(f"IP set to: {ip}")
                        port = int(input(f"enter a PORT: "))
                        print(f"PORT set to: {port}")
                    
                        multiplayer.IP = bytes(ip, "UTF-8")
                        multiplayer.PORT=port

                        multiplayer.Host()
                    except Exception as e:
                        print('ERROR: ', e)
                        sleep(1)
                        multiplayer = m.multiplayer()
                        print(f'IP was set to: {multiplayer.IP}')
                        print(f'PORT was set to: {multiplayer.PORT}')
                        sleep(1)
                        multiplayer.Host()

                elif Selected == "2":
                    multiplayer = m.multiplayer()

                    try:
                        ip= input(f"enter IP: ")
                        print(f"IP set to: {ip}")
                        port = int(input(f"enter a PORT: "))
                        print(f"PORT set to: {port}")
                    
                        multiplayer.IP = bytes(ip, "UTF-8")
                        multiplayer.PORT=port

                        multiplayer.Connect()
                    except Exception as e:
                        print("Error, There was a problem.", e)
                elif Selected == "3":
                    ct()
                    break
                else:
                    print("?")
        else:
            print("?")
            ct()

            


        
