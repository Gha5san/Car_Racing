from tkinter import *
from random import randint, choice
from time import sleep

windowWidth = 800
windowHeight = 700
playerLives = 5
direction = ['Ambulance', 'Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'Police', 'taxi', 'truck']

window = Tk()
canvas = Canvas(window, width=windowWidth, height=windowHeight, bg='#857d7a')
canvas.pack()
for i in range(100, windowWidth, 150):
    canvas.create_line(i, 0, i, windowHeight)

livesTxt = canvas.create_text(10, 10, text='Lives: '+str(playerLives), font=('Aerial', 15), anchor='nw')

vehicleImage = PhotoImage(file="images/Car.png")
vehicleCanvas = canvas.create_image(175, 500, image=vehicleImage)

while True:
    pos = canvas.coords(vehicleCanvas)
    if pos[1] < 0:
        canvas.delete(vehicleCanvas)
        break
    canvas.move(vehicleCanvas, 0, -10)
    sleep(0.02)
    window.update()

window.mainloop()

