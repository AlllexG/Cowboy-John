import pygame
import os
from variables import *

pygame.init()

moving_left = False
moving_right = False
shoot = False
reload = False

pygame.display.set_caption("Shooter")


def drawText(text, x, y):
    img = FONT.render(text, True, (0, 0, 0))
    SCREEN.blit(img, (x, y))


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, health, shooting_speed):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.shooting_speed = shooting_speed
        self.reload_time = 0
        self.health = health
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

    def health_bar(self):
        half_hearts_total = self.health / 2
        half_heart_exists = half_hearts_total - int(half_hearts_total) != 0

        for heart in range(int(self.max_health / 2)):
            if int(half_hearts_total) > heart:
                SCREEN.blit(FULL_HEART_IMAGE, (heart * 50  + 10, 10))
            elif half_heart_exists and int(half_hearts_total) == heart:
                SCREEN.blit(HALF_HEART_IMAGE, (heart * 50 + 10, 10))
            else:
                SCREEN.blit(EMPTY_HEART_IMAGE, (heart * 50 + 10, 10))

    def ammo_count(self):
        for x in range(player.ammo):
            SCREEN.blit(BULLET_COUNT_IMAGE, (5 + (x * 30), 40))
    
        
    def update(self):
        self.update_animation()
        self.check_alive()
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
	
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
            self.shoot_cooldown = self.shooting_speed
            bullet = Bullet(
                self.rect.centerx,
                self.rect.centery + 5,
                self.direction,
            )
            BULLET_GROUP.add(bullet)
            self.ammo -= 1
    
    def reload(self):
        if pygame.time.get_ticks() - self.reload_time > 500:
            self.ammo += 1
            self.reload_time = pygame.time.get_ticks()
        if self.ammo == 6:
            self.reload_time = 0

        

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
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class HealthItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = HEART_IMAGE
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if player.health != player.max_health:
                player.health += 2
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 50
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        self.rect.x += (self.direction * self.speed)
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        if pygame.sprite.spritecollide(player, BULLET_GROUP, False):
            if player.alive:
                player.health -= 2
                self.kill()
        
        for enemy in ENEMY_GROUP:
            if pygame.sprite.spritecollide(enemy, BULLET_GROUP, False):
                if enemy.alive:
                    enemy.health -= 5
                    self.kill()

health_1 = HealthItem(100, 360)
OBJECT_GROUP.add(health_1)

player = Cowboy("Player", 200, 200, 1.5, 7, 6, 10, 25)
enemy = Cowboy("Enemy", 500, 350, 1.5, 7, 6, 10, 50)
ENEMY_GROUP.add(enemy)

run = True
while run:
    CLOCK.tick(FPS)
    SCREEN.fill(BG)
    pygame.draw.line(SCREEN, RED, (0, 400), (SCREEN_WIDTH, 400))

    player.update()
    player.draw()
    player.health_bar()
    player.ammo_count()

    for enemy in ENEMY_GROUP:
        enemy.update()
        enemy.draw()

    BULLET_GROUP.update()
    BULLET_GROUP.draw(SCREEN)

    OBJECT_GROUP.update()
    OBJECT_GROUP.draw(SCREEN)

    if player.alive:
        if shoot and not reload:
            player.shoot()
        if reload:
            drawText('RELOADING', 600, 15)
            player.reload()
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right)

        if player.reload_time == 0:
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
            if event.key == pygame.K_k and player.reload_time == 0 and player.ammo < 6:
                reload = True
                player.reload_time = pygame.time.get_ticks()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_j:
                shoot = False

    pygame.display.update()

pygame.quit()