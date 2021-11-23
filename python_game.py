from tkinter import *
from random import randint, choice, shuffle
from time import sleep, time

windowWidth   = 800
windowHeight  = 700
vehicleWidth  = 55
vehicleHeight = 128
defualtSpeed  = 10
playerDefualtSpeed = defualtSpeed
playerLives   = 5
vehicleOption = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']

window = Tk()
canvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
canvas.pack()
for i in range(100, windowWidth-99, 75):
    canvas.create_line(i, 0, i, windowHeight, dash=(10,3))
    # print(i)

# livesTxt = canvas.create_text(10, 10, text='Lives: '+str(playerLives), font=('Aerial', 15), anchor='nw')
timeText = canvas.create_text(10, 10, text='Time: 0', font=('Aerial', 15), anchor='nw')

class Vehicle():

    def __init__(self, x, y, vehicleType, player=""):
        self.x     = x
        self.y     = y
        self.speed = 10 + defualtSpeed
        self.dir   = ""
        self.image = PhotoImage(file=f"images/" + player + vehicleType + ".png")
        self.draw  = canvas.create_image(self.x, self.y, image=self.image)
        self.state = "Exist"
        self.width = vehicleWidth
        self.height= vehicleHeight

    def position_update(self):
        pos = self.get_position()
        if pos[1] < 25 or pos[1] > 675 or pos[0] < 125 or pos[0] > 675:
            pass
        else:
            if self.dir == "up":
                canvas.move(self.draw, 0, -self.speed - defualtSpeed)
            elif self.dir == "down":
                canvas.move(self.draw, 0, self.speed)
            elif self.dir == "left":
                canvas.move(self.draw, -75, 0)
            elif self.dir == "right":
                canvas.move(self.draw, 75, 0)
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
        pos = canvas.coords(self.draw)
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

def player_increase_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed += 2
def player_decrease_speed(event):
    global playerDefualtSpeed
    playerDefualtSpeed -= 2


playerVehicle = Vehicle(360, 700, "Car", "player/")
canvas.bind_all('<Up>', playerVehicle.dir_up)
canvas.bind_all('<Down>', playerVehicle.dir_down)
canvas.bind_all('<Left>', playerVehicle.dir_left)
canvas.bind_all('<Right>', playerVehicle.dir_right)
canvas.bind_all('<a>', player_decrease_speed)
canvas.bind_all('<d>', player_increase_speed)

vehicleOpposite = []
loop = True
def create_vehicle():
    global vehicleOpposite, loop, vehicleOption
    # while loop:
    lanes = [135, 210, 285, 360, 435, 510, 585, 660]
    shuffle(lanes)
    for i in range(5):
        vehicleOpposite.append(Vehicle(lanes[i], -50, choice(vehicleOption)))

# create_vehicle()
timeStamps = []
startTime = time()
while True:
    elapsedTime = round(time() - startTime, 2)
    canvas.itemconfig(timeText, text=f'Time: {elapsedTime}')
    elapsedTime = int(elapsedTime)
    if elapsedTime % 5 == 0 and elapsedTime not in timeStamps:
        timeStamps.append(elapsedTime)
        create_vehicle()

    # pos = playerVehicle.get_position()
    #update player vehicle position

    canvas.move(playerVehicle.draw, 0, -playerDefualtSpeed+5)
    playerVehicle.position_update()
    if playerVehicle.get_position()[1] < -50:
        canvas.delete(playerVehicle.draw)
        break

    # opposite vehicle motion
    for i in vehicleOpposite[-5:]:
        if i.state != "Deleted" and i.get_position()[1] > 800:
            canvas.delete(i.draw)
            i.state = "Deleted"
        canvas.move(i.draw, 0, defualtSpeed)

    sleep(0.02)
    window.update()


window.mainloop()

