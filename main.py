import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

BG = (236, 217, 149)
RED = (255, 0, 0)

moving_left = False
moving_right = False

ANIMATION_COOLDOWN = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True

        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0

        self.animation_list = []
        self.animation_types = ['Idle', 'Run', 'Jump']
        for animation in self.animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'Images/{char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Images/{char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, left, right):
        move_x, move_y = 0, 0

        if left:
            move_x = -self.speed
            self.flip = True
            self.direction = -1
        if right:
            move_x = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        move_y += self.vel_y

        if self.rect.bottom + move_y > 400:
            move_y = 400 - self.rect.bottom
            self.in_air = False

        self.rect.x += move_x
        self.rect.y += move_y

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Cowboy('Player', 200, 200, 1.5, 7)
# enemy = Cowboy('Enemy', 400, 200, 1.5, 7)

run = True
while run:
    clock.tick(FPS)
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (SCREEN_WIDTH, 400))

    player.update_animation()
    player.draw()

    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

    # enemy.update_animation()
    # enemy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
