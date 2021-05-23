# MODULES
import os, random, keyboard
from pynput.keyboard import Key, Listener

# SYMBOLS
UP    = "^"
LEFT  = "<"
RIGHT = ">"
DOWN  = "v"

WALL      = "❐"
SNAKEHEAD = RIGHT
SNAKETAIL = "L"
SNAKEDEATH= "#"

FOOD = "A"

MAP = [ # template map
    [WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,"","","","","","","","","",WALL],
    [WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL,WALL]
]



def clearText():
    os.system("cls")

def spawnFood(liveMAP):
    openPositions = []
    
    # Get empty positions
    for Column in range(0,len(liveMAP)):
        for Row in range(0,len(liveMAP[Column])):
            if liveMAP[Column][Row] == "":
                openPositions.append((Column, Row))

    # Select a random Position
    FoodPosition = openPositions[random.randint(0, len(openPositions)-1)]

    # Spawn food
    liveMAP[FoodPosition[0]][FoodPosition[1]] = FOOD

    return liveMAP, FoodPosition


def KeyCheck():
    def on_press(key):
        if key == "Key.up":
            return "UP"
        elif key == "Key.right":
            return "RIGHT"
        elif key == "Key.left":
            return "LEFT"
        elif key == "Key.down":
            return "DOWN"

    def on_release(key):
        if key == "Key.up":
            return "UP_r"
        elif key == "Key.right":
            return "RIGHT_r"
        elif key == "Key.left":
            return "LEFT_r"
        elif key == "Key.down":
            return "DOWN_r"

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join() 

def keyPressed():
    try:
        if keyboard.is_pressed('up'):
            return "UP"
        elif keyboard.is_pressed('right'): 
            return "RIGHT"
        elif keyboard.is_pressed('left'):  
            return "LEFT"
        elif keyboard.is_pressed('down'): 
            return "DOWN"
    except:
        return None

