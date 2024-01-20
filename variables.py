import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

level = 1
ROWS = 16
COLS = 500

FPS = 60
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 20

SCROLL_THRESH = 200
SCREEN_SCROLL = 0
BACKGROUND_SCROLL = 0 

FONT = pygame.font.Font('PixelForce.ttf', 32)

GRAVITY = 0.75

BULLET_IMAGE = pygame.image.load("Images/Objects/bullet.png")
BULLET_COUNT_IMAGE = pygame.image.load("Images/Objects/bullet_count_image.png")

HEART_IMAGE = pygame.image.load("Images/Objects/heart.png")
FULL_HEART_IMAGE = pygame.image.load("Images/Objects/full_heart.png")
HALF_HEART_IMAGE = pygame.image.load("Images/Objects/half_heart.png")
EMPTY_HEART_IMAGE = pygame.image.load("Images/Objects/empty_heart.png")

SAND_1_IMAGE = pygame.image.load("Images/Background/sand1.png")
SAND_2_IMAGE = pygame.image.load("Images/Background/sand2.png")
SAND_3_IMAGE = pygame.image.load("Images/Background/sand3.png")
SKY_IMAGE = pygame.image.load("Images/Background/sky.png")

BG = (236, 217, 149)
RED = (255, 0, 0)

ANIMATION_COOLDOWN = 100

ENEMY_GROUP = pygame.sprite.Group()
BULLET_GROUP = pygame.sprite.Group()
OBJECT_GROUP = pygame.sprite.Group()
DECORATION_GROUP = pygame.sprite.Group()
WATER_GROUP = pygame.sprite.Group()
EXIT_GROUP = pygame.sprite.Group()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))