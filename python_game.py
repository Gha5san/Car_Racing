from tkinter import *
from random import randint, choice, shuffle
from time import sleep, time

pauseState    = False
livesMode     = False
cheatIsOn     = False
vehicleNumbers = 0
maxVehicleNumber  = 6
miniVehicleNumber = 0
startingPoint = [360, 650]
windowWidth   = 800
windowHeight  = 700
vehicleWidth  = 55
vehicleHeight = 128
defualtSpeed  = 10
playerDefualtSpeed = 3
playerLives   = 5
vehicleOption = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']


# window = Tk()
# myCanvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
# myCanvas.pack()
# for i in range(100, windowWidth-99, 75):
#     myCanvas.create_line(i, 0, i, windowHeight, dash=(10,3))
#
# livesText = myCanvas.create_text(10, 10, text='Lives: '+str(playerLives), font=('Aerial', 15), anchor='nw')
# scoreText = myCanvas.create_text(100, 10, text='Score: 0', font=('Aerial', 15), anchor='nw')

window = Tk()
myCanvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
myCanvas.pack()
for i in range(100, windowWidth - 99, 75):
    myCanvas.create_line(i, 0, i, windowHeight, dash=(10, 3))

livesText = myCanvas.create_text(10, 10, text='Lives: ' + str(playerLives), font=('Aerial', 15), anchor='nw')
scoreText = myCanvas.create_text(100, 10, text='Score: 0', font=('Aerial', 15), anchor='nw')

class Vehicle():

    def __init__(self, x, y, vehicleType, vehicleTag, player=""):
        self.x     = x
        self.y     = y
        self.speed = 10 + defualtSpeed
        self.dir   = ""
        self.tag = vehicleTag
        self.image = PhotoImage(file=f"images/" + player + vehicleType + ".png")
        self.draw  = myCanvas.create_image(self.x, self.y, image=self.image, tag=self.tag)
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
    #     if self.state == "Deleted":
    #         pass
    #     elif self.state == "Destroy":
    #         pass
    #     elif self.state == "Exist":
    #         pos = self.get_position()
    #
    #         #Check if car is not touching borders
    #         if self.dir == "Right":

    def get_position(self):
        pos = myCanvas.coords(self.draw)
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

def pause(textOutput):
    global pauseState, pauseText, resumeText, livesMode
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
            playerVehicle.draw = myCanvas.create_image(startingPoint[0],
                                                       startingPoint[1],
                                                       image=playerVehicle.image,
                                                       tag=playerVehicle.tag)
            livesMode = False
            delete_vehicle()
            create_vehicle()

        main_code()
    else:
        if textOutput == "Pause":
            pauseText = myCanvas.create_text(400, 350, text=textOutput, font=("Aerial", 100), fill="Black")
            resumeText = myCanvas.create_text(400, 450, text="Click p to resume", font=("Aerial", 20), fill="Black")
        elif textOutput.startswith("Y"):
            pauseText = myCanvas.create_text(400, 350, text=textOutput, font=("Aerial", 30), fill="red")
            resumeText = myCanvas.create_text(400, 450, text="Click p to resume", font=("Aerial", 20), fill="red")
            livesMode = True

        pauseState = True

def player_increase_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed += 2

def player_decrease_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed -= 2

vehicleOpposite = []
loop = True
def create_vehicle():
    global vehicleNumbers
    vehicleNumbers = int(randint(miniVehicleNumber, maxVehicleNumber))
    lanes = [135, 210, 285, 360, 435, 510, 585, 660]
    shuffle(lanes)
    for i in range(vehicleNumbers):
        vehicleOpposite.append(Vehicle(lanes[i], -50, choice(vehicleOption), "bots"))

def collision(pos, pos2):
    if pos[0] < pos2[2] and pos[1] < pos2[3] and pos[2] > pos2[0] and pos[3] > pos2[1]:
        return True
    else:
        return False

def delete_vehicle():
    for i in vehicleOpposite:
            myCanvas.delete(i.draw)
            i.state = "Deleted"

def change_vehicle():
    global  chosenVehicle, vehicleChoice, vehicleButton, vehicleButtonWindow
    vehicleIndex = vehicleOption.index(chosenVehicle)
    if vehicleIndex == 8:
        vehicleIndex = - vehicleIndex
    chosenVehicle = vehicleOption[vehicleIndex + 1]
    vehicleChoice = PhotoImage(file="images/player/" + chosenVehicle + ".png")
    myCanvas.delete(vehicleButtonWindow)
    vehicleButton = Button(window, image=vehicleChoice, borderwidth=0, bg="#857d7a", command=change_vehicle, activebackground="#857d7a")
    vehicleButtonWindow = myCanvas.create_window(336, 590, anchor=NW, window=vehicleButton)
    if selectVehicle in myCanvas.find_all(): myCanvas.delete(selectVehicle)

def cheat_mode_on(event):
    global cheatIsOn
    cheatIsOn = True
def cheat_mode_off(event):
    global cheatIsOn
    cheatIsOn = False
def intiating():
    global playerVehicle

    myCanvas.delete(startButtonWindow)
    myCanvas.delete(vehicleButtonWindow)
    if selectVehicle in myCanvas.find_all(): myCanvas.delete(selectVehicle)
    playerVehicle = Vehicle(startingPoint[0], startingPoint[1], chosenVehicle, "player", "player/")
    myCanvas.bind_all('<Up>', playerVehicle.dir_up)
    myCanvas.bind_all('<Down>', playerVehicle.dir_down)
    myCanvas.bind_all('<Left>', playerVehicle.dir_left)
    myCanvas.bind_all('<Right>', playerVehicle.dir_right)
    myCanvas.bind_all('<a>', player_decrease_speed)
    myCanvas.bind_all('<d>', player_increase_speed)
    myCanvas.bind_all('<p>', lambda x: pause("Pause"))
    myCanvas.bind_all("<KeyPress-c>",   cheat_mode_on)
    myCanvas.bind_all("<KeyRelease-c>", cheat_mode_off)

    main_code()

timeStamps = []
startTime = time()
unusedTime = 0
totatUnusedTime = 0
def main_code():
    global pauseState, playerLives, scoreText, unusedTime, totatUnusedTime, score
    while (not pauseState):
        if unusedTime != 0:
            unusedTime = time() - unusedTime
            totatUnusedTime += unusedTime
        elapsedTime = time() - (startTime + totatUnusedTime)
        score = (elapsedTime * defualtSpeed) / 10
        myCanvas.itemconfig(scoreText, text=f'Score: {round(score, 2)}')
        elapsedTime = int(elapsedTime)
        if elapsedTime % 2 == 0 and elapsedTime not in timeStamps:
            timeStamps.append(elapsedTime)
            if len(myCanvas.find_withtag("bots")) >= 2 * maxVehicleNumber:
                delete_vehicle()
            create_vehicle()
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
            myCanvas.move(i.draw, 0, defualtSpeed)
            # print(len(myCanvas.find_withtag("bots")))
            if not cheatIsOn:
                if i.draw in myCanvas.find_withtag("bots") and collision(playerVehicle.get_position(), i.get_position()):
                    playerLives -= 1
                    myCanvas.itemconfig(livesText, text='Lives: ' + str(playerLives))
                    pause(f"You have {playerLives} lives left")

        sleep(0.02)
        window.update()
    else:
        unusedTime = time()

chosenVehicle = choice(vehicleOption)
vehicleChoice = PhotoImage(file="images/player/" + chosenVehicle +".png")
vehicleButton = Button(window, image=vehicleChoice, borderwidth=0, bg="#857d7a", command=change_vehicle, activebackground="#857d7a")
vehicleButtonWindow = myCanvas.create_window(336, 590, anchor=NW, window=vehicleButton)
selectVehicle = myCanvas.create_text(370, 580, text='Click to switch vehicle: ', font=('Aerial', 15))

startButton = Button(window, text="Start", font=("Aerial", 40), borderwidth=0, bg="#857d7a", command=intiating)
startButtonWindow = myCanvas.create_window(335, 200, window=startButton)


# intiating()
window.mainloop()








