import pygame
import sys
from pygame import Vector2
import random


class BIRD:
    def __init__(self):
        self.x = 100
        self.y = 250
        self.image = pygame.image.load('./images/bird.png')

    def draw_bird(self):
        bird_rect = pygame.Rect(self.x, self.y, 100, 100)
        screen.blit(self.image, bird_rect)

    def move_bird(self):
        if self.y <= 0:
            self.y = 0
        else:
            self.y -= 150


class MAIN:
    def __init__(self):
        self.bird = BIRD()

    def draw_elements(self):
        self.bird.draw_bird()

    def update(self):
        if self.bird.y >= 700:
            self.bird.y = 700
        else:
            self.bird.y += 3


pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 20)

main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            main.bird.move_bird()

    screen.fill((255, 255, 255))
    main.draw_elements()
    pygame.display.update()
    clock.tick(144)
