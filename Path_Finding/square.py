import pygame
from board import Board
from typing import List, Tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135,206,235)
ORANGE = (255, 165, 0)
GREEN = (0,100,0)
GRAY = (142, 142, 142)
RED = (255, 0, 0)
GOLD = (255,215,0)

class Node:
    def __init__(self, row, col, length, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = col * length
        self.y = row * length
        self.color = GRAY
        self.neighbors: List[Tuple[float, Node]] = []
        self.length = length
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == GOLD

    def is_open(self):
        return self.color == BLUE

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == GREEN

    def reset(self):
        self.color = GRAY

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = GOLD

    def make_open(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.length, self.length))

    def update_neighbors(self, grid: List[List["Node"]]):
        self.neighbors.clear()
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append((1.0, grid[self.row - 1][self.col]))

        if self.row > 0 and self.col < self.total_cols -1 and not grid[self.row - 1][self.col + 1].is_barrier(): # Up-right
            self.neighbors.append((1.41, grid[self.row - 1][self.col + 1]))

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbors.append((1.0, grid[self.row][self.col + 1]))

        if self.row < self.total_rows - 1 and self.col < self.total_cols - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # Down-Right
            self.neighbors.append((1.41, grid[self.row + 1][self.col + 1]))

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Down
            self.neighbors.append((1.0, grid[self.row + 1][self.col]))

        if self.col > 0 and self.row < self.total_rows - 1 and not grid[self.row + 1][self.col - 1].is_barrier(): # Down-Left
            self.neighbors.append((1.41, grid[self.row + 1][self.col - 1]))

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbors.append((1.0, grid[self.row][self.col - 1]))

        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier(): # Up-Left
            self.neighbors.append((1.41, grid[self.row - 1][self.col - 1]))

    def __lt__(self, other):
        return False

    def __str__(self) -> str:
        return f"({self.row, self.col}) xy=({self.x, self.y}, c={self.color})"



class SquareBoard(Board):
    def __init__(self, rows, cols, length) -> None:
        self.rows = rows
        self.cols = cols
        self.length = length
        self.grid: List[List["Node"]] = []
        self.width = cols * length
        self.height = rows * length

    def make_grid(self):
        self.grid: List[List[Node]] = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.cols):
                node: Node = Node(i, j, self.length, self.rows, self.cols)
                self.grid[i].append(node)
    
    def draw_grid(self, win):
        for i in range(self.rows):
            pygame.draw.line(win, BLACK, (0, i * self.length), (self.cols * self.length, i * self.length))

        for j in range(self.cols):
            pygame.draw.line(win, BLACK, (j * self.length, 0), (j * self.length, self.rows * self.length))

    # Draw the grid and its elements
    def draw(self, win):
        win.fill(WHITE)
        for ridx in range(self.rows):
            for cidx in range(self.cols):
                self.grid[ridx][cidx].draw(win)
        self.draw_grid(win)
        pygame.display.update()


    def get_clicked_pos(self, pos):
        x, y = pos
        row = y // self.length
        col = x // self.length
        return row, col

