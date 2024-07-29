import pygame
from node import Node
from typing import List
from icecream import ic

WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# def make_grid(rows: int, width: int):
#     grid: List[List[Node]] = []
#     gap = width // rows
#     for i in range(rows):
#         grid.append([])
#         for j in range(rows):
#             node: Node = Node(i, j, gap, rows)
#             grid[i].append(node)
#     return grid
    

# def draw_grid(win, rows: int, width: int):
#     gap = width // rows
#     for i in range(rows):
#         pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
#         for j in range(rows):
#             pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# def get_clicked_pos(pos, rows: int, width: int):
#     ic(pos)
#     gap = width // rows
#     y, x = pos
#     row = y // gap
#     col = x // gap
#     return row, col
