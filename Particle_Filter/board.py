import pygame
import random
import numpy as np
from dataclasses import dataclass

@dataclass
class Sensors:
    up: int
    down: int
    left: int
    right: int 

    def apply_limit(self, sensor_limit):
        if sensor_limit is not None:
            if self.up > sensor_limit:
                self.up = sensor_limit
            if self.down > sensor_limit:
                self.down = sensor_limit
            if self.left > sensor_limit:
                self.left = sensor_limit
            if self.right > sensor_limit:
                self.right = sensor_limit

    @staticmethod
    def euclidean_distance(x1, x2):
        return np.linalg.norm(np.asarray(x1) - np.asarray(x2))

    def gaussian_distance(self, s2: 'Sensors', std=500):
        distance = Sensors.euclidean_distance((self.up, self.down, self.left, self.right), 
                                              (s2.up, s2.down, s2.left, s2.right))
        return np.exp(-distance ** 2 / (2 * std)) 

    def __str__(self) -> str:
        return f"Up: {self.up}, Left: {self.left}, Down: {self.down}, Right: {self.right}"


class Board():
    def __init__(self, width: int, height: int, cell_size: int):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.n_cols = width // cell_size
        self.n_rows = height // cell_size
        assert self.n_cols > 2, f"Increase width={self.width} or decrease cell_size={self.cell_size}"
        assert self.n_rows > 2, f"Increase height={self.height} or decrease cell_size={self.cell_size}"
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

    def read_sensors(self, x, y)-> Sensors:
        # Calculate sensors to the nearest wall in each direction
        x = int(x)
        y = int(y)

        xrem = x % self.cell_size
        yrem = y % self.cell_size

        up = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row, col] == 0:
            row -= 1 
            up += self.cell_size

        left = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row, col] == 0:
            col -= 1 
            left += self.cell_size

        down = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row, col] == 0:
            row += 1 
            down += self.cell_size

        right = 0
        col = x // self.cell_size
        row = y // self.cell_size
        while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row, col] == 0:
            col += 1 
            right += self.cell_size

        up = up - self.cell_size + yrem
        left = left - self.cell_size + xrem
        down = down - yrem
        right = right - xrem

        return Sensors(up=up, down=down, left=left, right=right)
        
    def __str__(self):
        return f"Board Information:\nWidth: {self.width}\nHeight: {self.height}\nCell Size: {self.cell_size}\nNumber of Rows: {self.n_rows}\nNumber of Columns: {self.n_cols}\n"


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
        sensor: Sensors = board.read_sensors(x, y)
        print(sensor)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
