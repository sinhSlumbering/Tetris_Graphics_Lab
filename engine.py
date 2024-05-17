import glfw
from OpenGL.GL import *
import math
import random
import numpy as np


POINTS_ONLY = 0
BORDER = 1
FILLED = 2

class Rect:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = [(x, y), (x, y+height), (x+width, y+height), (x+width, y)]
        
class Polygon:
    def __init__(self, points):
        self.points = points


class Edge:
    def __init__(self, ymin, ymax, x, slope_inverse, x1, y1, x2, y2):
        self.ymin = ymin
        self.ymax = ymax
        self.x = x
        self.slope_inverse = slope_inverse
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
# Example 5x7 bitmap font for uppercase letters and digits
font = {
    'A': [
        0b01110,
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001,
        0b10001,
    ],
    'B': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10001,
        0b10001,
        0b11110,
    ],
    'C': [
        0b01111,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b01111,
    ],
    'D': [
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b11110,
    ],
    'E': [
        0b11111,
        0b10000,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b11111,
    ],
    'F': [
        0b11111,
        0b10000,
        0b10000,
        0b11110,
        0b10000,
        0b10000,
        0b10000,
    ],
    'G': [
        0b01111,
        0b10000,
        0b10000,
        0b10011,
        0b10001,
        0b10001,
        0b01111,
    ],
    'H': [
        0b10001,
        0b10001,
        0b10001,
        0b11111,
        0b10001,
        0b10001,
        0b10001,
    ],
    'I': [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b11111,
    ],
    'J': [
        0b00001,
        0b00001,
        0b00001,
        0b00001,
        0b00001,
        0b10001,
        0b01110,
    ],
    'K': [
        0b10001,
        0b10010,
        0b10100,
        0b11000,
        0b10100,
        0b10010,
        0b10001,
    ],
    'L': [
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b10000,
        0b11111,
    ],
    'M': [
        0b10001,
        0b11011,
        0b10101,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
    ],
    'N': [
        0b10001,
        0b10001,
        0b11001,
        0b10101,
        0b10011,
        0b10001,
        0b10001,
    ],
    'O': [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    'P': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10000,
        0b10000,
        0b10000,
    ],
    'Q': [
        0b01110,
        0b10001,
        0b10001,
        0b10001,
        0b10101,
        0b10010,
        0b01101,
    ],
    'R': [
        0b11110,
        0b10001,
        0b10001,
        0b11110,
        0b10100,
        0b10010,
        0b10001,
    ],
    'S': [
        0b01111,
        0b10000,
        0b10000,
        0b01110,
        0b00001,
        0b00001,
        0b11110,
    ],
    'T': [
        0b11111,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
    ],
    'U': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    'V': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100,
    ],
    'W': [
        0b10001,
        0b10001,
        0b10001,
        0b10001,
        0b10101,
        0b10101,
        0b01010,
    ],
    'X': [
        0b10001,
        0b10001,
        0b01010,
        0b00100,
        0b01010,
        0b10001,
        0b10001,
    ],
    'Y': [
        0b10001,
        0b10001,
        0b10001,
        0b01010,
        0b00100,
        0b00100,
        0b00100,
    ],
    'Z': [
        0b11111,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b10000,
        0b11111,
    ],
    '0': [
        0b01110,
        0b10001,
        0b10011,
        0b10101,
        0b11001,
        0b10001,
        0b01110,
    ],
    '1': [
        0b00100,
        0b01100,
        0b00100,
        0b00100,
        0b00100,
        0b00100,
        0b11111,
    ],
    '2': [
        0b01110,
        0b10001,
        0b00001,
        0b00110,
        0b01000,
        0b10000,
        0b11111,
    ],
    '3': [
        0b11110,
        0b00001,
        0b00001,
        0b01110,
        0b00001,
        0b00001,
        0b11110,
    ],
    '4': [
        0b00010,
        0b00110,
        0b01010,
        0b10010,
        0b11111,
        0b00010,
        0b00010,
    ],
    '5': [
        0b11111,
        0b10000,
        0b11110,
        0b00001,
        0b00001,
        0b10001,
        0b01110,
    ],
    '6': [
        0b01110,
        0b10000,
        0b11110,
        0b10001,
        0b10001,
        0b10001,
        0b01110,
    ],
    '7': [
        0b11111,
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b01000,
        0b01000,
    ],
    '8': [
        0b01110,
        0b10001,
        0b10001,
        0b01110,
        0b10001,
        0b10001,
        0b01110,
    ],
    '9': [
        0b01110,
        0b10001,
        0b10001,
        0b01111,
        0b00001,
        0b10001,
        0b01110,
    ],
    '[': [
        0b01110,
        0b01000,
        0b01000,
        0b01000,
        0b01000,
        0b01000,
        0b01110,
    ],
    ']': [
        0b01110,
        0b00010,
        0b00010,
        0b00010,
        0b00010,
        0b00010,
        0b01110,
    ],
    '>':[
        0b10000,
        0b01000,
        0b00100,
        0b00010,
        0b00100,
        0b01000,
        0b10000,
    ],
    '<':[
        0b00001,
        0b00010,
        0b00100,
        0b01000,
        0b00100,
        0b00010,
        0b00001,
    ],
    '^':[
        0b00000,
        0b00000,
        0b00000,
        0b00100,
        0b01010,
        0b01010,
        0b10001,
    ]

}

def get_char_bitmap(char):
    return font.get(char.upper(), [0] * 7)  # Return empty bitmap for undefined characters


# Render function
def render_text(x, y, height, pointSize, text):
    glColor3ub(255, 255, 255)
    glPointSize(pointSize)
    glBegin(GL_POINTS)
    
    scale = height / 7  # Calculate scale based on desired character height
    start_x = x
    
    for char in text:
        bitmap = get_char_bitmap(char)
        for row in range(7):
            bits = bitmap[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    glVertex2f(x + col * scale, y + row * scale)
        x += 6 * scale  # Move to the next character position

    glEnd() 
        


def get_zone(x0, y0, x1, y1):
    dx= x1-x0
    dy= y1-y0

    if dx>=0 and dy>=0:
        if dx > dy:
            return 0
        return 1

    elif dx>=0 and dy<0:
        if dx > abs(dy):
            return 7
        return 6

    elif dx<0 and dy>=0:
        if abs(dx) > dy :
            return 3
        return 2

    else:
        if abs(dx)>abs(dy):
            return 4
        return 5

def return_back(zone, x, y): 
    if zone == 0:
        return y, -x
    elif zone == 1:
        return -x, y
    elif zone == 2:
        return x, y 
    elif zone == 3:
        return -y, -x 
    elif zone == 4:
        return -y, x 
    elif zone == 5:
        return x, -y 
    elif zone == 6:
        return -x, -y 
    else:
        return y, x
    
def allZone_to_2(zone, x, y): 
    if zone == 0:
        return -y, x
    elif zone == 1:
        return -x, y
    elif zone == 2:
        return x, y 
    elif zone == 3:
        return -y, -x 
    elif zone == 4:
        return y, -x 
    elif zone == 5:
        return x, -y 
    elif zone == 6:
        return -x, -y 
    else:
        return y, x


def draw_pixel(x, y, zone):
    x, y = return_back(zone, x, y)
    glVertex2f(x, y)

def draw_line_2(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = -2 * dx - dy
    del_n = -2 * dx
    del_nw = 2 * (- dy - dx)
    draw_pixel(x, y, zone)
    while (y< y1):
        draw_pixel(x, y, zone)
        if (d < 0):
            d += del_n
            y += 1
        else:
            d += del_nw
            x -= 1
            y += 1

def drawLine(x0, y0, x1, y1):
    zone = get_zone(x0, y0, x1, y1)
    dx0, dy0 = allZone_to_2(zone, x0, y0)
    dx1, dy1 = allZone_to_2(zone, x1, y1)
    glBegin(GL_POINTS)
    draw_line_2(dx0, dy0, dx1, dy1, zone)
    glEnd()


def initialize_all_edges(vertices):
    all_edges = []
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        if y1 != y2:
            if y1 < y2:
                ymin, ymax = y1, y2
                x = x1
            else:
                ymin, ymax = y2, y1
                x = x2
            slope_inverse = (x2 - x1) / (y2 - y1)
            all_edges.append(Edge(ymin, ymax, x, slope_inverse, x1, y1, x2, y2))
    return all_edges

def initialize_global_edge_table(all_edges):
    global_edge_table = []
    for edge in all_edges:
        index = 0
        for i, current_edge in enumerate(global_edge_table):
            if edge.ymin < current_edge.ymin:
                break
            elif edge.ymin == current_edge.ymin and edge.x < current_edge.x:
                break
            index += 1
        global_edge_table.insert(index, edge)
    return global_edge_table

def initialize_active_edge_table(scanline, global_edge_table):
    active_edge_table = []
    for edge in global_edge_table:
        if edge.ymin == scanline:
            active_edge_table.append(edge)
        elif edge.ymin > scanline:
            break
    return active_edge_table

def fill_polygon(vertices, color):
    all_edges = initialize_all_edges(vertices)
    global_edge_table = initialize_global_edge_table(all_edges)
    scanline = global_edge_table[0].ymin
    active_edge_table = initialize_active_edge_table(scanline, global_edge_table)
    for edge in active_edge_table:
        global_edge_table.remove(edge)
    glColor3ub(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    while active_edge_table:
        for i in range(0, len(active_edge_table), 2):
            edge1 = active_edge_table[i]
            edge2 = active_edge_table[i + 1]
            x1 = int(edge1.x)
            x2 = int(edge2.x)
            for x in range(x1, x2 + 1):
                glVertex2f(int(x), int(scanline))
        scanline += 1
        active_edge_table = [edge for edge in active_edge_table if edge.ymax != scanline]
        for edge in active_edge_table:
            edge.x += edge.slope_inverse
        add_edges = [edge for edge in global_edge_table if edge.ymin <= scanline]
        if add_edges:
            active_edge_table.extend(add_edges)
            for edge in add_edges:
                global_edge_table.remove(edge)
        remove_edges = [edge for edge in active_edge_table if scanline >= edge.ymax]
        for edge in remove_edges:
            active_edge_table.remove(edge)
        active_edge_table.sort(key=lambda edge: edge.x)
    glEnd()



def rotation_matrix(angle):
    theta = np.radians(angle)
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]])

def rotate_points(points, center, angle):
    points = np.array(points)
    center = np.array(center)
    translated_points = points - center
    rotated_points = np.dot(translated_points, rotation_matrix(angle))
    rotated_points += center
    return rotated_points.tolist()

def calculate_area(vertices):
    area = 0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

def calculate_centroid(vertices):
    area = calculate_area(vertices)
    cx = cy = 0
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        factor = x1 * y2 - x2 * y1
        cx += (x1 + x2) * factor
        cy += (y1 + y2) * factor
    cx /= 6 * area
    cy /= 6 * area
    return (cx, cy)


def drawPolygon(points, mode, color, Window):
    cx, cy = calculate_centroid(points)
    n = len(points)

    if mode == 1:
        glColor3ub(color[0], color[1], color[2])  
        glPointSize(1.0)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            zone = get_zone(x0, y0, x1, y1)
            dx0, dy0 = allZone_to_2(zone, x0, y0)
            dx1, dy1 = allZone_to_2(zone, x1, y1)
            glBegin(GL_POINTS)
            draw_line_2(dx0, dy0, dx1, dy1, zone)
            glEnd()
    elif mode == 0:
        glColor3ub(color[0], color[1], color[2])
        glPointSize(5.0)
        glBegin(GL_POINTS) # White for vertices
        for (x, y) in points:
            glVertex2f(x,y)
        glEnd()

    elif mode == 2:
        fill_polygon(points, color)
    return points

def drawRect(rect, mode, Window):
    rect.points = drawPolygon(rect.points, mode, rect.color, Window)
    return rect 
