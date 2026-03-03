import pygame

WHITE = (255,255,255)

class Laser:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.timer = 6

    def update(self):
        self.timer -= 1

    def draw(self, screen):
        pygame.draw.line(screen, WHITE,
                         (self.start_x, self.start_y),
                         (self.target_x, self.target_y), 3)

    def alive(self):
        return self.timer > 0