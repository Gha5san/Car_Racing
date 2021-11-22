from tkinter import *
from random import randint, choice
from time import sleep

windowWidth   = 800
windowHeight  = 700
vehicleWidth  = 93
vehicleHeight = 217
defualtSpeed  = 10
playerLives   = 5
vehicleOption = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']

window = Tk()
canvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
canvas.pack()
for i in range(100, windowWidth, 150):
    canvas.create_line(i, 0, i, windowHeight)

livesTxt = canvas.create_text(10, 10, text='Lives: '+str(playerLives), font=('Aerial', 15), anchor='nw')

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
                canvas.move(self.draw, -self.speed, 0)
            elif self.dir == "right":
                canvas.move(self.draw, self.speed, 0)
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

playerVehicle = Vehicle(175, 700, "Car", "player/")

canvas.bind_all('<Up>', playerVehicle.dir_up)
canvas.bind_all('<Down>', playerVehicle.dir_down)
canvas.bind_all('<Left>', playerVehicle.dir_left)
canvas.bind_all('<Right>', playerVehicle.dir_right)

# vehicleImage = PhotoImage(file="images/player/Car.png")
# vehicleCanvas = canvas.create_image(175, 0, image=vehicleImage)
vehicleOpposite1 = Vehicle(200,0, choice(vehicleOption))
while True:
    # pos = playerVehicle.get_position()
    print(playerVehicle.get_position())
    if playerVehicle.get_position()[1] > 700:
        canvas.delete(playerVehicle.draw)
        break
    canvas.move(playerVehicle.draw, 0, -defualtSpeed+5)
    playerVehicle.position_update()

    if vehicleOpposite1.state != "Deleted" and vehicleOpposite1.get_position()[1] < -100:
        canvas.delete(vehicleOpposite1.draw)
        vehicleOpposite1.state = "Deleted"
    canvas.move(vehicleOpposite1.draw, 0, defualtSpeed)

    sleep(0.02)
    window.update()




window.mainloop()

