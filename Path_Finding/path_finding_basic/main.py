import sys
import pygame
import argparse
from square import Node
from a_star import a_star_algorithm
from typing import List
from icecream import ic
from square import SquareBoard
from hex import HexBoard

def main(win, board):
    board.make_grid()
    start = None
    end = None

    run = True
    started = False

    while run:
        board.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]: # LEFT
                pos = pygame.mouse.get_pos()
                row, col = board.get_clicked_pos(pos)
                node: Node = board.grid[row][col]

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
                row, col = board.get_clicked_pos(pos)
                node: Node = board.grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in board.grid:
                        for node in row:
                            node.update_neighbors(board.grid)

                    a_star_algorithm(lambda: board.draw(win), board.grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    board.make_grid()

    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('shape', choices=['square', 'hex'], default='hex', nargs='?', help="Choose between 'square' or 'hex' (default: 'hex')")
    parser.add_argument('--rows', '-r', type=int, default=20, help='Number of rows')
    parser.add_argument('--cols', '-c', type=int, default=30, help='Number of columns')
    parser.add_argument('--length', '-l', type=int, default=30, help='Length of each cell in board')
    args = parser.parse_args()

    if args.shape == "square":
        board = SquareBoard(rows=args.rows, cols=args.cols, length=args.length)
    elif args.shape == "hex":
        board = HexBoard(rows=args.rows, cols=args.cols, length=args.length)
    else:
        print("Borad shape not supported!")
        sys.exit()

    board.make_grid()

    win = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("A* Path Finding Algorithm Visualization")

    # main(win, board, ROWS, COLS, LENGTH, -1)
    main(win, board)
