import glfw
from OpenGL.GL import *
import math
import random
import numpy as np
import engine 
import time
from copy import deepcopy
from random import choice, randrange

GW, GH = 10, 20
MODE = 0


tetrominos_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

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
    return False
def bump_ground(rect):
    if rect.y > GH -1 or field[rect.y][rect.x]:
        return True
    return False

def gameEvent(grid, tetromino, dwn, ctr, TILE, Window):
    change = False
    rotate = False
    dx = 0
    dy = dwn
    if glfw.get_key(Window, glfw.KEY_RIGHT):
        dx = 1
    elif glfw.get_key(Window, glfw.KEY_LEFT):
        dx = -1
    elif glfw.get_key(Window, glfw.KEY_UP):
        rotate = True
    elif glfw.get_key(Window, glfw.KEY_DOWN):
        dy = 1
    #check lines
    line = GH-1
    for row in range(GH-1, -1, -1):
        count = 0
        for i in range(GW):
            if field[row][i]:
                count+=1
            field[line][i] = field[row][i]
        if count < GW:
            line -= 1

    # Draw Grid
    [engine.drawRect(rect, 1, Window) for rect in grid]

    #Rotate Tetromino
    old_tet = deepcopy(tetromino)
    center = tetromino[0]
    if rotate:
        for i in range(4):
            x = tetromino[i].y - center.y
            y = tetromino[i].x - center.x
            tetromino[i].x = center.x - x
            tetromino[i].y = center.y + y
            if bump_walls(tetromino[i]):
                tetromino = deepcopy(old_tet)
                break
            elif bump_ground(tetromino[i]):
                tetromino = deepcopy(old_tet)
                break

    # Drawing Tetromino
    # showTetromino(tetromino, Window)
    [engine.drawRect(engine.Rect(tetromino[i].x*TILE,tetromino[i].y*TILE,TILE-2, TILE-2), 2, Window)for i, t in enumerate(tetromino)]
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                engine.drawRect(engine.Rect(x*TILE, y*TILE, TILE-2, TILE-2), 2, Window)
    
    old_tet = deepcopy(tetromino)
    for i in range(4):
        tetromino[i].x +=dx
        tetromino[i].y +=dy
        if bump_walls(tetromino[i]):
            tetromino = deepcopy(old_tet)
            break
        elif bump_ground(tetromino[i]):
            tetromino = deepcopy(old_tet)
            ctr += 2
            if ctr > 30:
                for i in range(4):
                    field[tetromino[i].y][tetromino[i].x] = 1
                change = True
            break
            
    return tetromino, change, ctr

def main():
    # Initialize GLFW
    if not glfw.init():
        return
    # get monitor
    monitor = glfw.get_primary_monitor()
    vidmode = glfw.get_video_mode(monitor)
    v_width = vidmode.size.width
    v_height = vidmode.size.height
    W = v_width
    H = v_height
    TILE = int(v_height/24)
    # print(v_width, v_height, GW, GH, TILE)
    Window = glfw.create_window(W, H, "Tetris", None, None)
    if not Window:
        glfw.terminate()
        return
    # Enable key events
    
    glfw.set_input_mode(Window,glfw.STICKY_KEYS,GL_FALSE) 
    
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
    tetrominos=[[engine.Rect(x+GW//2, y+1, TILE, TILE) for x, y in tetromino] for tetromino in tetrominos_pos]
    grid = [engine.Rect(x*TILE, y * TILE, TILE, TILE) for x in range(GW) for y in range(GH)]
    tetromino = deepcopy(choice(tetrominos))
    st_time = time.time()
    ctr = 0
    while not glfw.window_should_close(Window):
        glfw.poll_events()
        dy = 0
        if time.time()-st_time>1 and ctr < 25:
            dy=1
            st_time = time.time()
            ctr += 1
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)
        engine.render_text(W/2, 70, 70, 10, "Tetris")
        engine.render_text(W/2, 170, 30, 5, "Controls")
        engine.render_text(W/2, 230, 15, 3, "[<] left [>] right [^] rotate [v] down")
        engine.render_text(W/2, 300, 40, 5, "score")
        engine.render_text(W/2, 350, 50, 7, "0000000")

        tetromino, change, ctr = gameEvent(grid, tetromino, dy, ctr, TILE, Window)

        if change:
            tetromino = deepcopy(choice(tetrominos))
            st_time = time.time()
            ctr = 0

        glfw.swap_buffers(Window)

    glfw.terminate()


if __name__ == "__main__":
    main()
