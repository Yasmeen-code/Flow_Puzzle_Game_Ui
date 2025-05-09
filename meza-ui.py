import pygame
import sys


selSize = 100
grid_size = [5, 5, 5, 6, 7]  
Wite = (255, 255, 255)
blak = (0, 0, 0)
colors = [(255, 0, 0), 
          (0, 255, 0), 
          (0, 128, 255), 
          (255, 165, 0), 
          (128, 0, 128)
        ]  # red, green, blue, orange, purple

pygame.init()
font = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((500, 500)) 


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
    ]
]


current_level = 0
GRID_SIZE = grid_size[current_level]
widt = HEIGHT = GRID_SIZE * selSize
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def load_level(level_index):
    global grid, GRID_SIZE, widt, HEIGHT, screen
    GRID_SIZE = grid_size[level_index]
    widt = HEIGHT = GRID_SIZE * selSize
    screen = pygame.display.set_mode((widt, HEIGHT))
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for (x1, y1), (x2, y2), color_index in levels[level_index]:
        grid[y1][x1] = color_index
        grid[y2][x2] = color_index

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * selSize, y * selSize, selSize, selSize)
            v = grid[y][x]
            if v > 0:
                pygame.draw.rect(screen, colors[v - 1], rect)
            else:
                pygame.draw.rect(screen, Wite, rect)
            pygame.draw.rect(screen, blak, rect, 2)

    for (x1, y1), (x2, y2), color_index in levels[current_level]:
        for cx, cy in [(x1, y1), (x2, y2)]:
            center = (cx * selSize + selSize // 2, cy * selSize + selSize // 2)
            pygame.draw.circle(screen, colors[color_index - 1], center, selSize // 4)

def main():
    global current_level
    clock = pygame.time.Clock()
    load_level(current_level)

    while True:
        screen.fill(Wite)
        draw_grid()

        # Draw level text
        level_text = font.render(f"Level S {current_level + 1}", True, blak)
        screen.blit(level_text, (10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_level = (current_level + 1) % len(levels)
                    load_level(current_level)

        clock.tick(60)

main()
