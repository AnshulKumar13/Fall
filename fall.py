import tkinter as tk
from tkinter import ttk
import time
import random as rnd
import threading

HEIGHT = 650 
WIDTH = 600
TICK_INTERVAL = 0.01
BLOCK_COLOR = 'purple'
BASE_COLOR = 'black'

leftLock = threading.Lock()
rightLock = threading.Lock()

gameState = 0
blocks = [] # list of lists: [rectangle, velocity in pixels/second]
leftKeyPressed = 0
rightKeyPressed = 0

def main():
    window = tk.Tk()
    canvas = tk.Canvas(window, width = WIDTH, height = HEIGHT)
    canvas.pack()
    window.geometry(f"{WIDTH}x{HEIGHT}+0+0")
    window.resizable(False, False)

    base = canvas.create_rectangle(WIDTH / 2, HEIGHT - 10, (WIDTH / 2) + 20, HEIGHT, fill = BASE_COLOR)
    window.bind('<KeyPress-Left>', pressLeft)
    window.bind('<KeyRelease-Left>', releaseLeft)
    window.bind('<KeyPress-Right>', pressRight)
    window.bind('<KeyRelease-Right>', releaseRight)
    
    gameState = 1
    newBlock = 0
    clean = 1 / TICK_INTERVAL
    while gameState:
        if newBlock == 0:
            newBlock = createNewBlock(canvas)

        if clean == 0:
            cleanBlocks(canvas)
            clean = 1 / TICK_INTERVAL

        updateBlockPositions(canvas)
        updateBasePosition(canvas, base)
        
        newBlock -= 1
        clean -= 1
        window.update_idletasks()
        window.update()
        time.sleep(TICK_INTERVAL)

def createNewBlock(canvas = tk.Canvas):
    x = int(rnd.random() * WIDTH)
    y = 0
    rec = canvas.create_rectangle(x, y, x + 10, y + 10, fill = BLOCK_COLOR)
    blocks.append([rec, 170])
    return ((1/TICK_INTERVAL)/2) + int(rnd.random() * ((1/TICK_INTERVAL)/2))

def updateBlockPositions(canvas = tk.Canvas):
    length = len(blocks)
    for i in range(length):
        block = blocks[i]
        pxlsPerTick = block[1] / (1 / TICK_INTERVAL)
        canvas.move(block[0], 0, pxlsPerTick)

        if len(canvas.coords(block[0])) > 0 and canvas.coords(block[0])[1] >= HEIGHT:
            canvas.delete(block[0])

def cleanBlocks(canvas = tk.Canvas):
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if len(canvas.coords(block[0])) == 0:
            blocks.pop(i)
            i -= 1
        i += 1

    print("cleaned... New Length: " + str(len(blocks)))

def updateBasePosition(canvas = tk.Canvas, base = int):
    global leftKeyPressed, rightKeyPressed
    
    if leftKeyPressed:
        canvas.move(base, -10, 0)

    if rightKeyPressed:
        canvas.move(base, 10, 0)

def pressLeft(event):
    global leftKeyPressed
    
    if not leftKeyPressed:
        leftLock.acquire()
        leftKeyPressed = 1
        leftLock.release()

def releaseLeft(event):
    global leftKeyPressed
    
    if leftKeyPressed:
        leftLock.acquire()
        leftKeyPressed = 0
        leftLock.release()

def pressRight(event):
    global rightKeyPressed

    if not rightKeyPressed:
        rightLock.acquire()
        rightKeyPressed = 1
        rightLock.release()

def releaseRight(event):
    global rightKeyPressed

    if rightKeyPressed:
        rightLock.acquire()
        rightKeyPressed = 0
        rightLock.release()

if __name__ == "__main__":
    main()