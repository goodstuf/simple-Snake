import time
import lib.base as b

def DeathEvent():
    time.sleep(2)
    print("The snake has died.")
    time.sleep(5)
    print("Player 1 lost.")
    time.sleep(5)

def WinEvent():
    global SNAKEHEAD
    SNAKEHEAD = "B"
    b.Update()
    time.sleep(3)
    print("The snake has went into hibernation..")
    time.sleep(5)
    print("Player 1 Has won...")
    time.sleep(5)