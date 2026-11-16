import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja - Week 1: Setup & Blade")
clock = pygame.time.Clock()

# Colors
COLOR_BG_DARK = (45, 30, 20)
COLOR_BG_LIGHT = (70, 50, 35)
BLADE_COLOR = (220, 240, 255)

blade_trail = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            blade_trail.append((pygame.mouse.get_pos(), pygame.time.get_ticks()))

    # Remove old trail points (after 150ms)
    now = pygame.time.get_ticks()
    blade_trail = [pt for pt in blade_trail if now - pt[1] < 150]

    # Render Background
    screen.fill(COLOR_BG_DARK)
    for x in range(0, WIDTH, 120):
        pygame.draw.line(screen, COLOR_BG_LIGHT, (x, 0), (x, HEIGHT), 3)

    # Render Blade Trail
    if len(blade_trail) > 1:
        points = [pt[0] for pt in blade_trail]
        for i in range(len(points) - 1):
            thickness = int(max(2, 10 * (i / len(points))))
            pygame.draw.line(screen, BLADE_COLOR, points[i], points[i+1], thickness)

    pygame.display.flip()
    clock.tick(60)