import pygame
import sys
import random
from collections import deque
# Constants
CELL_SIZE = 80
GRID_SIZES = [5, 5, 5, 6, 7, 7, 8, 8, 8, 8]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_LINE_COLOR = (100, 100, 100)
COLORS = [
    (255, 0, 0),    
    (0, 255, 0),    
    (0, 128, 255),  
    (255, 165, 0),
    (205, 65, 0), 
    (105, 65, 0), 
    (105, 65, 100), 
    (128, 0, 128)   
]
# Initialize pygame
pygame.init()
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 25)

# Level data
LEVELS = [
    # Level 1 - 5x5
    [
        ((0, 1), (3, 0), 1),
        ((0, 4), (4, 0), 2),
        ((1, 4), (3, 3), 3),
        ((2, 2), (2, 4), 4),
    ],
    # Level 2 - 5x5 
    [
        ((0, 0), (1, 4), 1),
        ((2, 0), (1, 3), 2),
        ((2, 1), (2, 4), 3),
        ((4, 0), (3, 3), 4),
        ((4, 1), (3, 4), 5),
    ],
    # Level 3 - 5x5 
    [
        ((0, 0), (4, 3), 1),
        ((0, 3), (4, 4), 2),
        ((1, 3), (2, 2), 3),
        ((0, 4), (2, 3), 4),
    ],
    # Level 4 - 6x6 
    [
        ((0, 0), (3, 5), 1),
        ((0, 1), (1, 2), 2),
        ((0, 2), (0, 5), 3),
        ((1, 5), (4, 2), 4),
        ((3, 2), (4, 4), 5),
        ((2, 5), (3, 4), 6),
    ],
    # Level 5 - 7x7
    [
        ((0, 0), (1, 6), 1),
        ((1, 0), (4, 3), 2),
        ((2, 0), (3, 2), 3),
        ((1, 2), (2, 4), 4),
        ((1, 3), (6, 6), 5),
        ((5, 1), (4, 4), 6),
    ],

    # Level 6 - 7x7
    [
        ((3, 0), (5, 2), 1),
        ((3, 1), (3, 3), 2),
        ((1, 1), (5, 1), 3),
        ((4, 3), (1, 5), 4),
        ((4, 4), (6, 3), 5),
    ],
    # Level 7 - 8x8
    [
        ((0, 0), (4, 6), 1),
        ((3, 1), (6, 6), 2),
        ((2, 1), (6, 2), 3),
        ((4, 1), (7, 0), 4),
        ((5, 1), (3, 7), 5),
        ((1, 6), (4, 5), 6),
        ((1, 4), (5, 6), 7),
    ],
    # Level 8 - 8x8
    [
        ((1, 0), (0, 7), 1),
        ((2, 0), (1, 1), 2),
        ((2, 1), (3, 2), 3),
        ((3, 3), (6, 5), 4),
        ((5, 2), (5, 4), 5),
        ((1, 3), (1, 7), 6),
        ((5, 5), (6, 4), 7),
    ],
    # Level 9 - 8x8
    [
        ((0, 0), (1, 2), 1),
        ((1, 1), (3, 4), 2),
        ((1, 3), (0, 7), 3),
        ((0, 6), (3, 5), 4),
        ((3, 0), (6, 7), 5),
        ((4, 1), (6, 6), 6),
        ((3, 1), (2, 7), 7),
    ],
    # Level 10 - 8x8
    [
        ((0, 0), (2, 2), 1),
        ((0, 1), (2, 5), 2),
        ((1, 1), (1, 3), 3),
        ((2, 3), (5, 5), 4),
        ((2, 4), (4, 5), 5),
        ((0, 5), (6, 5), 8),
        ((3, 1), (0, 7), 6),
        ((5, 2), (4, 4), 7),
    ],
]

# Game state
current_level = 0
GRID_SIZE = GRID_SIZES[current_level]
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 100  
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
undo_stack = []
current_path = []
selected_color = None
mouse_held = False
last_pos = None
won = False
goal_nodes = set()
solution_paths = None
show_solution = False
auto_solve_in_progress = False
message = None
message_time = 0
connection_complete = False

def load_level(level_index):
    global grid, GRID_SIZE, WIDTH, HEIGHT, screen, undo_stack, selected_color
    global won, goal_nodes, solution_paths, show_solution, auto_solve_in_progress
    global message, message_time, connection_complete, CELL_SIZE
    
    GRID_SIZE = GRID_SIZES[level_index]
    CELL_SIZE = 100 if GRID_SIZE <= 5 else 80
    WIDTH = GRID_SIZE * CELL_SIZE
    HEIGHT = GRID_SIZE * CELL_SIZE + 80
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    undo_stack.clear()
    selected_color = None
    won = False
    goal_nodes = set()
    solution_paths = None
    show_solution = False
    auto_solve_in_progress = False
    message = None
    message_time = 0
    connection_complete = False
    
    # Place the endpoints on the grid
    for (x1, y1), (x2, y2), color_index in LEVELS[level_index]:
        grid[y1][x1] = color_index
        grid[y2][x2] = color_index
        goal_nodes.add((x1, y1))
        goal_nodes.add((x2, y2))

def draw_grid():
    # Draw grid cells
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

    # Draw connections between cells
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            val = grid[y][x]
            if val > 0:
                center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(screen, COLORS[val - 1], center, CELL_SIZE // 4)
                
                # Draw connections to adjacent cells
                for dx, dy in [(1, 0), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == val:
                        neighbor_center = (nx * CELL_SIZE + CELL_SIZE // 2, ny * CELL_SIZE + CELL_SIZE // 2)
                        pygame.draw.line(screen, COLORS[val - 1], center, neighbor_center, CELL_SIZE // 2)

    # Draw endpoints with white borders
    for (x1, y1), (x2, y2), color_index in LEVELS[current_level]:
        for cx, cy in [(x1, y1), (x2, y2)]:
            center = (cx * CELL_SIZE + CELL_SIZE // 2, cy * CELL_SIZE + CELL_SIZE // 2)
            pygame.draw.circle(screen, (255, 255, 255), center, CELL_SIZE // 4 + 5)
            pygame.draw.circle(screen, COLORS[color_index - 1], center, CELL_SIZE // 4)

    # Draw solution paths if enabled
    if show_solution and solution_paths:
        for color_idx, path in solution_paths.items():
            if path:
                for i in range(len(path) - 1):
                    x1, y1 = path[i]
                    x2, y2 = path[i+1]
                    start = (x1 * CELL_SIZE + CELL_SIZE // 2, y1 * CELL_SIZE + CELL_SIZE // 2)
                    end = (x2 * CELL_SIZE + CELL_SIZE // 2, y2 * CELL_SIZE + CELL_SIZE // 2)
                    pygame.draw.line(screen, COLORS[color_idx - 1], start, end, CELL_SIZE // 4)

def draw_level_label():
    label = font.render(f"Level {current_level + 1}", True, WHITE)
    screen.blit(label, (5, HEIGHT - 70))

def is_connected():
    def dfs(x, y, color, visited):
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return
        if visited[y][x] or grid[y][x] != color:
            return
        visited[y][x] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(x + dx, y + dy, color, visited)

    # Check if all color pairs are connected
    for (x1, y1), (x2, y2), color in LEVELS[current_level]:
        visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        dfs(x1, y1, color, visited)
        if not visited[y2][x2]:
            return False
    return True

def display_message(msg, color=(0, 255, 0), duration=1500):
    global message, message_time
    message = (msg, color)
    message_time = pygame.time.get_ticks() + duration

def draw_message():
    if message and pygame.time.get_ticks() < message_time:
        msg, color = message
        text = small_font.render(msg, True, WHITE)
        msg_width = text.get_width() + 30
        msg_height = text.get_height() + 20
        
        msg_x = WIDTH // 2 - msg_width // 2
        msg_y = 10 
        
        # Draw background
        bg_rect = pygame.Rect(msg_x, msg_y, msg_width, msg_height)
        pygame.draw.rect(screen, (40, 40, 40), bg_rect, border_radius=10)
        pygame.draw.rect(screen, color, bg_rect, 2, border_radius=10)
        
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = msg_y + 10
        screen.blit(text, (text_x, text_y))
        
        elapsed = message_time - pygame.time.get_ticks()
        if elapsed < 500:  
            alpha = int(255 * (elapsed / 500))
            fade_surface = pygame.Surface((msg_width, msg_height), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, 255 - alpha))
            screen.blit(fade_surface, (msg_x, msg_y))

def undo_available():
    return len(undo_stack) > 0

def draw_controls():
    # size and color of buttons
    button_style = {
        'color': (70, 70, 70),
        'hover_color': (100, 100, 100),
        'border_color': (150, 150, 150),
        'border_radius': 8,
        'border_width': 2,
        'text_color': WHITE,
        'font': small_font
    }
    
    total_width = GRID_SIZE * CELL_SIZE
    button_width = (total_width - 5 * 10) // 4  
    button_height = 40
    
    margin = 10
    top_margin = HEIGHT - 60

    buttons = []
    button_rects = []
    
    button_defs = [
        ("Undo", (200, 200, 0), undo_available()),
        ("Restart", (0, 200, 0), True),
        ("Solve", (255, 0, 255), not auto_solve_in_progress),
        ("Next", (0, 150, 255), won)
    ]
    
    for i, (text, color, enabled) in enumerate(button_defs):
        btn_x = margin + i * (button_width + margin)
        btn_rect = pygame.Rect(btn_x, top_margin, button_width, button_height)
        button_rects.append(btn_rect)
        
        #btn collor
        btn_color = color if enabled else (100, 100, 60)
        hover = btn_rect.collidepoint(pygame.mouse.get_pos()) and enabled
        if hover:
            btn_color = tuple(min(c + 30, 255) for c in btn_color)
        
        # draw color
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=button_style['border_radius'])
        pygame.draw.rect(screen, button_style['border_color'], btn_rect, 
                        button_style['border_width'], border_radius=button_style['border_radius'])
        
        # btn text
        text_surf = button_style['font'].render(text, True, button_style['text_color'])
        text_rect = text_surf.get_rect(center=btn_rect.center)
        screen.blit(text_surf, text_rect)
    
    return button_rects[1], button_rects[3], button_rects[0], button_rects[2]  # restart, next, undo, solve

def find_solution(max_attempts=50):
    global solution_paths, auto_solve_in_progress
    
    temp_grid = [row[:] for row in grid]
    auto_solve_in_progress = True
    
    # Clear all non-endpoint cells
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) not in goal_nodes:
                temp_grid[y][x] = 0
    
    for attempt in range(max_attempts):
        solution_found = True
        current_solution = {}
        temp_grid_copy = [row[:] for row in temp_grid]
        
        # Randomize color processing order
        color_order = [lev for lev in LEVELS[current_level]]
        random.shuffle(color_order)
        
        for (start, end, color_idx) in color_order:
            start_x, start_y = start
            end_x, end_y = end
            queue = deque()
            queue.append((start_x, start_y, []))
            visited = set()
            visited.add((start_x, start_y))
            found = False
            
            # Randomize directions for each node
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            while queue and not found:
                x, y, path = queue.popleft()
                random.shuffle(directions)
                
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if (nx, ny) == (end_x, end_y):
                            current_solution[color_idx] = path + [(x, y), (nx, ny)]
                            # Mark the path on the temp grid
                            for px, py in current_solution[color_idx]:
                                if (px, py) not in [start, end]:
                                    temp_grid_copy[py][px] = color_idx
                            found = True
                            break
                        
                        if (nx, ny) not in visited and (temp_grid_copy[ny][nx] == 0 or temp_grid_copy[ny][nx] == color_idx):
                            visited.add((nx, ny))
                            queue.append((nx, ny, path + [(x, y)]))
                
                if found:
                    break
            
            if not found:
                solution_found = False
                break
        
        if solution_found:
            solution_paths = current_solution
            auto_solve_in_progress = False
            return solution_paths
    
    auto_solve_in_progress = False
    return None

def apply_solution():
    global grid, undo_stack
    if not solution_paths:
        display_message("No solution found!", (255, 0, 0))
        return
    
    # Save current state for undo
    undo_stack.append([(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if grid[y][x] != 0 and (x, y) not in goal_nodes])
    
    # Clear all non-endpoint cells
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) not in goal_nodes:
                grid[y][x] = 0
    
    # Apply the solution paths
    for color_idx, path in solution_paths.items():
        if path:
            for x, y in path:
                if (x, y) not in goal_nodes:
                    grid[y][x] = color_idx
    
    display_message("Solution Applied!", (0, 200, 0))

# Initialize the first level
load_level(current_level)

# Main game loop
while True:
    screen.fill(BLACK)
    draw_grid()
    draw_level_label()
    restart_btn, next_btn, undo_btn, solve_btn = draw_controls()
    draw_message()

    if won:
        win_text = font.render("You Win!", True, (74, 255, 65))
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = event.pos
                
                # Handle button clicks
                if restart_btn.collidepoint(mx, my):
                    load_level(current_level)
                elif next_btn.collidepoint(mx, my) and won:
                    current_level = (current_level + 1) % len(LEVELS)
                    load_level(current_level)
                elif undo_btn.collidepoint(mx, my) and undo_available():
                    path = undo_stack.pop()
                    for gx, gy in path:
                        if (gx, gy) not in goal_nodes:
                            grid[gy][gx] = 0
                elif solve_btn.collidepoint(mx, my) and not auto_solve_in_progress:
                    solution_paths = find_solution()
                    if solution_paths:
                        apply_solution()
                    else:
                        display_message("No solution found!", (255, 0, 0))
                else:
                    # Handle grid cell clicks
                    grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        val = grid[grid_y][grid_x]
                        if val > 0:
                            selected_color = val
                            mouse_held = True
                            last_pos = (grid_x, grid_y)
                            current_path = []
                            show_solution = False
                            connection_complete = False
                            
                            # Check if we're starting from one of the endpoints
                            for (x1, y1), (x2, y2), color in LEVELS[current_level]:
                                if color == selected_color:
                                    if (grid_x, grid_y) == (x1, y1) or (grid_x, grid_y) == (x2, y2):
                                        connection_complete = False
                                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if current_path and selected_color:
                    # Check if the path connects the endpoints
                    starts_ends = [(x1, y1, x2, y2) for (x1, y1), (x2, y2), c in LEVELS[current_level] if c == selected_color]
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
                            connection_complete = True
                            break
                    else:
                        # Remove the path if it doesn't connect the endpoints
                        for gx, gy in current_path:
                            if (gx, gy) not in goal_nodes:
                                grid[gy][gx] = 0

                mouse_held = False
                current_path = []
                last_pos = None

        elif event.type == pygame.MOUSEMOTION:
            if mouse_held and selected_color and not connection_complete:
                mx, my = event.pos
                grid_x, grid_y = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    if (grid_x, grid_y) not in goal_nodes and grid[grid_y][grid_x] in (0, selected_color):
                        if last_pos and (abs(grid_x - last_pos[0]) + abs(grid_y - last_pos[1]) == 1):
                            grid[grid_y][grid_x] = selected_color
                            current_path.append((grid_x, grid_y))
                            last_pos = (grid_x, grid_y)
                            
                            # Check if we reached the other endpoint
                            starts_ends = [(x1, y1, x2, y2) for (x1, y1), (x2, y2), c in LEVELS[current_level] if c == selected_color]
                            for x1, y1, x2, y2 in starts_ends:
                                if ((grid_x, grid_y) == (x1, y1) and last_pos == (x2, y2)) or \
                                    ((grid_x, grid_y) == (x2, y2) and last_pos == (x1, y1)):
                                    connection_complete = True
                                    break
    # Check if the level is complete
    won = is_connected()
    pygame.display.update()