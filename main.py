import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self, gravity):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.gravity_value = gravity

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += self.gravity_value
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type, speed):
        super().__init__()

        if type == 'boost':
            boost_image = pygame.image.load('graphics/powerup/boost.png').convert_alpha()
            self.image = boost_image
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), randint(200, 300)))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -100:
            self.kill()


def collision_power_up():
    global score, power_up_message, power_up_message_time
    if pygame.sprite.spritecollide(player.sprite, power_up_group, True):  
        score += 1  
        power_up_message = "Point boosted!"
        power_up_message_time = pygame.time.get_ticks()  
        return True
    return False

def display_power_up_message():
    global power_up_message, power_up_message_time
    if power_up_message:
        current_time = pygame.time.get_ticks()
        if current_time - power_up_message_time < 2000:  
            message_surf = test_font.render(power_up_message, False, (255, 165, 0))
            message_rect = message_surf.get_rect(center=(400, 100))
            screen.blit(message_surf, message_rect)
        else:
            power_up_message = None  

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, speed):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        self.speed = speed
        self.passed = False  

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

        # nguoi choi vuot qua chuong ngai
        if not self.passed and self.rect.right < player.sprite.rect.left:
            self.passed = True
            global score
            score += 1  

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    score_surf = test_font.render(f'Score: {score}', False, (64, 64, 64))  
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return score


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def display_mode_selection():
    screen.fill((94, 129, 162))

    game_name = test_font.render('MONSTER RUN', False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center=(400, 40))  
    screen.blit(game_name, game_name_rect)

    title_surf = test_font.render("Select Mode", False, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(400, 100))
    screen.blit(title_surf, title_rect)

    easy_surf = test_font.render("1. Easy", False, (111, 196, 169))
    easy_rect = easy_surf.get_rect(center=(400, 160))
    screen.blit(easy_surf, easy_rect)

    normal_surf = test_font.render("2. Normal", False, (111, 196, 169))
    normal_rect = normal_surf.get_rect(center=(400, 230))
    screen.blit(normal_surf, normal_rect)

    hard_surf = test_font.render("3. Hard", False, (111, 196, 169))
    hard_rect = hard_surf.get_rect(center=(400, 300))
    screen.blit(hard_surf, hard_rect)

    display_press_space_to_jump()

def display_press_space_to_jump():
    game_message = test_font.render('Press Space to jump', False, (255, 255, 255))
    game_message_rect = game_message.get_rect(center=(400, 380))
    screen.blit(game_message, game_message_rect)

def display_game_over():
    game_over_message = test_font.render(f'SCORE: {score}', False, (192, 192, 192))
    game_over_rect = game_over_message.get_rect(center=(400, 340))
    screen.blit(game_over_message, game_over_rect)
    restart_message = test_font.render('Press Space to restart', False, (255, 255, 255))
    restart_rect = restart_message.get_rect(center=(400, 380))
    screen.blit(restart_message, restart_rect)


def get_mode_settings(mode):
    if mode == 0:  # che do Easy
        return {"obstacle_speed": 4, "gravity": 0.8, "obstacle_timer": 2000}
    elif mode == 1:  # che do Normal
        return {"obstacle_speed": 6, "gravity": 1, "obstacle_timer": 1500}
    elif mode == 2:  # che do Hard
        return {"obstacle_speed": 8, "gravity": 1.2, "obstacle_timer": 1000}


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Monster Run')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
game_mode = None  

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)

# cac nhom
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()

power_up_group = pygame.sprite.Group()

power_up_message = None
power_up_message_time = 0

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player_stand = pygame.image.load('graphics/game over.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('MONSTER RUN', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press Space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

obstacle_timer = pygame.USEREVENT + 1

def reset_game():
    global score, game_active, game_mode
    score = 0
    game_active = False
    game_mode = None
    player.empty() 
    obstacle_group.empty()  
    power_up_group.empty()  
    pygame.time.set_timer(obstacle_timer, 0)  

def display_game_over():
    game_over_message = test_font.render(f'SCORE: {score}', False, (192, 192, 192))
    game_over_rect = game_over_message.get_rect(center=(400, 340))
    screen.blit(game_over_message, game_over_rect)
    restart_message = test_font.render('Press Space to restart', False, (255, 255, 255))
    restart_rect = restart_message.get_rect(center=(400, 380))
    screen.blit(restart_message, restart_rect)

#vong lap game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
        if game_mode is None:  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_mode = 0
                elif event.key == pygame.K_2:
                    game_mode = 1
                elif event.key == pygame.K_3:
                    game_mode = 2
                if game_mode is not None:
                    settings = get_mode_settings(game_mode)
                    player.add(Player(settings["gravity"]))
                    pygame.time.set_timer(obstacle_timer, settings["obstacle_timer"])
                    game_active = True  
                    start_time = int(pygame.time.get_ticks() / 1000)
        elif game_active:  
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail']), settings["obstacle_speed"]))
                if randint(0, 2) == 0:
                    power_up_group.add(PowerUp('boost', settings["obstacle_speed"]))

            # Space game bat dau
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        elif not game_active and game_mode is not None: 
            # Space bat dau lai
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()

    if game_mode is None:
        display_mode_selection()
    elif game_active:  
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        power_up_group.draw(screen)
        power_up_group.update()
        collision_power_up()
        display_power_up_message()  
        game_active = collision_sprite()
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if score == 0:
            display_press_space_to_jump()  
        else:
            display_game_over()

    pygame.display.update()
    clock.tick(60)