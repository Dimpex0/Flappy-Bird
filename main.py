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
        self.jumping = False
        self.max_jump = 120

    def draw_bird(self):
        self.bird_rect = pygame.Rect(self.x, self.y, 92, 70)
        screen.blit(self.image, self.bird_rect)

    def move_bird(self):
        if self.jumping:
            if self.max_jump > 0:
                self.max_jump -= 3
                self.y -= 3
            else:
                self.jumping = False
                self.max_jump = 120
                self.y += 2


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
        return random.randint(100, 500)

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
        screen.blit(city_image, (0, 0))
        self.bird.draw_bird()
        for pipes in self.pipes:
            pipes[0].draw_pipe()
            pipes[1].draw_pipe()
        self.draw_poins()

    def make_pipes(self):
        pipe_up = PIPE()
        pipe_down = PIPE()
        pipe_down.height = 600 - pipe_up.height
        pipe_down.y = 800 - pipe_down.height
        self.pipes.append((pipe_up, pipe_down))

    def update(self):
        self.bird.move_bird()
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
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (255, 255, 255))
        score_x = 900
        score_y = 700
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        pipe_rect = pipe.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(pipe_rect.left, pipe_rect.top, pipe_rect.width + score_rect.width + 20,
                              pipe_rect.height)

        pygame.draw.rect(screen, (128,128,128), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(pipe, pipe_rect)
        pygame.draw.rect(screen, (105,105,105), bg_rect, 2)

    def end_game(self):
        pygame.quit()
        sys.exit()




pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

city_image = pygame.image.load('./images/city_background.jpg').convert_alpha()

PIPE_SPAWN = pygame.USEREVENT
pygame.time.set_timer(PIPE_SPAWN, 3000)

pipe = pygame.image.load('./images/pipe_small.png').convert_alpha()
game_font = pygame.font.Font('./Font/PoetsenOne-Regular.ttf', 40)

main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == PIPE_SPAWN:
            main.make_pipes()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                main.bird.jumping = True

    main.update()
    main.draw_elements()
    pygame.display.update()
    clock.tick(144)
