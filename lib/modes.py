import lib.events as trigger
import lib.base as base
import time
import socket
import pickle
import threading
from pynput import keyboard

class singleplayer():
    def __init__(self):
        self.Victory = False
        self.DEAD    = False

        # STATS
        self.SCORE= 0
        self.Direction="RIGHT" # the Direction the Snake is heading to

        # PROPERTIES
        self.SnakeX_ROW    = 4
        self.SnakeY_COLUMN = 4
        self.SNAKELENGTH       = 5
        self.SNAKESPEED        = 1

        self.SNAKEHEAD=base.SNAKEHEAD
        self.SNAKETAIL=base.SNAKETAIL
        
        self.FoodDelay     = 5
        self.LastPosition  =[]
        
        self.foodAvailable = True

        self.timePast      = time.time()
        self.VictoryScore  = 50
        self.lastUpdate= 0

        self.liveMAP = [
            [base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","",base.FOOD,"",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL]
        ]

    def Move(self):
        def check4food(YCol, XRow):
            if self.liveMAP[YCol][XRow] == base.FOOD:
                #global SCORE, SNAKELENGTH
                # eat food
                self.liveMAP[YCol][XRow] = ""
                self.SCORE += 1
                self.SNAKELENGTH += 1

                self.foodAvailable = False
        
        if self.Direction == "UP":
            if self.SnakeY_COLUMN-1 <= 0 or self.liveMAP[self.SnakeY_COLUMN-1][self.SnakeX_ROW] == base.SNAKETAIL:
                self.DEAD = True
            else:
                self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                if len(self.LastPosition) > self.SNAKELENGTH:
                    self.LastPosition.pop(0)

                check4food(self.SnakeY_COLUMN-1, self.SnakeX_ROW)
                
                self.SNAKEHEAD=base.UP
                self.SnakeY_COLUMN -= 1
        elif self.Direction == "RIGHT":
            if self.SnakeX_ROW+1 >= len(base.MAP[self.SnakeY_COLUMN])-1 or self.liveMAP[self.SnakeY_COLUMN][self.SnakeX_ROW+1] == base.SNAKETAIL:
                self.DEAD = True
            else:
                self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                if len(self.LastPosition) > self.SNAKELENGTH:
                    self.LastPosition.pop(0)
                
                check4food(self.SnakeY_COLUMN, self.SnakeX_ROW+1)
                self.SNAKEHEAD=base.RIGHT
                self.SnakeX_ROW += 1 
        elif self.Direction == "LEFT":
            if self.SnakeX_ROW-1 <= 0 or self.liveMAP[self.SnakeY_COLUMN][self.SnakeX_ROW-1] == base.SNAKETAIL:
                self.DEAD = True
            else:
                self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                if len(self.LastPosition) > self.SNAKELENGTH:
                    self.LastPosition.pop(0)

                check4food(self.SnakeY_COLUMN, self.SnakeX_ROW-1)
                self.SNAKEHEAD=base.LEFT
                self.SnakeX_ROW -= 1
        elif self.Direction == "DOWN":
            if (self.SnakeY_COLUMN+1) >= len(base.MAP)-1 or self.liveMAP[self.SnakeY_COLUMN+1][self.SnakeX_ROW] == base.SNAKETAIL:
                self.DEAD = True
            else:
                self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                if len(self.LastPosition) > self.SNAKELENGTH:
                    self.LastPosition.pop(0)

                check4food(self.SnakeY_COLUMN+1, self.SnakeX_ROW)
                self.SNAKEHEAD=base.DOWN
                self.SnakeY_COLUMN += 1

    def Update(self):
        if self.lastUpdate < self.timePast:
            self.Move()
            self.lastUpdate = self.timePast + self.SNAKESPEED

        base.clearText()
        for Column in range(0,len(base.MAP)):
            rowString=" "

            for Row in range(0,len(base.MAP[Column])):
                tailPOSITION=False
                for TAIL in self.LastPosition: # Check if snake tail is in position
                    if TAIL[0] == Column and TAIL[1] == Row:
                        rowString = rowString + self.SNAKETAIL + " " 
                        self.liveMAP[Column][Row] = self.SNAKETAIL
                        tailPOSITION=True
                        break
                
                if not tailPOSITION:
                    if self.liveMAP[Column][Row] == base.FOOD: # Food is in position
                        rowString = rowString + self.liveMAP[Column][Row] + " "
                    elif Column == self.SnakeY_COLUMN and Row == self.SnakeX_ROW: # Snake Head In position
                        rowString = rowString + self.SNAKEHEAD + " "
                        self.liveMAP[Column][Row] = self.SNAKEHEAD
                    elif base.MAP[Column][Row] == "": # Empty Position
                        rowString = rowString + "  "
                        self.liveMAP[Column][Row] = ""
                    else: # Obstacle in Position
                        rowString = rowString + base.MAP[Column][Row] + " "
                        self.liveMAP[Column][Row] = base.MAP[Column][Row]

            
            print(rowString)
        
        if not self.Victory and not self.DEAD:
            print(f"Food Eaten: {self.SCORE}")
            print(f"Snake length: {self.SNAKELENGTH}")
            print(f"Snake Speed: {self.SNAKESPEED}")

    def Start(self):
        base.clearText()
        time.sleep(0.5)
        print(f"To win you must eat about {self.VictoryScore} Apples.")
        time.sleep(2)

        while True:
            if self.DEAD or self.Victory:
                break
            # Check for player inputs
            inputPressed = base.keyPressed()
            if inputPressed:
                if inputPressed == "UP" and inputPressed != self.Direction and (self.LastPosition[-1][0] != self.SnakeY_COLUMN+1 and self.LastPosition[-1][1] != self.SnakeX_ROW):
                    self.Direction = inputPressed
                elif inputPressed == "RIGHT" and inputPressed != self.Direction and (self.LastPosition[-1][0] != self.SnakeY_COLUMN and self.LastPosition[-1][1] != self.SnakeX_ROW+1):
                    self.Direction = inputPressed
                elif inputPressed == "LEFT" and inputPressed != self.Direction and (self.LastPosition[-1][0] != self.SnakeY_COLUMN and self.LastPosition[-1][1] != self.SnakeX_ROW-1):
                    self.Direction = inputPressed
                elif inputPressed == "DOWN" and inputPressed != self.Direction and (self.LastPosition[-1][0] != self.SnakeY_COLUMN-1 and self.LastPosition[-1][1] != self.SnakeX_ROW):
                    self.Direction = inputPressed

            if not self.foodAvailable:
                self.liveMAP = base.spawnFood(self.liveMAP)
                self.foodAvailable=True

            
            self.timePast = time.time()
            if self.lastUpdate < self.timePast:
                self.Update()

        if self.DEAD:
            self.SNAKEHEAD=base.SNAKEDEATH
            self.SNAKETAIL=base.SNAKEDEATH
            self.Update()
            trigger.DeathEvent()
            
        elif self.Victory:
            trigger.WinEvent()

class multiplayer():
    def __init__(self):
        self.IP = socket.gethostname()
        self.PORT = 1235

        # PLAYER 1
        self.P1VictoryScore= 10
        self.PLAYER1_SCORE = 0
        self.PLAYER1ALIVE  = True

        self.Direction     = "RIGHT" # the Direction the Snake is heading to
        self.SnakeX_ROW    = 4
        self.SnakeY_COLUMN = 4
        self.SNAKELENGTH   = 5
        self.SNAKESPEED    = 1
        self.respawnCount  = 0

        self.SNAKEHEAD     = base.SNAKEHEAD
        self.SNAKETAIL     = base.SNAKETAIL
        
        self.LastPosition  =[]

        # PLAYER 2
        self.P2VictoryScore = 100
        self.PLAYER2_SCORE = 0
        self.foodAvailable = True
        self.FoodX_ROW    = 8
        self.FoodY_COLUMN = 5

        self.foodSpawnCount=0
        self.foodMoveDelay = .1


        self.UPkeyReleased = True
        self.RIGHTkeyReleased = True
        self.LEFTkeyReleased = True
        self.DOWNkeyReleased = True

        # other stuff
        
        self.Status = []

        self.liveMAP = [
            [base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,"","","","","","","","","",base.WALL],
            [base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL,base.WALL]
        ]

        self.timePast      = time.time()
        self.FoodDelay     = 5
        self.lastUpdate    = 0

    def displayInformation(self, client):
        if not client:
            self.Status=[]
            self.Status.append("Player 1;-           |Player 2;-")
            self.Status.append(f"SCORE: {self.PLAYER1_SCORE}/{self.P1VictoryScore}            |SCORE: {self.PLAYER2_SCORE}/{self.P2VictoryScore}")
            if not self.PLAYER1ALIVE:
                self.Status.append(f"Respawning in: {self.respawnCount}")
            else:
                self.Status.append(f"Snake Length: {self.SNAKELENGTH}")
                self.Status.append(f"Snake Speed: {self.SNAKESPEED}")
    
        for str in self.Status:
            print(str)
    
    def displayMap(self):
        for Column in range(0,len(base.MAP)):
            rowString=" "

            for Row in range(0,len(base.MAP[Column])):
                tailPOSITION=False
                for TAIL in self.LastPosition: # Check if snake tail is in position
                    if TAIL[0] == Column and TAIL[1] == Row:
                        rowString = rowString + self.SNAKETAIL + " " 
                        self.liveMAP[Column][Row] = self.SNAKETAIL
                        tailPOSITION=True
                        break
                
                if not tailPOSITION:
                    if self.liveMAP[Column][Row] == base.FOOD and (Column != self.FoodY_COLUMN and Row != self.FoodX_ROW):
                        self.liveMAP[Column][Row] = ""

                    if Column == self.FoodY_COLUMN and Row == self.FoodX_ROW:
                        rowString = rowString + base.FOOD + " "
                        self.liveMAP[Column][Row] = base.FOOD
                    elif Column == self.SnakeY_COLUMN and Row == self.SnakeX_ROW: # Snake Head In position
                        rowString = rowString + self.SNAKEHEAD + " "
                        self.liveMAP[Column][Row] = self.SNAKEHEAD
                    elif base.MAP[Column][Row] == "": # Empty Position
                        rowString = rowString + "  "
                        self.liveMAP[Column][Row] = ""
                    else: # Obstacle in Position
                        rowString = rowString + base.MAP[Column][Row] + " "
                        self.liveMAP[Column][Row] = base.MAP[Column][Row]

            
            print(rowString)

    def clientEaten(self):
        resultMap, newPositions = base.spawnFood(self.liveMAP)
        self.FoodY_COLUMN = newPositions[0]
        self.FoodX_ROW = newPositions[1]
        self.PLAYER2_SCORE -= 10
        self.foodAvailable = False

    def Move(self, TYPE):
        def check4food(YCol, XRow):
            if self.liveMAP[YCol][XRow] == base.FOOD or (YCol == self.FoodY_COLUMN and XRow == self.FoodX_ROW):
                # eat food
                self.liveMAP[YCol][XRow] = ""
                self.PLAYER1_SCORE += 1
                self.SNAKELENGTH += 1

                self.foodAvailable = False
        
        if TYPE == "SNAKE":
            if self.Direction == "UP":
                if self.SnakeY_COLUMN-1 <= 0 or self.liveMAP[self.SnakeY_COLUMN-1][self.SnakeX_ROW] == base.SNAKETAIL:
                    self.PLAYER1ALIVE = False
                    self.respawnCount = 4
                    self.SNAKETAIL = base.SNAKEDEATH
                    self.SNAKEHEAD = base.SNAKEDEATH
                else:
                    self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                    if len(self.LastPosition) > self.SNAKELENGTH:
                        self.LastPosition.pop(0)

                    check4food(self.SnakeY_COLUMN-1, self.SnakeX_ROW)
                    
                    self.SNAKEHEAD=base.UP
                    self.SnakeY_COLUMN -= 1
            elif self.Direction == "RIGHT":
                if self.SnakeX_ROW+1 >= len(base.MAP[self.SnakeY_COLUMN])-1 or self.liveMAP[self.SnakeY_COLUMN][self.SnakeX_ROW+1] == base.SNAKETAIL:
                    self.PLAYER1ALIVE = False
                    self.respawnCount = 4
                    self.SNAKETAIL = base.SNAKEDEATH
                    self.SNAKEHEAD = base.SNAKEDEATH
                else:
                    self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                    if len(self.LastPosition) > self.SNAKELENGTH:
                        self.LastPosition.pop(0)
                    
                    check4food(self.SnakeY_COLUMN, self.SnakeX_ROW+1)
                    self.SNAKEHEAD=base.RIGHT
                    self.SnakeX_ROW += 1 
            elif self.Direction == "LEFT":
                if self.SnakeX_ROW-1 <= 0 or self.liveMAP[self.SnakeY_COLUMN][self.SnakeX_ROW-1] == base.SNAKETAIL:
                    self.PLAYER1ALIVE = False
                    self.respawnCount = 4
                    self.SNAKETAIL = base.SNAKEDEATH
                    self.SNAKEHEAD = base.SNAKEDEATH
                else:
                    self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                    if len(self.LastPosition) > self.SNAKELENGTH:
                        self.LastPosition.pop(0)

                    check4food(self.SnakeY_COLUMN, self.SnakeX_ROW-1)
                    self.SNAKEHEAD=base.LEFT
                    self.SnakeX_ROW -= 1
            elif self.Direction == "DOWN":
                if self.SnakeY_COLUMN+1 >= len(base.MAP)-1 or self.liveMAP[self.SnakeY_COLUMN+1][self.SnakeX_ROW] == base.SNAKETAIL:
                    self.PLAYER1ALIVE = False
                    self.respawnCount = 4
                    self.SNAKETAIL = base.SNAKEDEATH
                    self.SNAKEHEAD = base.SNAKEDEATH
                else:
                    self.LastPosition.append((self.SnakeY_COLUMN, self.SnakeX_ROW))
                    if len(self.LastPosition) > self.SNAKELENGTH:
                        self.LastPosition.pop(0)

                    check4food(self.SnakeY_COLUMN+1, self.SnakeX_ROW)
                    self.SNAKEHEAD=base.DOWN
                    self.SnakeY_COLUMN += 1
        elif TYPE == "FOOD":
            if self.Direction == "UP":
                self.Direction = None
                if self.liveMAP[self.FoodY_COLUMN-1][self.FoodX_ROW] == "":
                    self.FoodY_COLUMN -=1
                    self.PLAYER2_SCORE +=1
                elif self.liveMAP[self.FoodY_COLUMN-1][self.FoodX_ROW] == self.SNAKEHEAD:
                    self.clientEaten()
            elif self.Direction == "RIGHT":
                self.Direction = None
                if self.liveMAP[self.FoodY_COLUMN][self.FoodX_ROW+1] == "":
                    self.FoodX_ROW += 1
                    self.PLAYER2_SCORE +=1
                elif self.liveMAP[self.FoodY_COLUMN][self.FoodX_ROW+1] == self.SNAKEHEAD:
                    self.clientEaten()
            elif self.Direction == "LEFT":
                self.Direction = None
                if self.liveMAP[self.FoodY_COLUMN][self.FoodX_ROW-1] == "":
                    self.FoodX_ROW -= 1
                    self.PLAYER2_SCORE +=1
                elif self.liveMAP[self.FoodY_COLUMN+1][self.FoodX_ROW] == self.SNAKEHEAD:
                    self.clientEaten()
            elif self.Direction == "DOWN":
                self.Direction = None
                if self.liveMAP[self.FoodY_COLUMN+1][self.FoodX_ROW] == "":
                    self.FoodY_COLUMN +=1
                    self.PLAYER2_SCORE +=1
                elif self.liveMAP[self.FoodY_COLUMN+1][self.FoodX_ROW] == self.SNAKEHEAD:
                    self.clientEaten()

    def snakeinputCheck(self):
        def on_press(key):
            if str(key) == "Key.up" and self.UPkeyReleased and self.Direction != "DOWN":
                self.Direction = "UP"
                self.UPkeyReleased = False
            elif str(key) == "Key.right" and self.RIGHTkeyReleased and self.Direction != "LEFT":
                self.Direction = "RIGHT"
                self.RIGHTkeyReleased = False
            elif str(key) == "Key.left" and self.LEFTkeyReleased and self.Direction != "RIGHT":
                self.Direction = "LEFT"
                self.LEFTkeyReleased = False
            elif str(key) == "Key.down" and self.DOWNkeyReleased and self.Direction != "UP":
                self.Direction = "DOWN"
                self.DOWNkeyReleased = False

        def on_release(key):
            if str(key) == "Key.up" and not self.UPkeyReleased:
                self.UPkeyReleased = True
            elif str(key) == "Key.right" and not self.RIGHTkeyReleased:
                self.RIGHTkeyReleased = True
            elif str(key) == "Key.left" and not self.LEFTkeyReleased:
                self.LEFTkeyReleased = True
            elif str(key) == "Key.down" and not self.DOWNkeyReleased:
                self.DOWNkeyReleased = True

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()

    def Update(self, client):
        base.clearText()
        self.displayInformation(client)

        if client==False:
            if self.PLAYER1ALIVE:
                if self.lastUpdate < self.timePast:
                    self.Move("SNAKE")
                    self.lastUpdate = self.timePast + self.SNAKESPEED
        elif client==True:
            if self.foodAvailable:
                self.Move("FOOD")
        
        self.displayMap()

    def Host(self): # Host Server
        base.clearText()
        Player2 ="AWAITING CONNECTION..."
        LOBBY = [
            "| PLAYER 1 : HOST",
            f"| PLAYER 2 : {Player2}"
        ]
        for str in LOBBY:
            print(str)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.PORT))
        s.listen(5)
    
        clientsocket, address = s.accept()
        base.clearText()
        print(f"Connection from {address} has been established!")
        Player2 = "CONNECTED."
        for str in LOBBY:
            print(str)
        
        self.Over = False
        print("Match will begin shortly..")
        self.ClientData = []
        def receive_Data():
            while True:
                if self.Over == True:
                    break
                try:
                    foodPosition = clientsocket.recv(1024)
                    if not len(foodPosition):
                        return None

                    self.liveMAP[self.FoodY_COLUMN][self.FoodX_ROW] = ""
                    foodPosition = b'' + foodPosition
                    foodPositionDecrypted = pickle.loads(foodPosition[10:])
                    self.ClientData = foodPositionDecrypted
                except Exception as e:
                    pass

        clientDataThread = threading.Thread(target=receive_Data, args=())
        inputCheck = threading.Thread(target=self.snakeinputCheck, args=())

        # Run another thread to check for input.
        inputCheck.start()

        # Receive Client Data (Position, score, etc)
        clientDataThread.start()
        while True:
            try:
                if len(self.ClientData) > 0:
                    self.FoodY_COLUMN = self.ClientData[0]
                    self.FoodX_ROW = self.ClientData[1]
                    self.PLAYER2_SCORE = self.ClientData[3]
                    if self.ClientData[2] == False: # Was player accidently eaten?
                        self.PLAYER1_SCORE += 1
                        self.SNAKELENGTH += 1

                    self.liveMAP[self.FoodY_COLUMN][self.FoodX_ROW] = base.FOOD
                    
                
                self.timePast = time.time()

                if self.lastUpdate < self.timePast:
                    if not self.PLAYER1ALIVE:
                        if self.respawnCount > 0:
                            self.respawnCount -= 1
                            self.lastUpdate = self.timePast + 1
                        else:
                            self.PLAYER1ALIVE  = True
                            self.SnakeX_ROW    = 4
                            self.SnakeY_COLUMN = 4
                            self.LastPosition  = []
                            self.SNAKEHEAD     = base.SNAKEHEAD
                            self.SNAKETAIL     = base.SNAKETAIL
                    
                    self.Update(False)

                    # Send Data to client
                    DATA = {
                        "currentSnakeHead_Position": (self.SnakeY_COLUMN, self.SnakeX_ROW),
                        "TailPositions": self.LastPosition,
                        "SnakeHead": self.SNAKEHEAD,
                        "SnakeSpeed": self.SNAKESPEED,
                        "InformationToDisplay": self.Status,
                        "SNAKEALIVE": self.PLAYER1ALIVE,
                        "PLAYER2ALIVE": self.foodAvailable,
                        "PLAYER2SCORE": self.PLAYER2_SCORE,
                        "PLAYER1SCORE": self.PLAYER1_SCORE,
                        "P1VictoryScore": self.P1VictoryScore,
                        "P2VictoryScore": self.P2VictoryScore}

                    stringData = pickle.dumps(DATA)
                    stringData = bytes(f'{len(stringData):<10}', "UTF-8") +stringData
                    clientsocket.send(stringData)
                    self.foodAvailable=True

                    if self.PLAYER2_SCORE >= self.P2VictoryScore:
                        break
                    elif self.PLAYER1_SCORE >= self.P1VictoryScore:
                        break
                elif len(self.ClientData) > 0:
                    self.Update(None)
                self.ClientData=[]


            except Exception as e:
                if not (self.PLAYER2_SCORE >= self.P2VictoryScore ) or not (self.PLAYER1_SCORE >= self.P1VictoryScore):
                    print(f"Lost Connection to Player2({address})... ERROR MESSAGE: ", e)
                    clientsocket.close()
                
                break
        
        if self.PLAYER2_SCORE >= self.P2VictoryScore:
            print(".")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print("...")
            time.sleep(1)
            print("Player2 has won.")
            time.sleep(2)
        elif self.PLAYER1_SCORE >= self.P1VictoryScore:
            print(".")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print("...")
            time.sleep(1)
            print("You won.")
            time.sleep(2)

        self.Over = True
        clientDataThread = None
        inputCheck=None
        clientsocket.close()
    
    def Connect(self): # Client
        Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Server.connect((self.IP, self.PORT))
        print("Server found!")

        LOBBY = [
            "| PLAYER 1 : HOST",
            "| PLAYER 2 : >YOU<"
        ]
        for stri in LOBBY:
            print(stri)
        
        print("Match will begin shortly..")
        self.Over = False
        self.Direction = None
        def newInputDetection():
            def on_press(key):
                if str(key) == "Key.up" and self.UPkeyReleased:
                    self.Direction = "UP"
                    self.UPkeyReleased = False
                elif str(key) == "Key.right" and self.RIGHTkeyReleased:
                    self.Direction = "RIGHT"
                    self.RIGHTkeyReleased = False
                elif str(key) == "Key.left" and self.LEFTkeyReleased:
                    self.Direction = "LEFT"
                    self.LEFTkeyReleased = False
                elif str(key) == "Key.down" and self.DOWNkeyReleased:
                    self.Direction = "DOWN"
                    self.DOWNkeyReleased = False

            def on_release(key):
                if str(key) == "Key.up" and not self.UPkeyReleased:
                    self.UPkeyReleased = True
                elif str(key) == "Key.right" and not self.RIGHTkeyReleased:
                    self.RIGHTkeyReleased = True
                elif str(key) == "Key.left" and not self.LEFTkeyReleased:
                    self.LEFTkeyReleased = True
                elif str(key) == "Key.down" and not self.DOWNkeyReleased:
                    self.DOWNkeyReleased = True

            # Collect events until released
            with keyboard.Listener(
                    on_press=on_press,
                    on_release=on_release) as listener:
                listener.join()

        def send_Data():
            foodPositionData = pickle.dumps((
                self.FoodY_COLUMN, self.FoodX_ROW, 
                self.foodAvailable, self.PLAYER2_SCORE))
            foodPositionData = bytes(f'{len(foodPositionData):<10}', "UTF-8") + foodPositionData
            Server.send(foodPositionData)
            self.foodAvailable=True

        self.decryptedData=[]
        def receive_Data():
            while not self.Over:
                try:
                    receivedData=Server.recv(1024)
                    SERVERDATA = b'' + receivedData
                    self.decryptedData= pickle.loads(SERVERDATA[10:])
                except Exception as e:
                    pass


        receivingThread = threading.Thread(target=receive_Data, args=())
        inputCheck = threading.Thread(target=newInputDetection, args=())

        # Run another thread to check for input.
        inputCheck.start()

        # Run another thread to check if the server sent any Data.
        receivingThread.start()

        self.Update(True)

        self.lastFoodPositionY = self.FoodY_COLUMN
        self.lastFoodPositionX = self.FoodX_ROW
        self.lastPlayerScore = self.PLAYER2_SCORE

        while True:
            try:
                self.timePast = time.time()

                # Send Player 2 Position to Server
                #if self.lastFoodPositionX != self.FoodX_ROW or self.lastFoodPositionY != self.FoodY_COLUMN or self.lastPlayerScore != self.PLAYER2_SCORE:
                send_Data()
                self.lastFoodPositionY = self.FoodY_COLUMN
                self.lastFoodPositionX = self.FoodX_ROW
                self.lastPlayerScore = self.PLAYER2_SCORE

                if len(self.decryptedData) > 0:
                    self.SnakeY_COLUMN = self.decryptedData["currentSnakeHead_Position"][0]
                    self.SnakeX_ROW = self.decryptedData["currentSnakeHead_Position"][1]
                    self.LastPosition = self.decryptedData["TailPositions"]
                    self.SNAKEHEAD = self.decryptedData["SnakeHead"]
                    self.SNAKESPEED = self.decryptedData["SnakeSpeed"]
                    self.Status = self.decryptedData["InformationToDisplay"]
                    self.PLAYER1ALIVE = self.decryptedData["SNAKEALIVE"]
                    self.PLAYER1_SCORE= self.decryptedData["PLAYER1SCORE"]
                    self.P1VictoryScore = self.decryptedData["P1VictoryScore"]
                    self.P2VictoryScore = self.decryptedData["P2VictoryScore"]

                    
                    if not self.PLAYER1ALIVE:
                        self.SNAKETAIL = base.SNAKEDEATH
                    else:
                        self.SNAKETAIL = base.SNAKETAIL


                    if self.decryptedData["PLAYER2ALIVE"] == False:
                        self.clientEaten()

                    self.Update(True)

                    if self.PLAYER1_SCORE >= self.P1VictoryScore:
                        break
                    elif self.decryptedData["PLAYER2SCORE"] >= self.P2VictoryScore:
                        break
                    self.decryptedData=[]
                elif self.Direction:
                    self.Update(True)

            except Exception as e:
                if (self.PLAYER2_SCORE < self.P2VictoryScore ) or (self.PLAYER1_SCORE < self.P1VictoryScore):
                    print(f"Lost Connection to Host... ERROR MESSAGE: ", e)
                break
        Server.close()
        self.Over = True
        receivingThread=None
        inputCheck=None

        if self.PLAYER2_SCORE >= self.P2VictoryScore:
            print(".")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print("...")
            time.sleep(1)
            print("You won.")
            time.sleep(2)
        elif self.PLAYER1_SCORE >= self.P1VictoryScore:
            print(".")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print("...")
            time.sleep(1)
            print("Player1 has won.") 
            time.sleep(2)

    
        

            
                










