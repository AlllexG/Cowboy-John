import pygame


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

start_game = False
start_intro = False

level = 1
MAX_LEVELS = 3
ROWS = 16
COLS = 50

FPS = 60
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 20

SCROLL_THRESH = 360
screen_scroll = 0
background_scroll = 0

FONT = pygame.font.Font('PixelForce.ttf', 32)

GRAVITY = 0.75

START_BUTTON_IMAGE = pygame.image.load('Images/Buttons/start_button.png').convert_alpha()
EXIT_BUTTON_IMAGE = pygame.image.load('Images/Buttons/exit_button.png').convert_alpha()
RESTART_BUTTON_IMAGE = pygame.image.load('Images/Buttons/restart_button.png').convert_alpha()

BULLET_IMAGE = pygame.image.load("Images/Objects/bullet.png").convert_alpha()
BULLET_COUNT_IMAGE = pygame.image.load("Images/Objects/bullet_count_image.png").convert_alpha()

HEART_IMAGE = pygame.image.load("Images/Objects/heart.png").convert_alpha()
FULL_HEART_IMAGE = pygame.image.load("Images/Objects/full_heart.png").convert_alpha()
HALF_HEART_IMAGE = pygame.image.load("Images/Objects/half_heart.png").convert_alpha()
EMPTY_HEART_IMAGE = pygame.image.load("Images/Objects/empty_heart.png").convert_alpha()

SAND_1_IMAGE = pygame.image.load("Images/Background/sand1.png").convert_alpha()
SAND_2_IMAGE = pygame.image.load("Images/Background/sand2.png").convert_alpha()
SAND_3_IMAGE = pygame.image.load("Images/Background/sand3.png").convert_alpha()
SKY_IMAGE = pygame.image.load("Images/Background/sky.png").convert_alpha()

BG = (236, 217, 149)
RED = (136, 8, 8)
BLACK = (0, 0, 0)


ANIMATION_COOLDOWN = 150

ENEMY_GROUP = pygame.sprite.Group()
BULLET_GROUP = pygame.sprite.Group()
OBJECT_GROUP = pygame.sprite.Group()
DECORATION_GROUP = pygame.sprite.Group()
WATER_GROUP = pygame.sprite.Group()
EXIT_GROUP = pygame.sprite.Group()