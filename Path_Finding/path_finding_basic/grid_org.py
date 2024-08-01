import pygame
from typing import List

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

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
        self.color = WHITE

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: List[List["Node"]]):
        self.neighbors: List[Node] = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

    def __str__(self):
        return f"({self.row}, {self.col})"



class Board:
    def __init__(self, rows, cols, length) -> None:
        self.rows = rows
        self.cols = cols
        self.length = length
        self.grid: List[List["Node"]] = []
        self.width = 100
        self.height = 100


    def make_grid(self, rows: int, width: int):
        grid: List[List[Node]] = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                node: Node = Node(i, j, gap, rows)
                grid[i].append(node)
        return grid
    
    def draw_grid(self, win, rows: int, width: int):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


    # Draw the grid and its elements
    def draw(self, win, grid, rows, width):
        win.fill(WHITE)

        for row in grid:
            for node in row:
                node.draw(win)

        self.draw_grid(win, rows, width)
        pygame.display.update()


    def get_clicked_pos(self, pos, rows: int, width: int):
        gap = width // rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col

