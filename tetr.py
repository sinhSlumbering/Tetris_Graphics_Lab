import glfw
from OpenGL.GL import *
import math
import random
import numpy as np
import engine 
from copy import deepcopy
from random import choice, randrange


GW, GH = 10, 20
W, H = 800, 600
WL, WR, WH = -W/2, W/2-1, -H
Window = None
MODE = 0
TILE = 25

tetrominos_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

tetrominos=[[engine.Rect(x+GW//2, y+1, TILE, TILE) for x, y in tetromino] for tetromino in tetrominos_pos]
field = [[0 for i in range(GW)] for j in range (GH)]



def showTetromino(tetromino, Window):
    print(tetromino)
    tet_rect = engine.Rect(0,0, TILE-2, TILE-2)
    for i in range(4):
        print(tetromino[i].points)
        tet_rect.x = tetromino[i].x * TILE-2
        tet_rect.y = tetromino[i].y * TILE -2
        engine.drawRect(tet_rect, 2, Window)
def bump_walls(rect):
    if rect.x < 0 or rect.x > GW -1:
        return True
    elif rect.y > H -1 or field[rect.y][rect.x]:
        print(rect.y)
        return True
    return False

def gameEvent(grid, tetromino, Window):
    dx = 0
    dy = 0
    if glfw.get_key(Window, glfw.KEY_RIGHT):
        dx = 1
    elif glfw.get_key(Window, glfw.KEY_LEFT):
        dx = -1
    elif glfw.get_key(Window, glfw.KEY_UP):
        dy = -1
    elif glfw.get_key(Window, glfw.KEY_DOWN):
        dy = 1

    old_tet = deepcopy(tetromino)
    for i in range(4):
        tetromino[i].x +=dx
        tetromino[i].y +=dy
        if bump_walls(tetromino[i]):
            tetromino = deepcopy(old_tet)
            break
    
    # drawing Grid
    [engine.drawRect(rect, 1, Window) for rect in grid]
    # Drawing Tetromino
    [engine.drawRect(engine.Rect(int(tetromino[i].x*TILE),int(tetromino[i].y*TILE),TILE-2, TILE-2), 2, Window)for i, t in enumerate(tetromino)]
    return tetromino

def main():
    # Initialize GLFW
    if not glfw.init():
        return
    
    Window = glfw.create_window(W, H, "Roll 15 Polygon Filling", None, None)
    if not Window:
        glfw.terminate()
        return
    # Enable key events
    
    glfw.set_input_mode(Window,glfw.STICKY_KEYS,GL_TRUE) 

    # Enable key event callback
    # glfw.set_key_callback(Window,key_event)
    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up the orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, H, 0, -1,1)
    # glOrtho(-W/2, W/2-1, -H/2, H/2-1, -1,1)

    # Set up to use the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    grid = [engine.Rect(x*TILE, y * TILE, TILE, TILE) for x in range(GW) for y in range(GH)]
    tetromino = choice(tetrominos)
    
    while not glfw.window_should_close(Window):
        glfw.wait_events()


        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        tetromino = gameEvent(grid, tetromino, Window)

        glfw.swap_buffers(Window)

    glfw.terminate()


if __name__ == "__main__":
    main()
