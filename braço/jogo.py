import pygame
import math

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Braço Robótico 2D")

clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (150, 150, 150)
YELLOW = (200, 200, 0)
BLUE = (0, 0, 255)

# Base
base_x = WIDTH // 2
base_y = HEIGHT // 2 + 100

# Ângulos
angle1 = 0
angle2 = 0

# Tamanhos
arm1_length = 120
arm2_length = 100

def rotate_point(x, y, angle):
    rad = math.radians(angle)
    new_x = x * math.cos(rad) - y * math.sin(rad)
    new_y = x * math.sin(rad) + y * math.cos(rad)
    return new_x, new_y

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movimento da base
    if keys[pygame.K_a]:
        base_x -= 3
    if keys[pygame.K_d]:
        base_x += 3

    # Rotação braço 1
    if keys[pygame.K_q]:
        angle1 -= 2
    if keys[pygame.K_e]:
        angle1 += 2

    # Rotação braço 2
    if keys[pygame.K_z]:
        angle2 -= 2
    if keys[pygame.K_c]:
        angle2 += 2

    # Base
    base_width = 130
    base_height = 140

    pygame.draw.rect(
        screen,
        RED,
        (base_x - base_width // 2, base_y - base_height, base_width, base_height)
    )

    # Braço 1
    arm1_end_x, arm1_end_y = rotate_point(arm1_length, 0, angle1)
    arm1_end_x += base_x
    arm1_end_y += base_y - 80

    pygame.draw.line(screen, GRAY, (base_x, base_y - 80), (arm1_end_x, arm1_end_y), 8)

    # Braço 2 (depende do braço 1)
    arm2_end_x, arm2_end_y = rotate_point(arm2_length, 0, angle1 + angle2)
    arm2_end_x += arm1_end_x
    arm2_end_y += arm1_end_y

    pygame.draw.line(screen, YELLOW, (arm1_end_x, arm1_end_y), (arm2_end_x, arm2_end_y), 8)

    # Junta (pontos)
    pygame.draw.circle(screen, BLACK, (int(base_x), int(base_y - 80)), 6)
    pygame.draw.circle(screen, BLUE, (int(arm1_end_x), int(arm1_end_y)), 6)

    pygame.display.flip()

pygame.quit()