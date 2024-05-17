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
points = {0: 0, 1:100, 2:400, 3: 800, 4: 1600}

palettes = {
    0: [
        (0, 255, 255),  # Cyan
        (255, 255, 0),  # Yellow
        (128, 0, 128),  # Purple
        (0, 255, 0),    # Green
        (255, 0, 0),    # Red
        (0, 0, 255),    # Blue
        (255, 165, 0)   # Orange
    ],
    1: 
    [
        (173, 216, 230),  # Light Blue
        (255, 255, 224),  # Light Yellow
        (216, 191, 216),  # Light Purple
        (144, 238, 144),  # Light Green
        (240, 128, 128),  # Light Coral
        (176, 196, 222),  # Light Steel Blue
        (255, 218, 185)   # Peach
    ], 
    2: 
    [
        (0, 255, 255),   # Neon Cyan
        (255, 255, 0),   # Neon Yellow
        (255, 0, 255),   # Neon Magenta
        (57, 255, 20),   # Neon Green
        (255, 36, 0),    # Neon Red
        (0, 0, 255),     # Neon Blue
        (255, 140, 0)    # Neon Orange
    ]
}
tetrominos_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)], # I
               [(0, -1), (-1, -1), (-1, 0), (0, 0)], # O
               [(-1, 0), (-1, 1), (0, 0), (0, -1)], # Z
               [(0, 0), (-1, 0), (0, 1), (-1, -1)], # S
               [(0, 0), (0, -1), (0, 1), (-1, -1)], # L
               [(0, 0), (0, -1), (0, 1), (1, -1)], # J
               [(0, 0), (0, -1), (0, 1), (-1, 0)]] # T

class Tetromino:
    def __init__(self, pos, name, mp):
        self.pos = pos
        self.name = name + 1
        self.mp = mp
field = [[0 for i in range(GW)] for j in range (GH)]


def bump_walls(rect):
    if rect.x < 0 or rect.x > GW -1:
        return True
    return False
def bump_ground(rect, field):
    if rect.y > GH -1 or field[rect.y][rect.x]:
        return True
    return False

def gameEvent(grid, tetromino, dwn, ctr, TILE, score, field, Window):
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
    line, lines = GH-1, 0
    for row in range(GH-1, -1, -1):
        count = 0
        for i in range(GW):
            if field[row][i]:
                count+=1
            field[line][i] = field[row][i]
        if count < GW:
            line -= 1
        else:
            lines += 1
    score += points[lines]
    # Draw Grid
    [engine.drawRect(rect, 1, Window) for rect in grid]

    #Rotate Tetromino
    old_tet = deepcopy(tetromino)
    center = tetromino.mp[0]
    if rotate:
        for i in range(4):
            x = tetromino.mp[i].y - center.y
            y = tetromino.mp[i].x - center.x
            tetromino.mp[i].x = center.x - x
            tetromino.mp[i].y = center.y + y
            if bump_walls(tetromino.mp[i]):
                tetromino = deepcopy(old_tet)
                break
            elif bump_ground(tetromino.mp[i], field):
                tetromino = deepcopy(old_tet)
                break

    # Drawing Tetromino
    # showTetromino(tetromino, Window)
    [engine.drawRect(engine.Rect(tetromino.mp[i].x*TILE,tetromino.mp[i].y*TILE,TILE-2, TILE-2, tetromino.mp[i].color), 2, Window)for i, t in enumerate(tetromino.mp)]
    
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                engine.drawRect(engine.Rect(x*TILE, y*TILE, TILE-2, TILE-2, palettes[1][col-1]), 2, Window)
    
    old_tet = deepcopy(tetromino)
    for i in range(4):
        tetromino.mp[i].x +=dx
        tetromino.mp[i].y +=dy
        if bump_walls(tetromino.mp[i]):
            tetromino = deepcopy(old_tet)
            break
        elif bump_ground(tetromino.mp[i], field):
            tetromino = deepcopy(old_tet)
            ctr += 2
            if ctr > 30:
                for i in range(4):
                    field[tetromino.mp[i].y][tetromino.mp[i].x] = tetromino.name
                change = True
            break
    for i in range(GW):
        if field[0][i]:
            field = [[0 for i in range(GW)] for i in range(GH)]
            score = 0
            
    return tetromino, change, ctr, score, field

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
    tetrominos=[Tetromino(tetromino, i, [engine.Rect(x+GW//2, y+1, TILE, TILE, palettes[1][i]) for x, y in tetromino]) for i, tetromino in enumerate(tetrominos_pos)]
    grid = [engine.Rect(x*TILE, y * TILE, TILE, TILE, (127, 127, 127)) for x in range(GW) for y in range(GH)]
    field = [[0 for i in range(GW)] for j in range (GH)]
    tetromino = deepcopy(choice(tetrominos))
    next_tet = deepcopy(tetrominos[6])
    st_time = time.time()
    ctr = 0
    score = 0
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
        engine.render_text(W/2, 350, 50, 7, f"{str(score)}")
        [engine.drawRect(engine.Rect(W/2+next_tet.mp[i].x*TILE,H/2+next_tet.mp[i].y*TILE,TILE-2, TILE-2, next_tet.mp[i].color), 2, Window)for i, t in enumerate(next_tet.mp)]
        tetromino, change, ctr, score, field = gameEvent(grid, tetromino, dy, ctr, TILE, score, field, Window)

        if change:
            tetromino = next_tet
            next_tet = deepcopy(choice(tetrominos))
            st_time = time.time()
            ctr = 0

        glfw.swap_buffers(Window)

    glfw.terminate()


if __name__ == "__main__":
    main()
