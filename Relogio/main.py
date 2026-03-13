import pygame
import math
import datetime

# Inicialização
pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relógio Analógico")

clock = pygame.time.Clock()

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 200

font = pygame.font.SysFont("Arial", 24)

def draw_numbers():
    for num in range(1, 13):
        angle = math.radians((num * 30) - 90)

        x = CENTER[0] + math.cos(angle) * (RADIUS - 30)
        y = CENTER[1] + math.sin(angle) * (RADIUS - 30)

        text = font.render(str(num), True, (255,255,255))
        rect = text.get_rect(center=(x,y))
        screen.blit(text, rect)

def draw_hand(angle, length, color, width):
    x = CENTER[0] + math.cos(angle) * length
    y = CENTER[1] + math.sin(angle) * length

    pygame.draw.line(screen, color, CENTER, (x,y), width)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30,30,30))

    #círculo do relógio
    pygame.draw.circle(screen, (200,200,200), CENTER, RADIUS, 4)

    #números
    draw_numbers()

    # Hora do sistema
    now = datetime.datetime.now()

    second = now.second
    minute = now.minute
    hour = now.hour % 12

    # ângulos
    second_angle = math.radians((second * 6) - 90)
    minute_angle = math.radians((minute * 6) - 90)
    hour_angle = math.radians((hour * 30 + minute * 0.5) - 90)

    #ponteiros
    draw_hand(second_angle, RADIUS-20, (255,0,0), 2)   # segundos vermelho
    draw_hand(minute_angle, RADIUS-40, (0,0,255), 4)   # minutos azul
    draw_hand(hour_angle, RADIUS-70, (0,255,0), 6)     # horas verde

    pygame.display.flip()
    clock.tick(60)

pygame.quit()