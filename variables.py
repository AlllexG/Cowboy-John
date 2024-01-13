import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

FPS = 60
TILE_SIZE = 40

FONT = pygame.font.Font('PixelForce.ttf', 32)

GRAVITY = 0.75

BULLET_IMAGE = pygame.image.load("Images/Objects/bullet.png")
BULLET_COUNT_IMAGE = pygame.image.load("Images/Objects/bullet_count_image.png")
HEART_IMAGE = pygame.image.load("Images/Objects/heart.png")

BG = (236, 217, 149)
RED = (255, 0, 0)

ANIMATION_COOLDOWN = 100