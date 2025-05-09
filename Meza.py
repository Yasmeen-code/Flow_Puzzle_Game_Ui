import pygame
import sys


selSize = 100
grid_size = [5, 5, 5, 6, 7 , 7 , 8 , 8 , 8 , 8]   
Wite = (0, 0, 0) 
blak = (0, 0, 0)
grid_line_color = (50, 50, 50) 
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 128, 255),
    (255, 165, 0),
    (128, 0, 128)
]

pygame.init()
font = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((500, 600))

# lev = first , end , color num
levels = [
    # Lev 1 - 5x5
    [
        ((0, 0), (4, 0), 1),
        ((0, 4), (4, 4), 2),
        ((2, 1), (2, 3), 3),
        ((1, 2), (3, 2), 4),
    ],
    # Lev 2 - 5x5 
    [
        ((1, 0), (0, 4), 1),  # R
        ((4, 0), (2, 4), 2),  # G
        ((2, 0), (3, 3), 3),  # B
        ((0, 0), (0, 3), 4),  # O
 ] ,


    # Lev 3 - 5x5 
  [
        ((0, 0), (3,3), 1),  # R
        ((0, 4), (2, 2), 2),  # G
        ((2, 4), (4,1), 3),  # B
       ((0, 2), (2, 1), 4),  # O
 ],

    # Lev 4 - 6x6 
    [
        ((0, 0), (3, 3), 1),
        ((0, 1), (5, 4), 2),
        ((2, 0), (1, 2), 3),
        ((4,0), (5, 3), 4),
    ],

    # Lelv 5 - 7x7
    [
        ((2, 4), (5, 1), 1),
        ((4, 2), (5, 4), 2),
        ((1, 0), (6, 6), 3),
        ((3, 1), (6, 5), 4),
    ] , 
[
        ((2, 1), (3, 5), 1),  # R
        ((2, 0), (2, 3), 2),  # G
        ((5, 0), (6, 6), 3),  # B
        ((0, 3), (1, 6), 4),  # O
        ((0, 0), (2, 2), 5),  # P
 ] ,
[
        ((3, 0), (6, 7), 1),  # R
        ((4, 4), (6,6), 2),  # G
        ((4, 0), (7, 0), 3),  # B
        ((1, 0), (2, 5), 4),  # O
        ((2, 7), (6, 2), 5),  # P
 ] ,
[
        ((3, 0), (6, 7), 1),  # R
        ((6, 3), (4,6), 2),  # G
        ((0, 1), (1, 7), 3),  # B
        ((0, 0), (2, 5), 4),  # O
        ((2, 7), (6, 2), 5),  # P
 ] ,

   # Lev 9 - 8x8
    [
        ((2, 1), (7, 5), 1),  # R
        ((2, 2), (5, 3), 2),  # G
        ((3, 3), (7, 7), 3),  # B
        ((3, 5), (5, 6), 4),  # O
        ((0, 7), (7, 0), 5),  # P
    ],
    # Lev 10 - 8x8
    [
        ((1, 0), (6, 1), 1),  # R
        ((2, 2), (5, 2), 2),  # G
        ((3, 3), (0, 6), 3),  # B
        ((3, 5), (5, 6), 4),  # O
        ((1, 7), (7, 0), 5),  # P
    ],

    
]

current_level = 0
GRID_SIZE = grid_size[current_level]
widt = HEIGHT = GRID_SIZE * selSize
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
undo_stack = []
current_path = []
selected_color = None
mouse_held = False
last_pos = None
won = False
goal_nodes = set()

def load_level(level_index):
    global grid, GRID_SIZE, widt, HEIGHT, screen, undo_stack, selected_color, won, goal_nodes
    GRID_SIZE = grid_size[level_index]
    widt = HEIGHT = GRID_SIZE * selSize
    screen = pygame.display.set_mode((widt, HEIGHT + 100))
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    undo_stack.clear()
    selected_color = None
    won = False
    goal_nodes = set()
    for (x1, y1), (x2, y2), color_index in levels[level_index]:
        grid[y1][x1] = color_index
        grid[y2][x2] = color_index
        goal_nodes.add((x1, y1))
        goal_nodes.add((x2, y2))

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * selSize, y * selSize, selSize, selSize)
            pygame.draw.rect(screen, Wite, rect)
            pygame.draw.rect(screen, grid_line_color, rect, 1)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            v = grid[y][x]
            if v > 0:
                center = (x * selSize + selSize // 2, y * selSize + selSize // 2)
                pygame.draw.circle(screen, colors[v - 1], center, selSize // 4)
                for dx, dy in [(1, 0), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == v:
                        neighbor_center = (nx * selSize + selSize // 2, ny * selSize + selSize // 2)
                        pygame.draw.line(screen, colors[v - 1], center, neighbor_center, selSize // 2)

    for (x1, y1), (x2, y2), color_index in levels[current_level]:
        for cx, cy in [(x1, y1), (x2, y2)]:
            center = (cx * selSize + selSize // 2, cy * selSize + selSize // 2)
            pygame.draw.circle(screen, (255, 255, 255), center, selSize // 4 + 5)
            pygame.draw.circle(screen, colors[color_index - 1], center, selSize // 4)

def draw_level_label():
    label = font.render(f"Level {current_level + 1}", True, (255, 255, 255))
    screen.blit(label, (5, HEIGHT + 50))

def is_connected():
    def dfs(x, y, color, visited):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        if visited[y][x] or grid[y][x] != color:
            return
        visited[y][x] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(x + dx, y + dy, color, visited)

    for (x1, y1), (x2, y2), color in levels[current_level]:
        visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        dfs(x1, y1, color, visited)
        if not visited[y2][x2]:
            return False
    return True

def display_win_message():
    win_text = font.render("You Win!", True, (0, 255, 0))
    screen.blit(win_text, (widt // 2 - win_text.get_width() // 2, HEIGHT // 2 - 20))

def draw_controls():
    next_btn = pygame.Rect(widt - 110, HEIGHT + 10, 100, 40)
    pygame.draw.rect(screen, (0, 150, 255) if won else (100, 100, 100), next_btn)
    screen.blit(font.render("Next", True, blak), (widt - 85, HEIGHT + 15))

    restart_btn = pygame.Rect(widt // 2 - 60, HEIGHT + 10, 120, 40)
    pygame.draw.rect(screen, (0, 200, 0), restart_btn)
    screen.blit(font.render("Restart", True, blak), (widt // 2 - 35, HEIGHT + 15))

    undo_btn = pygame.Rect(10, HEIGHT + 10, 100, 40)
    pygame.draw.rect(screen, (200, 200, 0), undo_btn)
    screen.blit(font.render("Undo", True, blak), (30, HEIGHT + 15))

    return restart_btn, next_btn, undo_btn

load_level(current_level)

while True:
    screen.fill(Wite)
    draw_grid()
    draw_level_label()
    restart_btn, next_btn, undo_btn = draw_controls()

    if won:
        display_win_message()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                if restart_btn.collidepoint(mx, my):
                    load_level(current_level)
                elif won and next_btn.collidepoint(mx, my):
                    current_level = (current_level + 1) % len(levels)
                    load_level(current_level)
                elif undo_btn.collidepoint(mx, my):
                    if undo_stack:
                        path = undo_stack.pop()
                        for gx, gy in path:
                            if (gx, gy) not in goal_nodes:
                                grid[gy][gx] = 0
                else:
                    grid_x, grid_y = mx // selSize, my // selSize
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        val = grid[grid_y][grid_x]
                        if val > 0:
                            selected_color = val
                            mouse_held = True
                            last_pos = (grid_x, grid_y)
                            current_path = []

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if current_path and selected_color:
                    starts_ends = [(x1, y1, x2, y2) for (x1, y1), (x2, y2), c in levels[current_level] if c == selected_color]
                    for x1, y1, x2, y2 in starts_ends:
                        visited = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]

                        def dfs(x, y):
                            if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
                                return
                            if visited[y][x] or grid[y][x] != selected_color:
                                return
                            visited[y][x] = True
                            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                                dfs(x+dx, y+dy)

                        dfs(x1, y1)
                        if visited[y2][x2]:
                            undo_stack.append(current_path[:])
                            break
                    else:
                        for gx, gy in current_path:
                            if (gx, gy) not in goal_nodes:
                                grid[gy][gx] = 0

                mouse_held = False
                current_path = []
                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if mouse_held and selected_color:
                mx, my = event.pos
                grid_x, grid_y = mx // selSize, my // selSize
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if (grid_x, grid_y) not in goal_nodes and grid[grid_y][grid_x] in (0, selected_color):
                        if last_pos and (abs(grid_x - last_pos[0]) + abs(grid_y - last_pos[1]) == 1):
                            grid[grid_y][grid_x] = selected_color
                            current_path.append((grid_x, grid_y))
                            last_pos = (grid_x, grid_y)

    won = is_connected()
    pygame.display.update()
