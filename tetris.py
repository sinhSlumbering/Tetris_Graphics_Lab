import json
import os
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

class GameState:
    def __init__(self, window, tile_size):
        self.window = window
        self.tile_size = tile_size
        self.grid = [engine.Rect(x*tile_size, y * tile_size, tile_size, tile_size, (127, 127, 127)) for x in range(GW) for y in range(GH)]
        self.field = [[0 for _ in range(GW)] for _ in range(GH)]
        self.tetrominos = [Tetromino(tetromino, i, [engine.Rect(x+GW//2, y+1, tile_size, tile_size, palettes[0][i]) for x, y in tetromino]) for i, tetromino in enumerate(tetrominos_pos)]
        self.tetromino = deepcopy(choice(self.tetrominos))
        self.next_tetromino = deepcopy(self.tetrominos[6])
        self.palette_index = 0
        self.score = 0
        self.ctr = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = 1.0
        self.start_time = time.time()
        self.high_score = self.load_high_score()

    def bump_walls(self, rect):
        if rect.x < 0 or rect.x > GW - 1:
            return True
        return False

    def bump_ground(self, rect):
        if rect.y > GH - 1 or self.field[rect.y][rect.x]:
            return True
        return False

    def rotate_tetromino(self):
        old_tet = deepcopy(self.tetromino)
        center = self.tetromino.mp[0]
        for i in range(4):
            x = self.tetromino.mp[i].y - center.y
            y = self.tetromino.mp[i].x - center.x
            self.tetromino.mp[i].x = center.x - x
            self.tetromino.mp[i].y = center.y + y
            if self.bump_walls(self.tetromino.mp[i]) or self.bump_ground(self.tetromino.mp[i]):
                self.tetromino = deepcopy(old_tet)
                break

    def check_lines(self):
        line, lines = GH - 1, 0
        for row in range(GH - 1, -1, -1):
            count = 0
            for i in range(GW):
                if self.field[row][i]:
                    count += 1
                self.field[line][i] = self.field[row][i]
            if count < GW:
                line -= 1
            else:
                lines += 1
        self.score += points[lines]
        self.lines_cleared += lines
        if self.lines_cleared >= 10:
            self.level_up()

    def level_up(self):
        self.lines_cleared = 0
        self.level += 1
        self.fall_speed = max(0.1, 1.0 - (self.level - 1) * 0.05)
        self.change_palette()

    def change_palette(self):
        self.palette_index = self.level % len(palettes)
        new_palette = palettes[self.palette_index]
        for tetromino in self.tetrominos:
            for block in tetromino.mp:
                block.color = new_palette[tetromino.name - 1]

    def game_event(self, dy):
        change = False
        rotate = False
        dx = 0
        game_over = False

        if glfw.get_key(self.window, glfw.KEY_RIGHT):
            dx = 1
        elif glfw.get_key(self.window, glfw.KEY_LEFT):
            dx = -1
        elif glfw.get_key(self.window, glfw.KEY_UP):
            rotate = True
        elif glfw.get_key(self.window, glfw.KEY_DOWN):
            dy = 1

        self.check_lines()

        # Draw Grid
        [engine.drawRect(rect, 1, self.window) for rect in self.grid]

        # Rotate Tetromino
        if rotate:
            self.rotate_tetromino()

        # Drawing Tetromino
        [engine.drawRect(engine.Rect(self.tetromino.mp[i].x * self.tile_size, self.tetromino.mp[i].y * self.tile_size, self.tile_size - 2, self.tile_size - 2, self.tetromino.mp[i].color), 2, self.window) for i, t in enumerate(self.tetromino.mp)]

        for y, raw in enumerate(self.field):
            for x, col in enumerate(raw):
                if col:
                    engine.drawRect(engine.Rect(x * self.tile_size, y * self.tile_size, self.tile_size - 2, self.tile_size - 2, palettes[self.palette_index][col - 1]), 2, self.window)

        old_tet = deepcopy(self.tetromino)
        for i in range(4):
            self.tetromino.mp[i].x += dx
            self.tetromino.mp[i].y += dy
            if self.bump_walls(self.tetromino.mp[i]) or self.bump_ground(self.tetromino.mp[i]):
                self.tetromino = deepcopy(old_tet)
                if dy:
                    self.ctr += 2
                    if self.ctr > 30:
                        for i in range(4):
                            self.field[self.tetromino.mp[i].y][self.tetromino.mp[i].x] = self.tetromino.name
                        change = True
                break

        for i in range(GW):
            if self.field[0][i]:
                self.save_high_score()
                game_over = True

        return change, game_over

    def load_high_score(self):
        if os.path.exists("highscore.json"):
            with open("highscore.json", "r") as file:
                return json.load(file).get("high_score", 0)
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.json", "w") as file:
                json.dump({"high_score": self.high_score}, file)

    def reset(self):
        self.field = [[0 for _ in range(GW)] for _ in range(GH)]
        self.tetromino = deepcopy(choice(self.tetrominos))
        self.next_tetromino = deepcopy(choice(self.tetrominos))
        self.palette_index = 0
        self.score = 0
        self.ctr = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = 1.0
        self.start_time = time.time()

class StartScreen:
    def __init__(self, window):
        self.window = window

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        engine.render_text(300, 100, 100, 10, "Tetris")
        engine.render_text(300, 200, 30, 5, "Press Enter to Start")
        engine.render_text(300, 300, 20, 4, "Controls:")
        engine.render_text(300, 350, 15, 3, "[<] left [>] right [^] rotate [v] down")
        glfw.swap_buffers(self.window)

    def handle_input(self):
        if glfw.get_key(self.window, glfw.KEY_ENTER):
            return True
        return False

class PauseScreen:
    def __init__(self, window):
        self.window = window

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        engine.render_text(300, 200, 50, 7, "Paused")
        engine.render_text(300, 300, 30, 5, "Press R to Resume")
        engine.render_text(300, 400, 30, 5, "Press ESC to Exit")
        glfw.swap_buffers(self.window)

    def handle_input(self):
        if glfw.get_key(self.window, glfw.KEY_R):
            return "resume"
        if glfw.get_key(self.window, glfw.KEY_ESCAPE):
            return "exit"
        return None

class GameOverScreen:
    def __init__(self, window, score, high_score):
        self.window = window
        self.score = score
        self.high_score = high_score

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
        engine.render_text(300, 200, 50, 7, "Game Over")
        engine.render_text(300, 300, 30, 5, f"Score: {self.score}")
        engine.render_text(300, 350, 20, 4, f"High Score: {self.high_score}")
        engine.render_text(300, 400, 30, 5, "Press Enter to Restart")
        glfw.swap_buffers(self.window)

    def handle_input(self):
        if glfw.get_key(self.window, glfw.KEY_ENTER):
            return True
        return False

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
    TILE = int(v_height / 24)

    Window = glfw.create_window(W, H, "Tetris", None, None)
    if not Window:
        glfw.terminate()
        return
    # Enable key events
    glfw.set_input_mode(Window, glfw.STICKY_KEYS, GL_FALSE)

    glfw.make_context_current(Window)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up the orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, H, 0, -1, 1)

    # Set up to use the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    start_screen = StartScreen(Window)
    pause_screen = PauseScreen(Window)

    game_started = False
    game_paused = False
    game_over = False

    while not glfw.window_should_close(Window):
        glfw.poll_events()

        if not game_started:
            start_screen.render()
            if start_screen.handle_input():
                game_started = True
                game_state = GameState(Window, TILE)

        elif game_paused:
            pause_screen.render()
            action = pause_screen.handle_input()
            if action == "resume":
                game_paused = False
            elif action == "exit":
                break

        elif game_over:
            game_over_screen = GameOverScreen(Window, game_state.score, game_state.high_score)
            game_over_screen.render()
            if game_over_screen.handle_input():
                game_state.reset()
                game_started = True
                game_paused = False
                game_over = False

        else:
            dy = 0
            if time.time() - game_state.start_time > game_state.fall_speed and game_state.ctr < 25:
                dy = 1
                game_state.start_time = time.time()
                game_state.ctr += 1
            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT)
            engine.render_text(W / 2, 70, 70, 10, "Tetris")
            engine.render_text(W / 2, 170, 30, 5, "Controls")
            engine.render_text(W / 2, 230, 15, 3, "[<] left [>] right [^] rotate [v] down")
            engine.render_text(W / 2, 300, 40, 5, "Score")
            engine.render_text(W / 2, 350, 50, 7, f"{str(game_state.score)}")
            engine.render_text(W / 2, 400, 30, 5, f"High Score: {str(game_state.high_score)}")
            engine.render_text(W / 2, 450, 30, 5, f"Level: {str(game_state.level)}")
            [engine.drawRect(engine.Rect(W / 2 + game_state.next_tetromino.mp[i].x * TILE, H / 2 + game_state.next_tetromino.mp[i].y * TILE, TILE - 2, TILE - 2, game_state.next_tetromino.mp[i].color), 2, Window) for i, t in enumerate(game_state.next_tetromino.mp)]
            change, game_over = game_state.game_event(dy)

            if change:
                game_state.tetromino = game_state.next_tetromino
                game_state.next_tetromino = deepcopy(choice(game_state.tetrominos))
                game_state.start_time = time.time()
                game_state.ctr = 0

            if glfw.get_key(Window, glfw.KEY_P):
                game_paused = True

            glfw.swap_buffers(Window)

    glfw.terminate()

if __name__ == "__main__":
    main()
