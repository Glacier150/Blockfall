import pygame
import sys
import random

def display_time():
    current_time = pygame.time.get_ticks()//1000 - start_time
    time_surf = font_goldeneye.render(f"Time {current_time}", False, (125, 125, 125))
    time_rect = time_surf.get_rect(topright = (1200, 0))
    screen.blit(time_surf, time_rect)

def display_score():
    score_surf = font_goldeneye.render(f"Score {score}", False, (125, 125, 125))
    score_rect = score_surf.get_rect(topleft = (0, 0))
    screen.blit(score_surf, score_rect)

pygame.init()

display_size = display_width, display_height = (1200, 900)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Blockfall")
clock = pygame.time.Clock()
font_goldeneye = pygame.font.Font("fonts/goldeneye.ttf", 80)
font_atari = pygame.font.Font("fonts/atari.ttf", 25)
game_active = False
start_time = 0
game_intro = True
score = 0

background_surf = pygame.image.load("graphics/star-background.bmp").convert()
floor_surf = pygame.image.load("graphics/grass-floor.bmp").convert()

title_surf = font_goldeneye.render("Block+fall", False, (255, 255, 255))
title_rect = title_surf.get_rect(midtop = (600, 200))

start_surf = font_goldeneye.render("Start", False, (255, 255, 255))
start_rect = start_surf.get_rect(midtop = (600, 350))

quit_surf = font_goldeneye.render("Quit", False, (255, 255, 255))
quit_rect = quit_surf.get_rect(midtop = (600, 450))

select_surf = font_goldeneye.render("*", False, (255, 255, 255))
select_rect = select_surf.get_rect(topright = (start_rect.left - 10, 360))

controls_surf = font_atari.render("Space to Continue", False, (255, 255, 255))
controls_rect = controls_surf.get_rect(midtop = (600, 600))

enemy_surf = pygame.image.load("graphics/red-square.bmp").convert()
enemy_rect = enemy_surf.get_rect(midtop = (600, 0))

pickup_surf = pygame.image.load("graphics/blue-square.bmp").convert()
pickup_rect = pickup_surf.get_rect(midtop = (400, 0))

player_surf = pygame.image.load("graphics/green-square.bmp").convert()
player_rect = player_surf.get_rect(midbottom = (600, 800))
player_speed = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # This is how to check if the mouse touches a rectangle in the event loop
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("collision")

        # This is how to check mouse button input
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("mouse down")

        if game_intro == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and select_rect.topright == (start_rect.left - 10, 360):
                    game_intro = False
                    game_active = True
                if event.key == pygame.K_SPACE and select_rect.topright == (quit_rect.left - 10, 460):
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_DOWN and select_rect.topright == (start_rect.left - 10, 360):
                    select_rect.topright = (quit_rect.left - 10, 460)
                    screen.blit(select_surf, select_rect)
                if event.key == pygame.K_UP and select_rect.topright == (quit_rect.left - 10, 460):
                    select_rect.topright = (start_rect.left - 10, 360)
                    screen.blit(select_surf, select_rect)

        if game_active == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_speed = -5
                if event.key == pygame.K_RIGHT:
                    player_speed = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_speed == -5:
                    player_speed = 0
                if event.key == pygame.K_RIGHT and player_speed == 5:
                    player_speed = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    enemy_rect.midbottom = (600, 0)
                    pickup_rect.midbottom = (400, 0)
                    start_time = pygame.time.get_ticks()//1000
                    score = 0

    if game_intro == True:
        screen.blit(background_surf, (0, 0))
        screen.blit(floor_surf, (0, 800))
        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)
        screen.blit(quit_surf, quit_rect)
        screen.blit(select_surf, select_rect)
        screen.blit(controls_surf, controls_rect)
    elif game_active == True:
        screen.blit(background_surf, (0, 0))
        screen.blit(floor_surf, (0, 800))
        display_time()
        display_score()

        # Enemy
        enemy_rect.y += 5
        if enemy_rect.bottom >= 800:
            enemy_rect.bottomleft = (random.randint(0, 1200-enemy_rect.w), 0)
        screen.blit(enemy_surf, enemy_rect)

        # Pickup
        pickup_rect.y += 5
        if pickup_rect.bottom >= 800:
            pickup_rect.bottomleft = (random.randint(0, 1200-pickup_rect.w), 0)
        screen.blit(pickup_surf, pickup_rect)

        # Player
        player_rect.x += player_speed
        if player_rect.left <= 0:
            player_rect.left = 0
        if player_rect.right >= 1200:
            player_rect.right = 1200
        screen.blit(player_surf, player_rect)

        # Collision
        if enemy_rect.colliderect(player_rect):
            enemy_rect.bottomleft = (random.randint(0, 1200-enemy_rect.w), 0)
            game_active = False
        
        if pickup_rect.colliderect(player_rect):
            pickup_rect.bottomleft = (random.randint(0, 1200-pickup_rect.w), 0)
            score += 1
            display_score()
    else:
        screen.fill("Black")
        screen.blit(player_surf, player_rect)
        screen.blit(controls_surf, controls_rect)
        
    # This is one way you can check mouse position and collision
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)