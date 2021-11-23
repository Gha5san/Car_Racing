from tkinter import *
from random import randint, choice, shuffle
from time import sleep, time

pauseState         = False
windowWidth   = 800
windowHeight  = 700
vehicleWidth  = 55
vehicleHeight = 128
defualtSpeed  = 10
playerDefualtSpeed = defualtSpeed
playerLives   = 5
vehicleOption = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']

window = Tk()
myCanvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
myCanvas.pack()
for i in range(100, windowWidth-99, 75):
    myCanvas.create_line(i, 0, i, windowHeight, dash=(10,3))

livesText = myCanvas.create_text(10, 10, text='Lives: '+str(playerLives), font=('Aerial', 15), anchor='nw')
timeText = myCanvas.create_text(100, 10, text='Time: 0', font=('Aerial', 15), anchor='nw')

class Vehicle():

    def __init__(self, x, y, vehicleType, player=""):
        self.x     = x
        self.y     = y
        self.speed = 10 + defualtSpeed
        self.dir   = ""
        self.image = PhotoImage(file=f"images/" + player + vehicleType + ".png")
        self.draw  = myCanvas.create_image(self.x, self.y, image=self.image)
        self.state = "Exist"
        self.width = vehicleWidth
        self.height= vehicleHeight

    def position_update(self):
        pos = self.get_position()
        if pos[1] < 25 or pos[1] > 675 or pos[0] < 125 or pos[0] > 675:
            pause(None)
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

def pause(event):
    global pauseState, pauseText
    if pauseState:
        myCanvas.delete(pauseText)
        pauseState = False
        pausePosition = playerVehicle.get_position()

        if pausePosition[0] <= 115:
            myCanvas.delete(playerVehicle.draw)
            playerVehicle.draw = myCanvas.create_image(pausePosition[0] + 75,
                                                       pausePosition[1],
                                                       image=playerVehicle.image)

        elif pausePosition[0] >= 735:
            myCanvas.delete(playerVehicle.draw)
            playerVehicle.draw = myCanvas.create_image(pausePosition[0] - 75,
                                                       pausePosition[1],
                                                       image=playerVehicle.image)

        else:
            myCanvas.delete(playerVehicle.draw)
            playerVehicle.draw = myCanvas.create_image(pausePosition[0],
                                                       pausePosition[1],
                                                       image=playerVehicle.image)
        main_code()
    else:
        pauseText = myCanvas.create_text(400, 350, text="Pause", font=("Aerial", 100), fill="Black")
        pauseState = True


def player_increase_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed += 2

def player_decrease_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed -= 2

playerVehicle = Vehicle(360, 650, "Car", "player/")
myCanvas.bind_all('<Up>', playerVehicle.dir_up)
myCanvas.bind_all('<Down>', playerVehicle.dir_down)
myCanvas.bind_all('<Left>', playerVehicle.dir_left)
myCanvas.bind_all('<Right>', playerVehicle.dir_right)
myCanvas.bind_all('<a>', player_decrease_speed)
myCanvas.bind_all('<d>', player_increase_speed)
myCanvas.bind_all('<p>', pause)

vehicleOpposite = []
loop = True
def create_vehicle():
    global vehicleNumbers
    vehicleNumbers = int(randint(2, 6))
    lanes = [135, 210, 285, 360, 435, 510, 585, 660]
    shuffle(lanes)
    for i in range(vehicleNumbers):
        vehicleOpposite.append(Vehicle(lanes[i], -50, choice(vehicleOption)))

def collision(pos, pos2):
    if pos[0] < pos2[2] and pos[1] < pos2[3] and pos[2] > pos2[0] and pos[3] > pos2[1]:
        return True
    else:
        return False

# create_vehicle()
timeStamps = []
startTime = time()
def main_code():
    global pauseState, playerLives, timeText
    while (True and not pauseState):
        # print(pauseState)
        elapsedTime = round(time() - startTime, 2)
        myCanvas.itemconfig(timeText, text=f'Time: {elapsedTime}')
        elapsedTime = int(elapsedTime)
        if elapsedTime % 5 == 0 and elapsedTime not in timeStamps:
            timeStamps.append(elapsedTime)
            create_vehicle()

        # pos = playerVehicle.get_position()
        #update player vehicle position

        myCanvas.move(playerVehicle.draw, 0, -playerDefualtSpeed+9)
        playerVehicle.position_update()
        if playerVehicle.get_position()[1] < -50:
            myCanvas.delete(playerVehicle.draw)
            break
        # print(playerVehicle.get_position())
        # opposite vehicle motion
        for i in vehicleOpposite[-vehicleNumbers:]:
            if i.state != "Deleted" and i.get_position()[1] > 800:
                myCanvas.delete(i.draw)
                i.state = "Deleted"
                continue
            myCanvas.move(i.draw, 0, defualtSpeed)
            if i.draw in myCanvas.find_all() and collision(playerVehicle.get_position(), i.get_position()):
                playerLives -= 1
                myCanvas.itemconfig(livesText, text='Lives: '+str(playerLives))

        sleep(0.02)
        window.update()
main_code()

window.mainloop()

