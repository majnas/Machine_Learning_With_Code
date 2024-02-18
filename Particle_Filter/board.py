import pygame
import random
import numpy as np
from dataclasses import dataclass

@dataclass
class Dictance:
    up: int
    down: int
    left: int
    right: int
    def __str__(self) -> str:
        return f"Up: {self.up}, Left: {self.left}, Down: {self.down}, Right: {self.right}"

class Board():
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.n_cols = width // cell_size
        self.n_rows = height // cell_size
        self.generate_board()
        self.set_board_edges()

    def generate_board(self):
        self.board = np.zeros((self.n_rows, self.n_cols))
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                if random.random() < 0.3:
                    self.board[row, col] = 1

    def set_board_edges(self):
        self.board[[0, -1], :] = 1
        self.board[:, [0, -1]] = 1

    def draw(self, screen):
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                color = (0, 0, 0) if self.board[row, col] == 1 else (255, 255, 255)
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))

    def calculate_distance_to_wall(self, x, y)-> Dictance:
        # Calculate distance to the nearest wall in each direction
        xrem = x % self.cell_size
        yrem = y % self.cell_size

        up = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row][col] == 0:
            row -= 1 
            up += self.cell_size

        left = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row][col] == 0:
            col -= 1 
            left += self.cell_size

        down = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row][col] == 0:
            row += 1 
            down += self.cell_size

        right = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row][col] == 0:
            col += 1 
            right += self.cell_size

        up = up - self.cell_size + yrem
        left = left - self.cell_size + xrem
        down = down - yrem
        right = right - xrem

        return Dictance(up=up, down=down, left=left, right=right)


def main():
    # Constants
    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 20
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Random Maze Generator")
    clock = pygame.time.Clock()

    board = Board(WIDTH, HEIGHT, CELL_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        board.draw(screen)

        # Example usage of calculate_distance_to_wall method
        x, y = pygame.mouse.get_pos()
        distance: Dictance = board.calculate_distance_to_wall(x, y)
        print(distance)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
