from tkinter import *


world_height = 50
world_width = 50

frame_time = 100

cell_size = 10
run = False

grid = [[0] * world_width for i in range(world_height)]

tickCounter = 0

def countNeighbours(x, y):
    neighbour_rows = [row for row in grid[y-1 if y>0 else 0 : y+2 if y<world_height else world_height]]
    neighbour_cells = [[cell for cell in row[x-1 if x>0 else 0 : x+2 if x<world_width else world_width]] for row in neighbour_rows]
    neighbour_count = 0;
    for row in neighbour_cells:
        for cell in row:
            if cell > 0: neighbour_count += 1

    if grid[y][x] > 0: neighbour_count -= 1

    return neighbour_count

def start():
    global run
    run = True
    tick()

def stop():
    global run
    run = False

def tick():
    global run
    updateGrid()
    drawFrame()
    if(run == True): frame.after(frame_time, tick)

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
    grid = [[0] * world_width for i in range(world_height)]

def canvas_clicked(event):
    # print("canvas clicked", event, canvas.winfo_x(), canvas.winfo_y())
    gridx = int(event.x / cell_size)
    gridy = int(event.y / cell_size)
    # print(gridx, gridy)
    grid[gridy][gridx] = 1 if grid[gridy][gridx] == 0 else 0
    drawFrame()
 
def drawFrame():
    global canvas
    global frame
    canvas.delete("all")
    for y in range(world_height):
        for x in range(world_width):
            if grid[y][x] == 0:
                r = canvas.create_rectangle(x * cell_size, y * cell_size, x * cell_size + cell_size - 1, y * cell_size + cell_size - 1, outline="white")
            else:
                r = canvas.create_rectangle(x * cell_size, y * cell_size, x * cell_size + cell_size - 1, y * cell_size + cell_size - 1, fill="black")
    # frame.after(frame_time, drawFrame)


root = Tk()
 
frame=Frame(root,width=600,height=600)
frame.pack(expand = True, fill=BOTH)
 
canvas = Canvas(frame,bg='white', width = 600,height = 600, scrollregion = (0,0,world_width * cell_size, world_height * cell_size) )
canvas.bind("<Button-1>", canvas_clicked)

btnDraw = Button(frame, text="draw", command=tick)
btnStart = Button(frame, text="start", command=start)
btnStop = Button(frame, text="stop", command=stop)

drawFrame()
 
canvas.pack(expand = True, fill = BOTH)
btnDraw.pack()
btnStart.pack()
btnStop.pack()
 
root.mainloop()