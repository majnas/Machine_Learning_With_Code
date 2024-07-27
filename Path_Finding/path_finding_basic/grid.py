import pygame, math
from icecream import ic

HEX_LEN = 30
HEX_SIN_LEN = math.sin(math.radians(60)) * HEX_LEN
HEX_COS_LEN = math.cos(math.radians(60)) * HEX_LEN
HEX_POINTS = [(HEX_LEN, 0), 
              (HEX_LEN-HEX_COS_LEN, HEX_SIN_LEN), 
              (HEX_COS_LEN-HEX_LEN, HEX_SIN_LEN),
              (-HEX_LEN, 0), 
              (HEX_COS_LEN-HEX_LEN, -HEX_SIN_LEN), 
              (HEX_LEN-HEX_COS_LEN, -HEX_SIN_LEN)]

class Hexagonal:
    def __init__(self, row, col, hex_len, total_rows) -> None:
        self.row = row
        self.col = col
        self.total_rows = total_rows

        if col % 2 == 0:
            self.x = hex_len + (col // 2) * 3 * hex_len
            self.y = (2 * row + 1) * HEX_SIN_LEN
        else:
            self.x = HEX_COS_LEN + 2 * hex_len + (col // 2) * 3 * hex_len
            self.y = 2 * (row + 1) * HEX_SIN_LEN

        self.points = [(x + self.x, y + self.y) for x, y in HEX_POINTS]
        self.tiel_rect = pygame.Rect(0, 0, HEX_LEN * 2, HEX_SIN_LEN * 2)
        self.tiel_rect.center = (self.x, self.y)
        self.color = "white"
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        for i in range(len(self.points)):
            pygame.draw.line(screen, (0, 0, 0), self.points[i], self.points[(i + 1) % len(self.points)], 5)

    def __str__(self) -> str:
        return f"({self.row, self.col}) xy=({self.x, self.y})"



class Board:
    def __init__(self, rows, cols, len) -> None:
        self.rows = rows
        self.cols = cols

    def make_grid(self):
        grid = []
        for row in range(self.rows):
            for col in range(self.cols):
                grid.append(Hexagonal(row, col, len, 1))


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
    board = Board(rows=ROWS, cols=COLS, len=HEX_LEN)
    grid = board.make_grid()

    while run:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # color = "white"
        # if collideHexagon(hex.tiel_rect, pygame.mouse.get_pos()):
        #     color = "red"
    
        screen.fill(0)
        # pygame.draw.polygon(screen, color, hex.points)         
        for hex in grid:
            hex.draw(screen)
        pygame.display.flip() 

    pygame.quit()
    exit()