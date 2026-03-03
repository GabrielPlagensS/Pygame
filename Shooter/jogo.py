import pygame
import random

from palavra import Word
from projetil import Laser
from carregadorcsv import load_words
from util import select_word_by_level, get_spawn_x, calculate_difficulty

WIDTH = 900
HEIGHT = 600
GROUND_Y = HEIGHT - 80

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (200,200,200)
RED = (220,50,50)
YELLOW = (255,255,0)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Word Shooter")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 28)
        self.hud_font = pygame.font.SysFont("arial", 22)

        self.words_data = load_words()

        self.language = None
        self.menu = True

        self.reset()

    def reset(self):
        self.words = []
        self.lasers = []
        self.score = 0
        self.combo = 0
        self.lives = 3
        self.level = 1
        self.spawn_timer = 0
        self.base_speed, self.max_words, self.spawn_delay = calculate_difficulty(self.level)
        self.game_over = False

    # =============================
    # SPAWN
    # =============================

    def spawn_word(self):
        if len(self.words) >= self.max_words:
            return

        text = select_word_by_level(self.words_data, self.level, self.language)

        if not text:
            return

        x = get_spawn_x(self.words, WIDTH)

        word = Word(text, self.level, x)
        word.speed = self.base_speed

        self.words.append(word)

    # =============================
    # INPUT
    # =============================

    def handle_input(self, event):
        if not self.words:
            return

        # Mira inteligente (mais próxima do chão)
        target = max(self.words, key=lambda w: w.y)

        if event.unicode.lower() == target.text[0].lower():

            laser = Laser(WIDTH//2, GROUND_Y, target.x, target.y)
            self.lasers.append(laser)

            target.remove_letter()

            self.combo += 1
            self.score += 10 + (self.combo * 2)

            if target.is_empty():
                if len(target.original) >= 7:
                    self.score += 20
                self.words.remove(target)

        else:
            self.combo = 0
            for w in self.words:
                w.speed += 1  # penalidade mais forte

    # =============================
    # UPDATE
    # =============================

    def update(self):
        if self.game_over:
            return

        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_word()

        for word in self.words[:]:
            word.update()

            if word.hit_ground(GROUND_Y):
                self.words.remove(word)
                self.lives -= 1

                if self.lives <= 0:
                    self.game_over = True

        for laser in self.lasers[:]:
            laser.update()
            if not laser.alive():
                self.lasers.remove(laser)

        # Progressão de nível
        if self.score >= self.level * 100:
            self.level += 1
            self.base_speed, self.max_words, self.spawn_delay = calculate_difficulty(self.level)

            # Atualiza velocidade das palavras existentes
            for word in self.words:
                word.speed = self.base_speed

    # =============================
    # MENU
    # =============================

    def draw_menu(self):
        self.screen.fill(BLACK)

        title = self.font.render("WORD SHOOTER", True, WHITE)
        pt = self.hud_font.render("Pressione 1 - PT-BR", True, WHITE)
        en = self.hud_font.render("Pressione 2 - EN", True, WHITE)

        self.screen.blit(title, (350,200))
        self.screen.blit(pt, (360,300))
        self.screen.blit(en, (360,340))

        pygame.display.flip()

    # =============================
    # DRAW
    # =============================

    def draw(self):
        self.screen.fill(BLACK)

        pygame.draw.rect(self.screen, GRAY, (0, GROUND_Y, WIDTH, 80))
        pygame.draw.rect(self.screen, WHITE, (WIDTH//2 - 20, GROUND_Y - 40, 40, 40))

        for word in self.words:
            word.draw(self.screen, self.font)

        for laser in self.lasers:
            laser.draw(self.screen)

        hud = self.hud_font.render(
            f"Pontos: {self.score}  Vidas: {self.lives}  Nivel: {self.level}",
            True, WHITE)

        combo = self.hud_font.render(f"Combo: {self.combo}", True, YELLOW)

        self.screen.blit(hud, (20,20))
        self.screen.blit(combo, (20,50))

        if self.game_over:
            text = self.font.render("GAME OVER - R para reiniciar", True, RED)
            self.screen.blit(text, (WIDTH//2 - 220, HEIGHT//2))

        pygame.display.flip()

    # =============================
    # LOOP PRINCIPAL
    # =============================

    def run(self):
        running = True

        while running:
            self.clock.tick(60)

            if self.menu:
                self.draw_menu()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.language = "pt"
                            self.menu = False
                        if event.key == pygame.K_2:
                            self.language = "en"
                            self.menu = False

                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.reset()
                    else:
                        self.handle_input(event)

            self.update()
            self.draw()

        pygame.quit()