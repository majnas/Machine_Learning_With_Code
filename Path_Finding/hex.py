import pygame, math
from board import Board
from shapely.geometry import Point, Polygon
from typing import List, Tuple
from icecream import ic

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
YELLOW = (255, 211, 0)
GRAY = (142, 142, 142)


class Node:
    def __init__(self, row, col, length, hex_sin_len, hex_cos_len, hex_polygon, total_rows, total_cols) -> None:
        self.row = row
        self.col = col
        self.length = length
        self.color = GRAY
        self.neighbors: List[Tuple[float, Node]] = []
        self.total_rows = total_rows
        self.total_cols = total_cols

        if col % 2 == 0:
            self.x = length + (col // 2) * 3 * length
            self.y = (2 * row + 1) * hex_sin_len
        else:
            self.x = hex_cos_len + 2 * length + (col // 2) * 3 * length
            self.y = 2 * (row + 1) * hex_sin_len

        self.points = [(x + self.x, y + self.y) for x, y in hex_polygon]

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = GRAY

    def is_highlight(self):
        return self.color == YELLOW

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.points)

    def update_neighbors(self, grid: List[List["Node"]]):
        self.neighbors.clear()

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append((1.0, grid[self.row - 1][self.col]))

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append((1.0, grid[self.row + 1][self.col]))

        if self.col % 2 == 0:
            if self.row > 0 and self.col < self.total_cols - 1 and not grid[self.row - 1][self.col + 1].is_barrier(): # Up-Right
                self.neighbors.append((1.0, grid[self.row - 1][self.col + 1]))

            if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # Down-Right
                self.neighbors.append((1.0, grid[self.row ][self.col + 1]))

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Down-Left
                self.neighbors.append((1.0, grid[self.row][self.col - 1]))

            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # Up-Left
                self.neighbors.append((1.0, grid[self.row - 1][self.col - 1]))
        else:        
            if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # Up-Right
                self.neighbors.append((1.0, grid[self.row][self.col + 1]))

            if self.row < self.total_rows - 1 and self.col < self.total_cols - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # Down-Right
                self.neighbors.append((1.0, grid[self.row + 1][self.col + 1]))

            if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): # Down-Left
                self.neighbors.append((1.0, grid[self.row + 1][self.col - 1]))

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Up-Left
                self.neighbors.append((1.0, grid[self.row][self.col - 1]))


    def __str__(self) -> str:
        return f"({self.row, self.col}) xy=({self.x, self.y}, c={self.color})"



class HexBoard(Board):
    def __init__(self, rows, cols, length) -> None:
        self.rows = rows
        self.cols = cols
        self.length = length
        self.grid: List[List["Node"]] = []
        self.width = None
        self.height = None

    def make_grid(self):
        hex_sin_len = math.sin(math.radians(60)) * self.length
        hex_cos_len = math.cos(math.radians(60)) * self.length
        hex_polygon = [(self.length, 0), 
                      (self.length - hex_cos_len, hex_sin_len), 
                      (hex_cos_len - self.length, hex_sin_len),
                      (-self.length, 0), 
                      (hex_cos_len - self.length, -hex_sin_len), 
                      (self.length - hex_cos_len, -hex_sin_len)]

        self.grid = []
        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                self.grid[row].append(Node(row, col, self.length, hex_sin_len, hex_cos_len, hex_polygon, self.rows, self.cols))

        # update width and height
        self.width = (self.cols // 2) * 3 * self.length + (hex_cos_len if self.cols % 2 == 0 else 2 * self.length)
        self.height = (2 * self.rows + 1 ) * hex_sin_len

    def draw_grid(self, win):
        for row in self.grid:
            for node in row:
                for i in range(len(node.points)):
                    pygame.draw.line(win, BLACK, node.points[i], node.points[(i + 1) % len(node.points)], 2)

    def draw(self, win):
        win.fill(WHITE)
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                self.grid[ridx][cidx].draw(win)
        self.draw_grid(win)
        pygame.display.update()


    def get_clicked_pos(self, pos):
        point = Point(pos)
        for row in self.grid:
            for node in row:
                polygon = Polygon(node.points)
                is_inside = polygon.contains(point)
                if is_inside:
                    return node.row, node.col
        return None