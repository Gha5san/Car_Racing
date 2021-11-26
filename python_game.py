from tkinter import *
from random import randint, choice, shuffle
from time import sleep, time

gameLevels = {
    1: {"score":25,
        "speed":5,
        "maxVehicles":3,
        "miniVehicles":0,
        "maxPeriod":6,
        "miniPeriod":3},
    2: {"score":75,
        "speed":10,
        "maxVehicles":4,
        "miniVehicles":1,
        "maxPeriod":5,
        "miniPeriod":3},
    3: {"score":150,
        "speed":15,
        "maxVehicles":5,
        "miniVehicles":2,
        "maxPeriod":4,
        "miniPeriod":2},
    4: {"score":250,
        "speed":20,
        "maxVehicles":6,
        "miniVehicles":3,
        "maxPeriod":3,
        "miniPeriod":2},
    5: {"score":375,
        "speed":25,
        "maxVehicles":7,
        "miniVehicles":4,
        "maxPeriod":2,
        "miniPeriod":1},
    6: {"score":550,
        "speed":30,
        "maxVehicles":7,
        "miniVehicles":6,
        "maxPeriod":1,
        "miniPeriod":1}}

cheatIsOn     = True
firstCall     = True
pauseState    = False
livesMode     = False
bossMode      = False
isLoad        = False

vehicleOption = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']
windowWidth   = 800
windowHeight  = 700
vehicleWidth  = 55
vehicleHeight = 128

playerLives        = 5
vehicleNumbers     = 0
startingPoint      = [360, 650]
defualtSpeed       = gameLevels[1]["speed"]
playerDefualtSpeed = 2

score             = 0
maxVehicleNumber  = gameLevels[1]["maxVehicles"]
miniVehicleNumber = gameLevels[1]["miniVehicles"]
period            = 5
maxPeriod         = gameLevels[1]["maxPeriod"]
miniPeriod        = gameLevels[1]["miniPeriod"]



window = Tk()
myCanvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
myCanvas.pack()
for i in range(100, windowWidth - 99, 75):
    myCanvas.create_line(i, 0, i, windowHeight, dash=(10, 3))

livesText = myCanvas.create_text(10, 10,
                                 text='Lives: ' + str(playerLives),
                                 font=('Aerial', 15), anchor='nw')
scoreText = myCanvas.create_text(100, 10,
                                 text='Score: 0', font=('Aerial', 15),
                                 anchor='nw')
speedText = myCanvas.create_text(750, 10,
                                 text=f'Speed: {playerDefualtSpeed} mph',
                                 font=('Aerial', 15), anchor='ne')

class Vehicle():

    def __init__(self, x, y, vehicleType, vehicleTag, player=""):
        self.x     = x
        self.y     = y
        if player: self.speed = 10 + defualtSpeed
        else: self.speed = randint(defualtSpeed - 2, defualtSpeed + 5)
        self.dir   = ""
        self.tag = vehicleTag
        self.image = PhotoImage(file=f"images/" + player + vehicleType + ".png")
        self.draw  = myCanvas.create_image(self.x, self.y,
                                           image=self.image, tag=self.tag)
        self.state = "Exist"
        self.width = vehicleWidth
        self.height= vehicleHeight

    def position_update(self):
        pos = self.get_position()
        if pos[1] < 25 or pos[1] > 675 or pos[0] < 125 or pos[0] > 675:
            pause("Pause")
        else:
            if self.dir == "up":
                myCanvas.move(self.draw, 0, -self.speed - defualtSpeed)
            elif self.dir == "down":
                myCanvas.move(self.draw, 0, self.speed + defualtSpeed) #edit the speed
            elif self.dir == "left":
                myCanvas.move(self.draw, -75, 0)
            elif self.dir == "right":
                myCanvas.move(self.draw, 75, 0)
        self.dir = ""

    def get_position(self):
        pos = myCanvas.coords(self.draw)
        if pos == []:
            pos =[0, 900]
        pos = pos + [pos[0] + self.width, pos[1] + self.height]
        return pos

    def dir_up(self, event):
        self.dir = "up"
    def dir_down(self, event):
        self.dir = "down"
    def dir_left(self, event):
        self.dir = "left"
    def dir_right(self, event):
        self.dir = "right"


vehicleOpposite = []
def create_vehicle():
    global vehicleNumbers
    vehicleNumbers = int(randint(miniVehicleNumber, maxVehicleNumber))
    lanes = [135, 210, 285, 360, 435, 510, 585, 660]
    shuffle(lanes)
    for i in range(vehicleNumbers):
        vehicleOpposite.append(Vehicle(lanes[i], -50, choice(vehicleOption), "bots"))

def delete_vehicle(all):
    global period, miniPeriod, maxPeriod
    period = randint(miniPeriod, maxPeriod)
    if all:
        for i in vehicleOpposite:
            i.state = "Deleted"
            myCanvas.delete(i.draw)
            del i
    else:
        for i in vehicleOpposite:
            if i.state == "Deleted":
                myCanvas.delete(i.draw)
                del i

def collision(pos, pos2):
    if pos[0] < pos2[2] and pos[1] < pos2[3] and pos[2] > pos2[0] and pos[3] > pos2[1]:
        return True
    else:
        return False

def customise():
    pass

def player_increase_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed += 2
    myCanvas.itemconfig(speedText,
                        text=f'Speed: {playerDefualtSpeed} mph')

def player_decrease_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed -= 2
    myCanvas.itemconfig(speedText,
                        text=f'Speed: {playerDefualtSpeed} mph')

def cheat_mode_on(event):
    global cheatIsOn
    cheatIsOn = True
def cheat_mode_off(event):
    global cheatIsOn
    cheatIsOn = False

def boss_key(event):
    global bossImage

    def remove_fullscreen():
        bossWindow.destroy()
        myCanvas.bind_all('<Return>', boss_key)
        window.deiconify()

    pause("Pause")
    window.withdraw()
    bossWindow = Toplevel(window)
    bossWindow.title("TradingView")
    bossWindow.iconbitmap('Capture.png')
    bossImage = PhotoImage(file="Capture.PNG")
    labelImage = Label(bossWindow, image=bossImage)
    labelImage.pack()
    myCanvas.unbind('<Return>')
    bossWindow.protocol("WM_DELETE_WINDOW", remove_fullscreen)

def delete_home_buttons():
    myCanvas.delete(startButtonWindow)
    myCanvas.delete(loadButtonWindow)
    myCanvas.delete(leaderBoardButtonWindow)
    myCanvas.delete(customiseButtonWindow)
    myCanvas.delete(quitButtonWindow)
    myCanvas.delete(vehicleButtonWindow)

def vehicle_appearance():
    global chosenVehicle, vehicleChoice, vehicleButtonWindow, selectVehicle
    chosenVehicle = choice(vehicleOption)
    vehicleChoice = PhotoImage(file="images/player/" + chosenVehicle + ".png")
    vehicleButton = Button(window, image=vehicleChoice, borderwidth=0,
                           bg="#857d7a", activebackground="#857d7a",
                           command=change_vehicle)
    vehicleButtonWindow = myCanvas.create_window(336, 590, anchor=NW, window=vehicleButton)
    selectVehicle = myCanvas.create_text(370, 580,
                                         text='Click to switch vehicle: ',
                                         font=('Aerial', 15), fill="#290B15")


def change_vehicle():
    global  chosenVehicle, vehicleChoice, vehicleButton, vehicleButtonWindow
    vehicleIndex = vehicleOption.index(chosenVehicle)
    if vehicleIndex == 8:
        vehicleIndex = - vehicleIndex
    chosenVehicle = vehicleOption[vehicleIndex + 1]
    vehicleChoice = PhotoImage(file="images/player/" + chosenVehicle + ".png")
    myCanvas.delete(vehicleButtonWindow)
    vehicleButton = Button(window, image=vehicleChoice,
                           borderwidth=0, bg="#857d7a",
                           command=change_vehicle, activebackground="#857d7a")
    vehicleButtonWindow = myCanvas.create_window(336, 590, anchor=NW, window=vehicleButton)
    # if selectVehicle in myCanvas.find_all(): myCanvas.delete(selectVehicle)
    myCanvas.itemconfig(selectVehicle, text=chosenVehicle)


def save_leader_board():
    global nameWindow, nameprompt

    def add_score():
        if nameEntry.get():
            userName = nameEntry.get()
        else:
            userName = "Anonymous"
        with open("leaderboard.txt", "a") as f:
            f.writelines(userName + "\n")
            f.writelines(str(round(score, 2)) + "\n")
            f.writelines(str(playerLives) + "\n")
        nameWindow.destroy()

    nameWindow = Toplevel(window)
    nameWindow.title("Enter your name:")

    nameEntry = Entry(nameWindow, width=50)
    nameEntry.pack()
    namebutton = Button(nameWindow, text="Save score to leaderboard",
                        command=add_score)
    namebutton.pack()

def leader_board():

    def board_to_home():
        myCanvas.delete("leaderboard")
        myCanvas.delete(homeButton2Window)
        home(True)
    myCanvas.delete(selectVehicle)
    delete_home_buttons()
    playersData = {}
    with open("leaderboard.txt") as f:
        data = f.readlines()
        offset = 0
        for i in range(int(len(data)/3)):
            name  = data[i + offset].strip()
            score = data[i + offset + 1].strip()
            playersData[name] = float(score)
            offset += 2

        playersData = {v:k for k, v in playersData.items()}
        playersData = [(v, k) for k, v in sorted(playersData.items(), reverse=True)]
        if len(playersData) >= 5: iterations = 5
        else: iterations = len(playersData)

        for i in range(iterations):
            myCanvas.create_text(350, i*100 + 50, text=f"{i+1}.{playersData[i][0]}:      {playersData[i][1]}",
                                 font=("Aerial", 20), tag="leaderboard")

        homeButton2 = Button(window, text="Home",
                             font=("Aerial", 40), borderwidth=0, bg="#857d7a",
                             activebackground="#857d7a", command=board_to_home)
        homeButton2Window = myCanvas.create_window(380, 600, window=homeButton2)

def load():
    global counter, playerLives, chosenVehicle, isLoad
    try:
        with open("save.txt") as f:
            data = f.readlines()
            counter = int(data[0])
            playerLives = int(data[2])
            chosenVehicle = data[3]
            isLoad = True
            intiating()

    except FileNotFoundError:
        print("file don't exist")


def save():
    with open("save.txt", "w") as f:
        f.writelines(str(counter) + "\n")
        f.writelines(str(round(score, 2)) + "\n")
        f.writelines(str(playerLives) + "\n")
        f.writelines(chosenVehicle)
        # quit()

def pause(textOutput, restart=False):
    global pauseState, pauseText, resumeText, livesMode, restartButtonWindow, saveButtonWindow, \
           homeButtonWindow
    if pauseState:
        myCanvas.delete(pauseText)
        myCanvas.delete(resumeText)
        pauseState = False
        pausePosition = playerVehicle.get_position()
        myCanvas.delete(playerVehicle.draw)
        if not livesMode:
            if pausePosition[0] <= 115:
                playerVehicle.draw = myCanvas.create_image(pausePosition[0] + 75,
                                                           pausePosition[1],
                                                           image=playerVehicle.image,
                                                           tag=playerVehicle.tag)
                # myCanvas.move(playerVehicle, 75, 0)
            elif pausePosition[0] >= 735:
                playerVehicle.draw = myCanvas.create_image(pausePosition[0] - 75,
                                                           pausePosition[1],
                                                           image=playerVehicle.image,
                                                           tag=playerVehicle.tag)

            else:
                playerVehicle.draw = myCanvas.create_image(pausePosition[0],
                                                           pausePosition[1],
                                                           image=playerVehicle.image,
                                                           tag=playerVehicle.tag)


        else:
            if not restart:
                playerVehicle.draw = myCanvas.create_image(startingPoint[0],
                                                           startingPoint[1],
                                                           image=playerVehicle.image,
                                                           tag=playerVehicle.tag)

            livesMode = False
            delete_vehicle(True)


        myCanvas.delete(restartButtonWindow)
        myCanvas.delete(saveButtonWindow)
        myCanvas.delete(homeButtonWindow)
        main_code()
    else:
        if textOutput.startswith("Y"):
            livesMode = True

        pauseText = myCanvas.create_text(380, 450,
                                         text=textOutput,
                                         font=("Aerial", 30), fill="red")
        resumeText = myCanvas.create_text(380, 550,
                                          text="Click space to resume",
                                          font=("Aerial", 20), fill="red")

        restartButton = Button(window, text="Restart", font=("Aerial", 40),
                               borderwidth=0, bg="#857d7a",
                               activebackground="#857d7a",
                               command=lambda:intiating(True))
        restartButtonWindow = myCanvas.create_window(380, 100, window=restartButton)

        saveButton = Button(window, text="Save", font=("Aerial", 40),
                            borderwidth=0, bg="#857d7a",
                            activebackground="#857d7a",
                            command= save)
        saveButtonWindow = myCanvas.create_window(380, 200, window=saveButton)

        homeButton = Button(window, text="Home", font=("Aerial", 40),
                            borderwidth=0, bg="#857d7a",
                            activebackground="#857d7a",
                            command=lambda: home(False))
        homeButtonWindow = myCanvas.create_window(380, 300, window=homeButton)

        pauseState = True


def home(firstCall):
    global startButtonWindow, loadButtonWindow,leaderBoardButtonWindow, customiseButtonWindow, \
           quitButtonWindow, restartButtonWindow, saveButtonWindow, \
           homeButtonWindow, playerVehicle, pauseText, resumeText

    if not firstCall:
        delete_vehicle(True)
        myCanvas.delete(pauseText)
        myCanvas.delete(resumeText)
        myCanvas.delete(playerVehicle.draw)
        myCanvas.delete(restartButtonWindow)
        myCanvas.delete(saveButtonWindow)
        myCanvas.delete(homeButtonWindow)
        save_leader_board()



    vehicle_appearance()

    startButton = Button(window, text="Start", font=("Aerial", 40),
                         borderwidth=0, bg="#857d7a",
                         activebackground="#857d7a",
                         command=intiating)
    startButtonWindow = myCanvas.create_window(380, 100, window=startButton)

    loadButton = Button(window, text="Load Game", font=("Aerial", 40),
                        borderwidth=0, bg="#857d7a",
                        activebackground="#857d7a",
                        command=load)
    loadButtonWindow = myCanvas.create_window(380, 200, window=loadButton)

    leaderBoardButton = Button(window, text="Leader Board", font=("Aerial", 40),
                               borderwidth=0, bg="#857d7a",
                               activebackground="#857d7a",
                               command=leader_board)
    leaderBoardButtonWindow = myCanvas.create_window(380, 300, window=leaderBoardButton)

    customiseButton = Button(window, text="Customise", font=("Aerial", 40),
                             borderwidth=0, bg="#857d7a",
                             activebackground="#857d7a",
                             command=customise)
    customiseButtonWindow = myCanvas.create_window(380, 400, window=customiseButton)

    quitButton = Button(window, text="Quit", font=("Aerial", 40),
                        borderwidth=0, bg="#857d7a",
                        activebackground="#857d7a",
                        command=quit)
    quitButtonWindow = myCanvas.create_window(380, 500, window=quitButton)


def intiating(restart=False):
    global playerVehicle, startTime, livesMode, playerLives, timeStamps, \
    unusedTime, totatUnusedTime, counter, score, scoreOffset, isLoad
    if not restart:
        delete_home_buttons()
    else:
        playerLives = 5
        pause("Pause", True)

    myCanvas.itemconfig(livesText, text='Lives: ' + str(playerLives))
    if selectVehicle in myCanvas.find_all(): myCanvas.delete(selectVehicle)

    playerVehicle = Vehicle(startingPoint[0], startingPoint[1], chosenVehicle, "player", "player/")
    myCanvas.bind_all('<Up>', playerVehicle.dir_up)
    myCanvas.bind_all('<Down>', playerVehicle.dir_down)
    myCanvas.bind_all('<Left>', playerVehicle.dir_left)
    myCanvas.bind_all('<Right>', playerVehicle.dir_right)
    myCanvas.bind_all('<a>', player_decrease_speed)
    myCanvas.bind_all('<d>', player_increase_speed)
    myCanvas.bind_all('<space>', lambda x: pause("Pause"))
    myCanvas.bind_all('<KeyPress-c>',   cheat_mode_on)
    myCanvas.bind_all('<KeyRelease-c>', cheat_mode_off)
    myCanvas.bind_all('<Return>', boss_key)

    if not isLoad:
        counter = 1
        startTime = time()
    else:
        scoreOffset = 0
        startTime = time() - (counter - 1) * 50
        isLoad = False

    score = 0
    timeStamps = []
    unusedTime = 0
    totatUnusedTime = 0
    main_code()

def main_code():
    global pauseState, playerLives, scoreText, unusedTime, totatUnusedTime, score, \
           counter, defualtSpeed, maxVehicleNumber, miniVehicleNumber, maxPeriod, miniPeriod, \
           period, elapsedTime, scoreOffset

    defualtSpeed = gameLevels[counter]["speed"]
    maxVehicleNumber = gameLevels[counter]["maxVehicles"]
    miniVehicleNumber = gameLevels[counter]["miniVehicles"]
    maxPeriod = gameLevels[counter]["maxPeriod"]
    miniPeriod = gameLevels[counter]["miniPeriod"]
    scoreOffset = 50*(counter-1)

    while (not pauseState and score<=gameLevels[counter]["score"]):
        if unusedTime != 0:
            unusedTime = time() - unusedTime
            totatUnusedTime += unusedTime
        elapsedTime = time() - (startTime + totatUnusedTime)

        if counter > 1:
            score = round((((elapsedTime - scoreOffset) * defualtSpeed) / 10), 2)
            score += gameLevels[counter - 1]["score"]
        else:  score = round((elapsedTime * defualtSpeed) / 10, 2)

        myCanvas.itemconfig(scoreText, text=f'Score: {round(score, 2)}')
        # pause("Pause")
        elapsedTime = int(elapsedTime)
        # print(elapsedTime)
        # print(elapsedTime)
        # period = randint(miniPeriod, maxPeriod)
        if elapsedTime % period == 0 and elapsedTime not in timeStamps:
            timeStamps.append(elapsedTime)
            # if len(myCanvas.find_withtag("bots")) >= 2 * maxVehicleNumber:
            delete_vehicle(False)
            create_vehicle()
            # print("speed: ",defualtSpeed, "vehivles: ",len(myCanvas.find_withtag("bots")), "time: ",period)
        unusedTime = 0

        # update player vehicle position
        myCanvas.move(playerVehicle.draw, 0, -playerDefualtSpeed)
        playerVehicle.position_update()
        if playerVehicle.get_position()[1] < -50:
            myCanvas.delete(playerVehicle.draw)
            break
        # print(playerVehicle.get_position())
        # opposite vehicle motion
        for i in vehicleOpposite:
            if i.state != "Deleted" and i.get_position()[1] > 800:
                myCanvas.delete(i.draw)
                i.state = "Deleted"
                continue
            myCanvas.move(i.draw, 0, i.speed)
            # print(len(myCanvas.find_withtag("bots")))
            if not cheatIsOn:
                if i.draw in myCanvas.find_withtag("bots") and collision(playerVehicle.get_position(), i.get_position()):
                    playerLives -= 1
                    if playerLives <= 0:
                        quit() #Add game over
                    myCanvas.itemconfig(livesText, text='Lives: ' + str(playerLives))
                    pause(f"You have {playerLives} lives left")

        sleep(0.02)
        window.update()
    else:
        if pauseState: unusedTime = time()
        elif counter < len(gameLevels) and score >= gameLevels[counter]["score"]:
            print("counter: ", counter, "Score: ", round(score, 2))
            counter += 1
            pause(f"You have finished level {counter-1}")
            main_code()
        else:
            quit()

home(True)
window.mainloop()
