from tkinter import *
import os
import random


world_height = 50
world_width = 50

frame_time = 100

cell_size = 10
run = False

border_colour = "grey"


grid = [[0] * world_width for i in range(world_height)]

tickCounter = 0

def gridForEach(grid, callback):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            grid[x][y] = callback(grid[x][y])


def countNeighbours(x, y):
    neighbour_rows = [row for row in grid[y-1 if y>0 else 0 : y+2 if y<world_height else world_height]]
    neighbour_cells = [[cell for cell in row[x-1 if x>0 else 0 : x+2 if x<world_width else world_width]] for row in neighbour_rows]
    neighbour_count = 0;
    for row in neighbour_cells:
        for cell in row:
            if cell > 0: neighbour_count += 1

    if grid[y][x] > 0: neighbour_count -= 1

    return neighbour_count

def toggleRun():
    global run
    run = not run
    btnRunStop.configure(image = images["pause"] if run else images["play"])
    btnClear.configure(state = DISABLED if run else NORMAL)
    btnTick.configure(state = DISABLED if run else NORMAL)
    btnRandom.configure(state = DISABLED if run else NORMAL)
    tick()

def tick():
    global run
    updateGrid()
    drawFrame()
    if(run == True): worldFrame.after(frame_time, tick)

def updateGrid():
    global tickCounter
    global grid
    newGrid =  [[0] * world_width for i in range(world_height)]
    for y in range(world_height):
        for x in range(world_width):
            neighbourCount = countNeighbours(x, y)
            if grid[y][x] > 0 :
                if neighbourCount > 1 and neighbourCount < 4: newGrid[y][x] = 1
            else:
                if neighbourCount == 3: newGrid[y][x] = 1

    grid = [[cell for cell in row] for row in newGrid]
    tickCounter += 1

def clear():
    global grid
    gridForEach(grid, lambda x : 0)

def randomizeGrid():
    global grid
    gridForEach(grid, lambda x : random.choice([0,1]))

def canvas_clicked(event):
    # print("canvas clicked", event, canvas.winfo_x(), canvas.winfo_y())
    gridx = int(event.x / cell_size)
    gridy = int(event.y / cell_size)
    # print(gridx, gridy)
    grid[gridy][gridx] = 1 if grid[gridy][gridx] == 0 else 0
    drawFrame()
 
def drawFrame():
    global canvas
    global worldFrame
    global drawBorders
    canvas.delete("all")
    for y in range(world_height):
        for x in range(world_width):
            if grid[y][x] == 0:
                r = canvas.create_rectangle(x * cell_size, y * cell_size, x * cell_size + cell_size - 1, y * cell_size + cell_size - 1, outline = border_colour if drawBorders.get() else "white")
            else:
                r = canvas.create_rectangle(x * cell_size, y * cell_size, x * cell_size + cell_size - 1, y * cell_size + cell_size - 1, fill="black")
    # frame.after(frame_time, drawFrame)

def clearClicked():
    clear()
    drawFrame()

def randomClicked():
    randomizeGrid()
    drawFrame()

root = Tk()
root.title("Conway's Game of Life")
 
worldFrame=Frame(root)
worldFrame.pack(expand = True, side = TOP)
buttonFrame = Frame(root)
buttonFrame.pack(side = BOTTOM)

 
canvas = Canvas(worldFrame,bg='white',width=world_width * cell_size,height=world_height * cell_size, scrollregion = (0,0,world_width * cell_size, world_height * cell_size) )
canvas.bind("<Button-1>", canvas_clicked)


dirPath = os.path.dirname(__file__) + "/"
images = {
    "clear": PhotoImage(file=dirPath + "images/clear.png"),
    "step_fwd": PhotoImage(file=dirPath + "images/step_forward.png"),
    "step_back": PhotoImage(file=dirPath + "images/step_back.png"),
    "play": PhotoImage(file=dirPath + "images/play.png"),
    "pause": PhotoImage(file=dirPath + "images/pause.png")
}

btnClear = Button(buttonFrame, image=images["clear"], command=clearClicked)
btnRunStop = Button(buttonFrame, image=images["play"], command=toggleRun)
btnTick = Button(buttonFrame, image=images["step_fwd"], command=tick)
btnRandom = Button(buttonFrame, text="random", command=randomClicked)
drawBorders = BooleanVar(buttonFrame, True)

chkBorders = Checkbutton(buttonFrame, variable = drawBorders, command=drawFrame, text = "Draw Borders")
canvas.pack(expand = True, fill = BOTH)
btnRandom.pack(side=LEFT)
btnClear.pack(side=LEFT)
btnRunStop.pack(side=LEFT)
btnTick.pack(side=LEFT)
chkBorders.pack(side=LEFT)

drawFrame()

 
 
root.mainloop()