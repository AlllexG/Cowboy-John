import pygame
import os
from variables import *

pygame.init()

clock = pygame.time.Clock()

moving_left = False
moving_right = False
shoot = False
reload = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter")


def drawText(text, x, y):
    img = FONT.render(text, True, (0, 0, 0))
    screen.blit(img, (x, y))


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.reload_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True

        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0

        self.animation_list = []
        self.animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in self.animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"Images/{char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"Images/{char_type}/{animation}/{i}.png")
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        self.update_animation()
        self.check_alive()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.reload_cooldown > 0:
            self.reload_cooldown -= 1
	
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
        
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(
                self.rect.centerx + (0.6 * self.rect.size[0] * self.direction),
                self.rect.centery,
                self.direction,
            )
            bullet_group.add(bullet)
            self.ammo -= 1
    
    def reload(self):
        if self.ammo < 6:
            self.ammo = 6
            self.reload_cooldown = 30 * (6 - self.ammo)

        

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class HealthItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = HEART_IMAGE
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            player.health += 25
            if player.health > player.max_health:
                player.health = player.max_health
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        self.rect.x += (self.direction * self.speed)
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 15
                self.kill()
                
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 30
                self.kill()

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
object_group = pygame.sprite.Group()

health_1 = HealthItem(100, 360)
object_group.add(health_1)

player = Cowboy("Player", 200, 200, 1.5, 7, 6)
enemy = Cowboy("Enemy", 400, 300, 1.5, 7, 6)
enemy_group.add(enemy)

run = True
while run:
    clock.tick(FPS)
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (SCREEN_WIDTH, 400))

    for x in range(player.ammo):
        screen.blit(BULLET_COUNT_IMAGE, (5 + (x * 30), 40))

    player.update()
    player.draw()

    for enemy in enemy_group:
        enemy.update()
        enemy.draw()

    bullet_group.update()
    bullet_group.draw(screen)

    object_group.update()
    object_group.draw(screen)

    if player.alive:
        if shoot and not reload:
            player.shoot()
        if reload:
            player.reload()
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

        if player.reload_cooldown == 0:
            reload = False

    enemy.update()
    enemy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_j:
                shoot = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_k:
                reload = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_j:
                shoot = False

    pygame.display.update()

pygame.quit()