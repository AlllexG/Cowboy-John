import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

level = 1
ROWS = 16
COLS = 150

FPS = 60
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 20

FONT = pygame.font.Font('PixelForce.ttf', 32)

GRAVITY = 0.75

BULLET_IMAGE = pygame.image.load("Images/Objects/bullet.png")
BULLET_COUNT_IMAGE = pygame.image.load("Images/Objects/bullet_count_image.png")

HEART_IMAGE = pygame.image.load("Images/Objects/heart.png")
FULL_HEART_IMAGE = pygame.image.load("Images/Objects/full_heart.png")
HALF_HEART_IMAGE = pygame.image.load("Images/Objects/half_heart.png")
EMPTY_HEART_IMAGE = pygame.image.load("Images/Objects/empty_heart.png")

BG = (236, 217, 149)
RED = (255, 0, 0)

ANIMATION_COOLDOWN = 100

ENEMY_GROUP = pygame.sprite.Group()
BULLET_GROUP = pygame.sprite.Group()
OBJECT_GROUP = pygame.sprite.Group()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))