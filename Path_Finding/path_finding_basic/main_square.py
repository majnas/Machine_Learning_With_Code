import pygame
from grid_org import Node
from a_star import a_star_algorithm
from typing import List
from icecream import ic
from grid_org import Board


def main(win, board, rows, width):
    grid: List[List[Node]]  = board.make_grid(rows, width)
    start = None
    end = None

    run = True
    started = False

    while run:
        board.draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_pos(pos, rows, width)
                node: Node = grid[row][col]

                # set start
                if not start and node != end:
                    start = node
                    start.make_start()

                # set end
                elif not end and node != start:
                    end = node
                    end.make_end()

                # set barrier
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_pos(pos, rows, width)
                node: Node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    a_star_algorithm(lambda: board.draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = board.make_grid(rows, width)

    pygame.quit()


if __name__ == "__main__":
    ROWS = 20
    COLS = 20
    LENGTH = 30

    WIDTH = LENGTH * COLS
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("A* Path Finding Algorithm Visualization")

    board = Board(rows=ROWS, cols=COLS, length=LENGTH)
    board.make_grid(rows=ROWS, width=COLS*LENGTH)

    # win = pygame.display.set_mode((board.width, board.height))
    # pygame.display.set_caption("A* Path Finding Algorithm Visualization")

    # main(win, board, ROWS, COLS, LENGTH, -1)
    main(WIN, board, ROWS, WIDTH)
