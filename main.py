import pygame
import sys
from pygame import Vector2
import random


class BIRD:
    def __init__(self):
        self.x = 100
        self.y = 250
        self.image = pygame.image.load('./images/bird.png').convert_alpha()
        self.bird_rect = None

    def draw_bird(self):
        self.bird_rect = pygame.Rect(self.x, self.y, 70, 70)
        screen.blit(self.image, self.bird_rect)

    def move_bird(self):
        if self.y <= 0:
            self.y = 0
        else:
            self.y -= 100

    def get_rect(self):
        return self.bird_rect


class PIPE:
    def __init__(self):
        self.x = 1000
        self.y = 0
        self.height = self.get_random_height()
        self.pipe_rect = None

    def draw_pipe(self):
        self.pipe_rect = pygame.Rect(self.x, self.y, 150, self.height)
        pygame.draw.rect(screen, pygame.Color('green'), self.pipe_rect)

    def get_random_height(self):
        return random.randint(100, 300)

    def move_pipe(self):
        self.x -= 1

    def get_rect(self):
        self.draw_pipe()
        return self.pipe_rect


class MAIN:
    def __init__(self):
        self.bird = BIRD()
        self.pipes = []
        self.score = 0

    def draw_elements(self):
        self.bird.draw_bird()
        for pipes in self.pipes:
            pipes[0].draw_pipe()
            pipes[1].draw_pipe()
        self.draw_poins()

    def make_pipes(self):
        pipe_up = PIPE()
        pipe_down = PIPE()
        pipe_down.y = 800 - pipe_down.height
        self.pipes.append((pipe_up, pipe_down))

    def update(self):
        if self.bird.y >= 700:
            self.bird.y = 700
        else:
            self.bird.y += 1

        for pipes in self.pipes:
            pipes[0].move_pipe()
            pipes[1].move_pipe()

        self.check_collision()
        self.check_for_point()

    def check_collision(self):
        for pipes in self.pipes:
            if pygame.Rect.colliderect(pipes[0].get_rect(), self.bird.get_rect()) or \
                    pygame.Rect.colliderect(pipes[1].get_rect(), self.bird.get_rect()):
                self.end_game()

    def check_for_point(self):
        for pipe_up, pipe_down in self.pipes:
            if pipe_up.x + 150 < self.bird.x:
                self.pipes = self.pipes[1:]
                self.score += 1

    def draw_poins(self):
        points_rect = pygame.Rect(900, 700, 60, 60)
        pygame.draw.rect(screen, (167, 150, 67), points_rect)

    def end_game(self):
        pygame.quit()
        sys.exit()




pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

city_image = pygame.image.load('./images/city_background.jpg').convert_alpha()

PIPE_SPAWN = pygame.USEREVENT
pygame.time.set_timer(PIPE_SPAWN, 2000)

main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PIPE_SPAWN:
            main.make_pipes()
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                main.bird.move_bird()

    screen.blit(city_image, (0, 0))
    main.draw_elements()
    main.update()
    pygame.display.update()
    clock.tick(144)
