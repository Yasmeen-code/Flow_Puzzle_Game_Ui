import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Game settings
GRID_SIZE = 5
CELL_SIZE = 100
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 50
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flow Puzzle")

# Colors and fonts
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
COLORS = [
    (255, 69, 0),     # Orange
    (34, 139, 34),    # Green
    (30, 144, 255),   # Blue
    (218, 165, 32),   # Golden
]
FONT = pygame.font.Font(None, 50)
BUTTON_FONT = pygame.font.Font(None, 40)

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
paths = {}
current_path = []
current_color = None

def get_neighbors(x, y):
    neighbors = []
    if x > 0: neighbors.append((x - 1, y))
    if x < GRID_SIZE - 1: neighbors.append((x + 1, y))
    if y > 0: neighbors.append((x, y - 1))
    if y < GRID_SIZE - 1: neighbors.append((x, y + 1))
    return neighbors

def is_valid_move(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and (grid[x][y] is None or grid[x][y] == current_color) and all((x, y) not in path for path in paths.values())

def place_points():
    global grid
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    available_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
    random.shuffle(available_positions)
    for color in COLORS:
        if not available_positions:
            break
        start = available_positions.pop()
        grid[start[0]][start[1]] = color
        if available_positions:
            end = available_positions.pop()
            grid[end[0]][end[1]] = color
place_points()

def draw_grid():
    SCREEN.fill((240, 240, 240))
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 3)
            if grid[x][y]:
                pygame.draw.circle(SCREEN, grid[x][y], (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
    for path_color, path in paths.items():
        for i in range(1, len(path)):
            pygame.draw.line(SCREEN, path_color, ((path[i-1][0] * CELL_SIZE + CELL_SIZE // 2, path[i-1][1] * CELL_SIZE + CELL_SIZE // 2)), ((path[i][0] * CELL_SIZE + CELL_SIZE // 2, path[i][1] * CELL_SIZE + CELL_SIZE // 2)), 8)
    
    pygame.draw.rect(SCREEN, (0, 150, 200), (WIDTH // 2 - 160, HEIGHT - 50, 150, 40))
    pygame.draw.rect(SCREEN, (200, 50, 50), (WIDTH // 2 + 10, HEIGHT - 50, 150, 40))
    solve_text = BUTTON_FONT.render("Solve", True, WHITE)
    reset_text = BUTTON_FONT.render("Reset", True, WHITE)
    SCREEN.blit(solve_text, (WIDTH // 2 - 135, HEIGHT - 45))
    SCREEN.blit(reset_text, (WIDTH // 2 + 35, HEIGHT - 45))

def check_win():
    return all(color in paths and len(paths[color]) > 1 and grid[paths[color][-1][0]][paths[color][-1][1]] == color for color in COLORS)

def reset_game():
    global paths, current_path, current_color
    paths.clear()
    current_path = []
    current_color = None
    place_points()

running = True
while running:
    draw_grid()
    if check_win():
        text = FONT.render("You Win!", True, (0, 200, 0))
        SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if HEIGHT - 50 <= my <= HEIGHT - 10:
                if WIDTH // 2 - 160 <= mx <= WIDTH // 2 - 10:
                    solve_puzzle()  # Missing function
                elif WIDTH // 2 + 10 <= mx <= WIDTH // 2 + 160:
                    reset_game()
            else:
                gx, gy = mx // CELL_SIZE, my // CELL_SIZE
                if grid[gx][gy]:
                    current_color = grid[gx][gy]
                    current_path = [(gx, gy)]
        elif event.type == pygame.MOUSEMOTION and current_color:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            if is_valid_move(gx, gy) and (gx, gy) not in current_path and (gx, gy) in get_neighbors(*current_path[-1]):
                current_path.append((gx, gy))
                paths[current_color] = current_path[:]
        elif event.type == pygame.MOUSEBUTTONUP:
            if len(current_path) > 1 and grid[current_path[-1][0]][current_path[-1][1]] == current_color:
                paths[current_color] = current_path[:]
            else:
                if current_color in paths:
                    del paths[current_color]
            current_path = []
            current_color = None

pygame.quit()
