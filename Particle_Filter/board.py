import pygame
import random
import numpy as np

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
        # board = [[0 for _ in range(self.n_cols)] for _ in range(self.n_rows)]
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

    def calculate_distance_to_wall(self, x, y):
        # Calculate distance to the nearest wall in each direction
        xcn = x // self.cell_size
        ycn = y // self.cell_size
        print("x, y", x, y, xcn, ycn)
        return 0, 0, 0, 0

    # def calculate_distance_to_wall(self, x, y):
    #     # Calculate distance to the nearest wall in each direction
    #     up_distance = left_distance = down_distance = right_distance = None

    #     # Check for walls in each direction
    #     for row_offset, col_offset in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
    #         row = y // self.cell_size
    #         col = x // self.cell_size
    #         distance = 0
    #         while 0 <= row < self.n_rows and 0 <= col < self.n_cols and self.board[row][col] == 0:
    #             distance += self.cell_size
    #             row += row_offset
    #             col += col_offset
    #         if row_offset == 0 and col_offset == -1:
    #             left_distance = distance
    #         elif row_offset == -1 and col_offset == 0:
    #             up_distance = distance
    #         elif row_offset == 0 and col_offset == 1:
    #             right_distance = distance
    #         elif row_offset == 1 and col_offset == 0:
    #             down_distance = distance

    #     return up_distance, left_distance, down_distance, right_distance


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
        up_dist, left_dist, down_dist, right_dist = board.calculate_distance_to_wall(x, y)
        print(f"Up: {up_dist}, Left: {left_dist}, Down: {down_dist}, Right: {right_dist}")

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
