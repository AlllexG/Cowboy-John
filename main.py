from variables import *
from button import Button
import pygame
import os
import random
import csv

pygame.init()

moving_left = False
moving_right = False
shoot = False
reload = False

images_list = []
for x in range(TILE_TYPES):
    current_image = pygame.image.load(f'Images/Tile/{x}.png')
    current_image = pygame.transform.scale(current_image, (TILE_SIZE, TILE_SIZE))
    images_list.append(current_image)

pygame.display.set_caption("Shooter")


def drawText(text, x, y):
    img = FONT.render(text, True, (0, 0, 0))
    SCREEN.blit(img, (x, y))
    

def draw_background():
    SCREEN.fill(BG)
    width = SKY_IMAGE.get_width()
    for x in range(4):
        SCREEN.blit(SKY_IMAGE, ((x * width) - background_scroll * 0.5, 0))
        SCREEN.blit(SAND_3_IMAGE, ((x * width) - background_scroll * 0.5, SCREEN_HEIGHT - SAND_3_IMAGE.get_height() - 250))
        SCREEN.blit(SAND_2_IMAGE, ((x * width) - background_scroll * 0.6, SCREEN_HEIGHT - SAND_2_IMAGE.get_height() - 270))
        SCREEN.blit(SAND_1_IMAGE, ((x * width) - background_scroll * 0.8, SCREEN_HEIGHT - SAND_1_IMAGE.get_height() - 10))


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, health, shooting_cooldown):
        pygame.sprite.Sprite.__init__(self)

        self.alive = True
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.shooting_speed = shooting_cooldown
        self.reload_time = 0
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True
        self.char_type = char_type

        self.move_counter = 0
        self.idling = False
        self.vision = pygame.Rect(0, 0, 250, 20)
        self.idle_counter = 0

        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0

        self.animation_list = []
        self.animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in self.animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"Images/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"Images/{self.char_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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
        screen_scroll = 0

        if left:
            move_x = -self.speed
            self.flip = True
            self.direction = -1
        if right:
            move_x = self.speed
            self.flip = False
            self.direction = 1

        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        move_y += self.vel_y
        
        #check collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + move_x, self.rect.y, self.width, self.height):
                move_x = 0
            #check collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + move_y, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    move_y = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    move_y = tile[1].top - self.rect.bottom
                    
        #check if going off the edges of the screen
        if self.char_type == 'Player':
            if self.rect.left + move_x < 0 or self.rect.right + move_x > SCREEN_WIDTH:
                move_x = 0
                
        self.rect.x += move_x
        self.rect.y += move_y
        
        #update scroll based on player position
        if self.char_type == 'Player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and\
                background_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                or (self.rect.left < SCROLL_THRESH and background_scroll > abs(move_x)):
                self.rect.x -= move_x
                screen_scroll = -move_x
                
        return screen_scroll
                
    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = self.shooting_speed
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            BULLET_GROUP.add(bullet)
            if self.char_type == 'Player':
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

    def ai(self):
        if self.alive and player.alive:
            if not self.idling and  random.randint(1, 200) == 1:
                self.idling = True
                self.update_action(0)
                self.idle_counter = 50
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot()    
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    self.move_counter += 1
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idle_counter -= 1
                    if self.idle_counter <= 0:
                        self.idling = False
                        
        #scroll
        self.rect.x += screen_scroll
    
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            if self.char_type == 'Enemy':
                health = HealthItem(self.rect.centerx - 25, self.rect.centery - 25)
                OBJECT_GROUP.add(health)
            self.kill()

    def draw(self):
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World:
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data_from_csvfile):
        self.level_length = len(data_from_csvfile[0])
        
        for y, row in enumerate(data_from_csvfile):
            for x, tile in enumerate(row):
                if tile >= 0:
                    current_image = images_list[tile]
                    image_rect = current_image.get_rect()
                    image_rect.x = x * TILE_SIZE
                    image_rect.y = y * TILE_SIZE
                    tile_data = (current_image, image_rect)
                    if tile in range(9): #image of sand
                        self.obstacle_list.append(tile_data)
                    elif tile in (9, 10): #image of water
                        water = Water(current_image, x * TILE_SIZE, y * TILE_SIZE)
                        WATER_GROUP.add(water)
                    elif tile in (11, 12, 13, 14, 18, 19): #image of decoration
                        decoration = Decoration(current_image, x * TILE_SIZE, y * TILE_SIZE)
                        DECORATION_GROUP.add(decoration)
                    elif tile == 15: #create player
                        player = Cowboy("Player", x * TILE_SIZE, y * TILE_SIZE, 1.5, 8, 6, 10, 30)
                    elif tile == 16: #create enemies
                        enemy = Cowboy('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.5, 2, 6, 10, 50)
                        ENEMY_GROUP.add(enemy)
                    elif tile == 17: #create exit
                        exit = Exit(current_image, x * TILE_SIZE, y * TILE_SIZE)
                        EXIT_GROUP.add(exit)
        
        return player
                    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            SCREEN.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll
        
        
class Water(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll
        
        
class Exit(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll                   
                    
class HealthItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = HEART_IMAGE
        self.vel_y = -11
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        
        if pygame.sprite.collide_rect(self, player):
            if player.health != player.max_health:
                player.health += 2
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()

        self.vel_y += GRAVITY
        move_y = self.vel_y
        
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + move_y, self.width, self.height):
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    move_y = tile[1].top - self.rect.bottom
                elif self.vel_y < 0:
                    self.vel_y = 0
                    move_y = tile[1].bottom - self.rect.top
        
        self.rect.y += move_y    


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 30
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
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
                    

start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, START_BUTTON_IMAGE, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, EXIT_BUTTON_IMAGE, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, RESTART_BUTTON_IMAGE, 1)


world_data = []
for row in range(ROWS):
    current_row = [-1] * COLS
    world_data.append(current_row)

with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
            
world = World()
player = world.process_data(world_data)

run = 1
while run:
    CLOCK.tick(FPS)
    
    if not start_game:
        #draw menu
        SCREEN.fill(BG)
        
        #add buttons
        if start_button.draw(SCREEN):
            start_game = True
        exit_button.draw(SCREEN)
    else:
        draw_background()
        
        world.draw()
        
        player.update()
        player.draw()
        player.health_bar()
        player.ammo_count()
        
        for enemy in ENEMY_GROUP:
            enemy.ai()
            enemy.update()
            enemy.draw()
            
        BULLET_GROUP.update()
        BULLET_GROUP.draw(SCREEN)
        
        OBJECT_GROUP.update()
        OBJECT_GROUP.draw(SCREEN)
        
        DECORATION_GROUP.update()
        DECORATION_GROUP.draw(SCREEN)
        
        WATER_GROUP.update()
        WATER_GROUP.draw(SCREEN)
        
        EXIT_GROUP.update()
        EXIT_GROUP.draw(SCREEN)
        
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
                
            screen_scroll = player.move(moving_left, moving_right)
            background_scroll -= screen_scroll
            
            if player.reload_time == 0:
                reload = False
                
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
                
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