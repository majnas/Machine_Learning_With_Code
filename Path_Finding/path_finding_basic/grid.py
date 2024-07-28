import pygame, math
from typing import List
from icecream import ic

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)



class HexNode:
    def __init__(self, row, col, hex_len, hex_sin_len, hex_cos_len, hex_polygon, total_rows, total_cols) -> None:
        self.row = row
        self.col = col
        self.hex_len = hex_len
        self.neighbors = []
        self.total_rows = total_rows
        self.total_cols = total_cols

        if col % 2 == 0:
            self.x = hex_len + (col // 2) * 3 * hex_len
            self.y = (2 * row + 1) * hex_sin_len
        else:
            self.x = hex_cos_len + 2 * hex_len + (col // 2) * 3 * hex_len
            self.y = 2 * (row + 1) * hex_sin_len

        self.points = [(x + self.x, y + self.y) for x, y in hex_polygon]
        self.tiel_rect = pygame.Rect(0, 0, hex_len * 2, hex_sin_len * 2)
        self.tiel_rect.center = (self.x, self.y)
        self.color = "gray"

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

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        for i in range(len(self.points)):
            pygame.draw.line(screen, (0, 0, 0), self.points[i], self.points[(i + 1) % len(self.points)], 5)


    def update_neighbors(self, grid: List[List["HexNode"]]):
        self.neighbors: List[HexNode] = []

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Up-Left
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): # Up-Right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_barrier(): # Bottom-Left
            self.neighbors.append(grid[self.row + 1][self.col - 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Bottom
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row < self.total_rows - 1 and self.col < self.total_cols - 1 and not grid[self.row + 1][self.col + 1].is_barrier(): # Bottom-Right
            self.neighbors.append(grid[self.row + 1][self.col + 1])

    def __str__(self) -> str:
        return f"({self.row, self.col}) xy=({self.x, self.y})"



class Board:
    def __init__(self, rows, cols, length) -> None:
        self.rows = rows
        self.cols = cols
        self.length = length
        self.grid = []
        self.width = 100
        self.height = 100

    def make_hex_grid(self):
        hex_sin_len = math.sin(math.radians(60)) * self.length
        hex_cos_len = math.cos(math.radians(60)) * self.length
        hex_polygon = [(self.length, 0), 
                      (self.length - hex_cos_len, hex_sin_len), 
                      (hex_cos_len - self.length, hex_sin_len),
                      (-self.length, 0), 
                      (hex_cos_len - self.length, -hex_sin_len), 
                      (self.length - hex_cos_len, -hex_sin_len)]

        for row in range(self.rows):
            self.grid.append([])
            for col in range(self.cols):
                self.grid[row].append(HexNode(row, col, self.length, hex_sin_len, hex_cos_len, hex_polygon, self.rows, self.cols))

        # update width and height
        self.width = (self.cols // 2) * 3 * self.length + (hex_cos_len if self.cols % 2 == 0 else 2 * self.length)
        self.height = (2 * self.rows + 1 ) * hex_sin_len



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    def collideHexagon(bounding_rect, position):
        px, py = position
        if bounding_rect.collidepoint((px, py)):
            dx = min(px - bounding_rect.left, bounding_rect.right - px)
            dy = abs(py - bounding_rect.centery)
            if dy < dx * math.tan(math.radians(60)):
                return True
        return False

    run = True
    ROWS = 5
    COLS = 10
    board = Board(rows=ROWS, cols=COLS, length=HEX_LEN)
    board.make_hex_grid()

    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # color = "white"
        # if collideHexagon(hex.tiel_rect, pygame.mouse.get_pos()):
        #     color = "red"
    
        screen.fill(0)
        for row in board.grid:
            for node in row:
                node.draw(screen)
        pygame.display.flip() 

    pygame.quit()
    exit()