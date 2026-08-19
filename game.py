import pygame
from sys import exit
import os
import random
import tile_map


row_count = 16
coloumn_count = row_count
tile_size = 32
window_width = tile_size * coloumn_count
window_height = tile_size * row_count
game_map = tile_map.GAME_MAP1
Player_X = window_width/2
Player_Y = window_height/2
Player_Width = 42
Player_Height = 48
Player_Shift = 3
jumping_velocity = -11
moving_velocity = 5
friction = 0.4
gravity = 0.5
floor_y = window_height + Player_Height
metall_width = 36
metall_height = 30
invincible_end = pygame.USEREVENT + 0
shooting_end = pygame.USEREVENT + 1
max_health = 28
health_width = 16
health_height = 4
player_shoot_width = 62
player_jump_shoot_width = 58
player_bullet_width = 16
player_bullet_height = 12
moving_bullet_velocity = 8
metall_bullet_width = 12
metall_bullet_height = metall_bullet_width
life_energy_width = 20
life_energy_height = 24
big_life_energy_width = 28
big_life_energy_height = 32
item_velocty_y = -7
blader_width = 32
blader_height = 40
blader_moving_velocty = 4
blader_jumping_velocity = 2

def load_image(image_name, scale = None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("background.png")
player_image_right = load_image("megaman-right.png", (Player_Width, Player_Height))
player_image_left = load_image("megaman-left.png", (Player_Width, Player_Height))
player_image_right_jump = load_image("megaman-right-jump.png", (Player_Width, Player_Height))
player_image_left_jump = load_image("megaman-left-jump.png", (Player_Width, Player_Height))
tiles_image = load_image("floor-tile.png", (tile_size, tile_size))
metall_image_right = load_image("metall-right.png", (metall_width, metall_height))
metall_image_left = load_image("metall-left.png", (metall_width, metall_height))
metall_image_guarding_right = load_image("metall-right-guard.png", (metall_width, metall_height))
metall_image_guarding_left = load_image("metall-left-guard.png", (metall_width, metall_height))
health_image = load_image("health.png", (health_width, health_height))
player_image_bullet = load_image("bullet.png", (player_bullet_width, player_bullet_height))
player_image_shoot_right = load_image("megaman-right-shoot.png", (player_shoot_width, Player_Height))
player_image_shoot_left = load_image("megaman-left-shoot.png", (player_shoot_width, Player_Height))
player_image_jump_shoot_right = load_image("megaman-right-jump-shoot.png", (player_jump_shoot_width, Player_Height))
player_image_jump_shoot_left = load_image("megaman-left-jump-shoot.png", (player_jump_shoot_width, Player_Height))
metall_image_bullet = load_image("metall-bullet.png", (metall_bullet_width, metall_bullet_height))
life_energy_image = load_image("life-energy.png", (life_energy_width, life_energy_height))
big_life_energy_image = load_image("big-life-energy.png", (big_life_energy_width, big_life_energy_height))
spike_image = load_image("spike.png", (tile_size, tile_size))
blader_image_left = load_image("blader-left.png", (blader_width, blader_height))
blader_image_right = load_image("blader-right.png", (blader_width, blader_height))
wall_tile_image = load_image("wall-tile.png", (tile_size, tile_size))
beam_tile_image = load_image("beam-tile.png", (tile_size, tile_size))
rock_tile1_image = load_image("rock-tile1.png", (tile_size, tile_size))
rock_tile2_image = load_image("rock-tile2.png", (tile_size, tile_size))
rock_tile3_image = load_image("rock-tile3.png", (tile_size, tile_size))
rock_tile4_image = load_image("rock-tile4.png", (tile_size, tile_size))
door_tile_image = load_image("door-tile.png", (tile_size, tile_size))
room_tile_image = load_image("room-tile.png", (tile_size, tile_size))

class Player(pygame.Rect):
    class Bullets(pygame.Rect):
        def __init__(self):
            if player.direction == "left":
                pygame.Rect.__init__(self, player.x, player.y + tile_size/2, player_bullet_width, player_bullet_height)
                self.velocity_x = -moving_bullet_velocity
            elif player.direction == "right":
                pygame.Rect.__init__(self, player.x + Player_Width, player.y + tile_size/2, player_bullet_width, player_bullet_height)
                self.velocity_x = moving_bullet_velocity
            self.image = player_image_bullet
            self.used = False
    def __init__(self):
        pygame.Rect.__init__(self, Player_X, Player_Y, Player_Width, Player_Height) 
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False
        self.direction = "right"
        self.invencibility = False
        self.max_health = max_health
        self.current_health = max_health
        self.shooting = False
        self.bullets = []
        self.score = 0

    def update_image(self):
        if self.direction == "left":
            self.image = player_image_left
        if self.direction == "right":
            self.image = player_image_right
        if self.jumping == True:
            if self.direction == "left":
                self.image = player_image_left_jump
            elif self.direction == "right":
                 self.image = player_image_right_jump
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_x]):
            if self.direction == "left":
                self.image = player_image_shoot_left
            if self.direction == "right":
                self.image = player_image_shoot_right
            if self.jumping == True:
                if self.direction == "left":
                    self.image = player_image_jump_shoot_left
                if self.direction == "right":
                    self.image = player_image_jump_shoot_right

    
    def set_invencibility(self, milliseconds = 1000):
        self.invencibility = True
        pygame.time.set_timer(invincible_end, milliseconds, 1)

    def set_shooting(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullets())
            pygame.time.set_timer(shooting_end, 250, 1)
            
class Metall(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, metall_width, metall_height)
        self.image = metall_image_left
        self.velocity_y = 0
        self.direction = "right"
        self.jumping = False
        self.health = 1
        self.bullets = []
        self.shooting = False
        self.last_fired = pygame.time.get_ticks()
        self.guarding = False

    def update_image(self):
        if self.guarding is False:
            if self.direction == "right":
                self.image = metall_image_right
            elif self.direction == "left":
                self.image = metall_image_left
        else:
            if self.direction == "right":
                    self.image = metall_image_guarding_right
            elif self.direction == "left":
                self.image = metall_image_guarding_left
        
    def set_shooting(self):
        if abs(self.x - player.x) <= tile_size*6:
            self.guarding = False
            now = pygame.time.get_ticks()
            if now - self.last_fired > 1000:
                self.shooting = True
                self.last_fired = now
                self.bullets.append(Metall.Bullet(self, -moving_bullet_velocity))
                self.bullets.append(Metall.Bullet(self, 0))
                self.bullets.append(Metall.Bullet(self, moving_bullet_velocity))
        else:
           self.guarding = True

    class Bullet(pygame.Rect):
        def __init__(self, metall, velocity_y):
            
            if metall.direction == "left":
                pygame.Rect.__init__(self, metall.x, metall.y + tile_size/2, metall_bullet_width, metall_bullet_height)
                self.velocity_x = -moving_bullet_velocity
            else:
                pygame.Rect.__init__(self, metall.x + metall_width, metall.y + tile_size/2, metall_bullet_width, metall_bullet_height)
                self.velocity_x = moving_bullet_velocity
            self.velocity_y = velocity_y
            self.image = metall_image_bullet
            self.used = False


class Blader(pygame.Rect):
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, blader_width, blader_height)
        self.image = blader_image_right
        self.direction_x = "right"
        self.direction_y = "up"
        self.max_health = 3
        self.health = 3
        self.velocity_x = blader_moving_velocty
        self.velocity_y = blader_jumping_velocity
        self.start_x = x
        self.start_y = y
        self.bullets = []
        self.last_fired = pygame.time.get_ticks()
        self.shooting = False

    def update_image(self):
        if self.direction_x == "right":
            self.image = blader_image_right
        if self.direction_x == "left":
            self.image = blader_image_left

    def set_shooting(self):
        now = pygame.time.get_ticks()
        if now - self.last_fired > 1000:
            self.shooting = True
            self.last_fired = now
            self.bullets.append(Blader.Bullet(self, moving_bullet_velocity))

    class Bullet(pygame.Rect):
            def __init__(self, blader, velocity_y):
                if blader.direction_x == "left":
                    pygame.Rect.__init__(self, blader.x, blader.y + tile_size/2, metall_bullet_width, metall_bullet_height)
                    self.velocity_x = -moving_bullet_velocity
                else:
                    pygame.Rect.__init__(self, blader.x + metall_width, blader.y + tile_size/2, metall_bullet_width, metall_bullet_height)
                    self.velocity_x = moving_bullet_velocity
                self.velocity_y = velocity_y
                self.image = metall_image_bullet
                self.used = False



pygame.init()
window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("Pygame")
player = Player()
clock = pygame.time.Clock()
Metalls = []
items = []
spikes = []
bladers = []
background_tiles = []
pygame.font.init()
game_font = pygame.font.SysFont("Arial", 24)
game_over = False

def drop_item(character):
    random_number = random.randint(1, 100)
    if 0 < random_number <= 20:
        items.append(Item(character.x, character.y, big_life_energy_image))
    elif 20 < random_number <= 70:
        items.append(Item(character.x, character.y, life_energy_image))

   

class Item(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, image.get_width(), image.get_height())
        self.image = image
        self.jumping = False
        self.used = False
        self.velocity_y = item_velocty_y

def move_player_x(velocity_x):
    move_map_x(velocity_x)
    tile = check_collision_x(player)
    if tile is not None:
        move_map_x(-velocity_x)


def move_map_x(velocity_x):
    for tile in tiles:
        tile.x += velocity_x
    for tile in background_tiles:
            tile.x += velocity_x
    for metall in Metalls:
        metall.x += velocity_x
        for bullet in metall.bullets:
            bullet.x += velocity_x
    for item in items:
        item.x += velocity_x

    for spike in spikes:
        spike.x += velocity_x

    for blader in bladers:
        blader.start_x += velocity_x
        blader.x += velocity_x

def move():
    global Metalls, items, spikes, bladers, game_over
    # if player.direction == "left" and player.velocity_x < 0:
    #     player.velocity_x += friction
    # elif player.direction == "right" and player.velocity_x > 0:
    #     player.velocity_x -= friction
    # else:
    #     player.velocity_x = 0
    # player.x += player.velocity_x
    # if player.x < 0:
    #     player.x = 0 
    #     player.velocity_x = 0
    # elif player.x > window_width - Player_Width:
    #     player.x = window_width - Player_Width

    # check_collision_x(player)

    player.velocity_y += gravity
    player.y += player.velocity_y
    if player.y + player.height > floor_y:
        player.y = floor_y - player.height
        player.jumping = False
        player.velocity_y = 0

    check_collision_y(player)

    for metall in Metalls:
        if player.x > metall.x:
            metall.direction = "right"
        elif player.x < metall.x:
            metall.direction = "left"
        metall.velocity_y += gravity
        metall.y += metall.velocity_y
        check_collision_y(metall)
        if player.invencibility is False and player.colliderect(metall):
            player.set_invencibility()
            player.current_health -= 1

    for bullet in player.bullets:
        bullet.x += bullet.velocity_x
        for metall in Metalls:
            if metall.health > 0 and not bullet.used and bullet.colliderect(metall):
                bullet.used = True
                if metall.guarding == False:
                    metall.health -= 1 
                    player.score += 500
                    if metall.health <= 0:
                        drop_item(metall)
                        player.score += 2000



    for blader in bladers:
        for bullet in blader.bullets:
            bullet.x += bullet.velocity_x
            bullet.y += bullet.velocity_y
            if not player.invencibility and player.colliderect(bullet):
                player.current_health -= 2
                bullet.used = True
                player.set_invencibility()
        for bullet in player.bullets:
            if blader.health > 0 and bullet.used == False and bullet.colliderect(blader):
                blader.health -= 1
                bullet.used = True
        blader.bullets = [bullet for bullet in blader.bullets if not bullet.used \
                        and bullet.x + bullet.width > 0 and bullet.x < window_width]

    bullet_collision()

    player.bullets = [bullet for bullet in player.bullets if not bullet.used \
                      and bullet.x + bullet.width > 0 and bullet.x < window_width]
    Metalls = [metall for metall in Metalls if metall.health > 0] 
    bladers = [blader for blader in bladers if blader.health > 0]

    for metall in Metalls:
        metall.set_shooting()
        for bullet in metall.bullets:
            bullet.x += bullet.velocity_x
            bullet.y += bullet.velocity_y
            if not player.invencibility and player.colliderect(bullet):
                player.current_health -= 2
                bullet.used = True
                player.set_invencibility()
        metall.bullets = [bullet for bullet in metall.bullets if not bullet.used \
                          and bullet.x + bullet.width > 0 and bullet.x < window_width]

    for item in items:
        item.velocity_y += gravity
        item.y += item.velocity_y
        check_collision_y(item)
        if player.colliderect(item):
            item.used = True
            if item.image == life_energy_image:
                player.current_health = min(player.current_health + 2, player.max_health)
                player.score += 1000
            elif item.image == big_life_energy_image:
                player.current_health = min(player.current_health + 5, player.max_health)
                player.score += 3000

    for spike in spikes:
        if player.colliderect(spike):
            player.current_health = 0

    for blader in bladers:
        blader.set_shooting()
        if blader.x > blader.start_x + tile_size*4:
            blader.direction_x = "left"
        elif blader.x < blader.start_x - tile_size*4:
            blader.direction_x = "right"
        if blader.direction_x == "right":
            blader.x += blader_moving_velocty
        else:
            blader.x -= blader_moving_velocty

        if blader.y > blader.start_y + tile_size:
            blader.direction_y = "up"
        elif blader.y < blader.start_y - tile_size:
            blader.direction_y = "down"
        if blader.direction_y == "up":
            blader.y -= blader_jumping_velocity
        else:
            blader.y += blader_jumping_velocity

    if player.current_health <= 0 or player.y > window_height:
        game_over = True
            
    items = [item for item in items if item.used == False]

def bullet_collision():
    for tile in tiles:
        for bullet in player.bullets:
            if bullet.colliderect(tile):
                bullet.used = True
        for metall in Metalls:
            for bullet in metall.bullets:
                if bullet.colliderect(tile):
                    bullet.used = True
        for blader in bladers:
            for bullet in blader.bullets:
                if bullet.colliderect(tile):
                    bullet.used = True


def draw():
    window.fill("blue")
    window.blit(background_image, (0, 80))
    player.update_image()
    window.blit(player.image, player)

    for tile in tiles:
        window.blit(tile.image, tile)

    for tile in background_tiles:
        window.blit(tile.image, tile)

    for metall in Metalls:
        metall.update_image()
        window.blit(metall.image, metall)
        for bullet in metall.bullets:
            window.blit(bullet.image, bullet)

    for bullet in player.bullets:
        window.blit(bullet.image, bullet)

    for item in items:
        window.blit(item.image, item)

    for spike in spikes:
        window.blit(spike.image, spike)

    for blader in bladers:
        blader.update_image()
        window.blit(blader.image, blader)
        pygame.draw.rect(window, "black", (blader.x - tile_size/5, blader.y - tile_size/3, health_width*3, health_height))
        for i in range(blader.health):
            pygame.draw.rect(window, "red", (blader.x - tile_size/5 + health_width*i, blader.y - tile_size/3, health_width, health_height))
        for bullet in blader.bullets:
            window.blit(bullet.image, bullet)

    if game_over:
        text_surface = game_font.render("Game Over", False, "white")
        window.blit(text_surface, (window_width/8, window_height/2))
        text_surface = game_font.render("Press [ENTER] to Replay", False, "white")
        window.blit(text_surface, (window_width/8, window_height/2 + tile_size))

    text_surface = game_font.render(str(player.score), False, "white")
    window.blit(text_surface, (window_width/2, tile_size/2))

    pygame.draw.rect(window, "black", (tile_size, tile_size, health_width , health_height*max_health))
    for i in range(max_health - player.current_health, max_health):
        window.blit(health_image, (tile_size, tile_size + i*health_height, health_width, health_height))


class create_tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, tile_size, tile_size)
        self.image = image

tiles = []

def create_map():
    for row in range(len(game_map)):
        for coloumn in range(len(game_map[row])):
            map_code = game_map[row][coloumn]
            x = coloumn * tile_size
            y = row * tile_size
            if map_code == 0:
                continue
            elif map_code == 1:
                tiles.append(create_tile(x, y, rock_tile1_image))
            elif map_code == 2:
                tiles.append(create_tile(x, y, rock_tile2_image))
            elif map_code == 3:
                tiles.append(create_tile(x, y, rock_tile3_image))
            elif map_code == 4:
                tiles.append(create_tile(x, y, rock_tile4_image))
            elif map_code == 5:
                tiles.append(create_tile(x, y, tiles_image))
            elif map_code == 6:
                tiles.append(create_tile(x, y, wall_tile_image))
            elif map_code == 7:
                background_tiles.append(create_tile(x, y, beam_tile_image))
            elif map_code == 8:
                spikes.append(create_tile(x, y, spike_image))
            elif map_code == 9:
                background_tiles.append(create_tile(x, y, door_tile_image))
            elif map_code == 10:
                background_tiles.append(create_tile(x, y, room_tile_image))
            elif map_code == 11:
                Metalls.append(Metall(x, y))
            elif map_code == 12:
                bladers.append(Blader(x, y))


def reset_game():
    global tiles, Metalls, items, spikes, bladers, background_tiles, player, game_over
    player = Player()
    tiles = []
    Metalls = []
    items = []
    spikes = []
    bladers = []
    background_tiles = []
    create_map()
    game_over = False
            

def collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None

def check_collision_x(character):
    tile = collision(character)
    if tile is not None:
        if character.velocity_x < 0:
            character.x = tile.x + tile.width
        elif character.velocity_x > 0:
            character.x = tile.x - character.width
        character.velocity_x = 0
    return tile

def check_collision_y(character):
    tile = collision(character)
    if tile is not None:
        if character.velocity_y < 0:
            character.y = tile.y + tile.height
        elif character.velocity_y > 0:
            character.y = tile.y - character.height
            character.jumping = False
        character.velocity_y = 0

def quit_game():
    pygame.quit()
    exit()

create_map()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == invincible_end:
            player.invencibility = False
        elif event.type == shooting_end:
            player.shooting = False

    keys = pygame.key.get_pressed()
    keys_unpress = pygame.key.get_just_released()
    if (keys[pygame.K_RETURN]) or (keys[pygame.K_0]) and game_over == True:
        reset_game()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if player.jumping is False:
            player.velocity_y = jumping_velocity
            player.jumping = True
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        player.direction = "left"
        move_player_x(moving_velocity)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player.direction = "right"
        move_player_x(-moving_velocity)
    if (keys[pygame.K_SPACE] or keys[pygame.K_x]):
        player.set_shooting()


    if game_over == False:
        move()
        draw()
        pygame.display.update()
        clock.tick(30)