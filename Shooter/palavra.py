import pygame
import random

WHITE = (255,255,255)
RED = (220,50,50)
BLUE = (50,120,255)

class Word:
    def __init__(self, text, level, x):
        self.original = text
        self.text = text
        self.x = x
        self.y = 0
        self.speed = 1 + level * 0.4
        self.color = random.choice([RED, BLUE])
        self.width = 0
        self.height = 0

    def update(self):
        self.y += self.speed

    def draw(self, screen, font):
        surface = font.render(self.text, True, WHITE)
        self.width = surface.get_width() + 20
        self.height = surface.get_height() + 10

        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        screen.blit(surface, (self.x + 10, self.y + 5))

    def remove_letter(self):
        self.text = self.text[1:]

    def is_empty(self):
        return len(self.text) == 0

    def hit_ground(self, ground_y):
        return self.y + self.height >= ground_y