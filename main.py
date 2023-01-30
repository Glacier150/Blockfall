import pygame
from sys import exit
from random import randint

# Displays time since game start in top right


def display_time():
    current_time = pygame.time.get_ticks() // 1000 - start_time
    time_surf = font_goldeneye.render(f"Time {current_time}", False, (125, 125, 125))
    time_rect = time_surf.get_rect(topright=(1200, 0))
    screen.blit(time_surf, time_rect)
    return current_time


# Displays score in top left


def display_score():
    score_surf = font_goldeneye.render(f"Score {score}", False, (125, 125, 125))
    score_rect = score_surf.get_rect(topleft=(0, 0))
    screen.blit(score_surf, score_rect)


# Enemy falling movement


def enemy_movement(enemy_list):
    if enemy_list:
        for red_block_rect in enemy_list:
            red_block_rect.y += 5

            # If the enemy is a red block, show a red block
            if red_block_rect.width == 50:
                screen.blit(red_block_surf, red_block_rect)
            # If the enemy is a spike block, show a spike block
            else:
                screen.blit(spike_block_surf, red_block_rect)

        # If the enemy touches the ground, remove them from the list
        enemy_list = [enemy for enemy in enemy_list if enemy.bottom <= 800]

        return enemy_list
    # Enemy list is NoneType on start, makes it an empty list
    else:
        return []


# Player to enemy collision


def enemy_collisions(player, enemies):
    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy):
                return False
    return True


# Pickup to player / enemy collision


def pickup_collisions(pickup, score, enemies, player):
    if enemies:
        # Check if pickup collides with any enemy
        for enemy in enemies:
            if pickup.colliderect(enemy):
                pickup_rect.bottomleft = (randint(0, 1200 - pickup_rect.width), 0)
        # Check if pickup collides with player, if true, increase score
        if pickup.colliderect(player):
            pickup_rect.bottomleft = (randint(0, 1200 - pickup_rect.width), 0)
            score += 1
    return score


pygame.init()

display_size = display_width, display_height = (1200, 900)
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption("Blockfall")
clock = pygame.time.Clock()
font_goldeneye = pygame.font.Font("fonts/goldeneye.ttf", 80)
font_atari = pygame.font.Font("fonts/atari.ttf", 25)
game_active = False
start_time = 0
current_time = 0
score = 0

background_surf = pygame.image.load("graphics/star-background.bmp").convert()
floor_surf = pygame.image.load("graphics/grass-floor.bmp").convert()

title_surf = font_goldeneye.render("Block+fall", False, (255, 255, 255))
title_rect = title_surf.get_rect(midtop=(600, 200))

start_surf = font_goldeneye.render("Start", False, (255, 255, 255))
start_rect = start_surf.get_rect(midtop=(600, 350))

quit_surf = font_goldeneye.render("Quit", False, (255, 255, 255))
quit_rect = quit_surf.get_rect(midtop=(600, 450))

select_surf = font_goldeneye.render("*", False, (255, 255, 255))
select_rect = select_surf.get_rect(topright=(start_rect.left - 10, 360))

controls_surf = font_atari.render("Space to Continue", False, (255, 255, 255))
controls_rect = controls_surf.get_rect(midtop=(600, 600))

# Enemies
red_block_surf = pygame.image.load("graphics/red-square.bmp").convert()
red_block_rect = red_block_surf.get_rect(midtop=(600, 0))

spike_block_surf = pygame.image.load("graphics/spike-square.bmp").convert()
spike_block_rect = spike_block_surf.get_rect(midtop=(800, 0))

enemy_rect_list = []

# Pickups
pickup_surf = pygame.image.load("graphics/blue-square.bmp").convert()
pickup_rect = pickup_surf.get_rect(midtop=(400, 0))

# Player
player_surf = pygame.image.load("graphics/green-square.bmp").convert()
player_rect = player_surf.get_rect(midbottom=(600, 800))
velocity = 0
accelerating_left = False
accelerating_right = False

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # This is how to check if the mouse touches a rectangle in the event loop
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("collision")

        # This is how to check mouse button input
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("mouse down")

        # In game controls
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    accelerating_left = True
                if event.key == pygame.K_RIGHT:
                    accelerating_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    accelerating_left = False
                if event.key == pygame.K_RIGHT:
                    accelerating_right = False
        # Intro screen controls
        else:
            if event.type == pygame.KEYDOWN:

                # Start button
                if event.key == pygame.K_SPACE and select_rect.topright == (
                    start_rect.left - 10,
                    360,
                ):
                    game_active = True
                    start_time = pygame.time.get_ticks() // 1000
                    score = 0
                    red_block_rect.midtop = (600, 0)
                    pickup_rect.midtop = (400, 0)
                    player_rect.midbottom = (600, 800)

                # Quit button
                if event.key == pygame.K_SPACE and select_rect.topright == (
                    quit_rect.left - 10,
                    460,
                ):
                    pygame.quit()
                    exit()

                # Move cursor down
                if (
                    event.key == pygame.K_DOWN
                    and select_rect.topright == (start_rect.left - 10, 360)
                    and score == 0
                ):
                    select_rect.topright = (quit_rect.left - 10, 460)
                    screen.blit(select_surf, select_rect)

                # Move cursor up
                if event.key == pygame.K_UP and select_rect.topright == (
                    quit_rect.left - 10,
                    460,
                ):
                    select_rect.topright = (start_rect.left - 10, 360)
                    screen.blit(select_surf, select_rect)

        # Add enemies to list every 1.5 seconds
        if event.type == enemy_timer and game_active:
            # If random number between 0-3 is 2 or less, make the enemy a red block
            if randint(0, 4) <= 2:
                enemy_rect_list.append(
                    red_block_surf.get_rect(
                        bottomleft=(
                            randint(0, 1200 - red_block_rect.width),
                            randint(-300, 0),
                        )
                    )
                )
            # If random number between 0-3 is 3, make the enemy a spike block
            else:
                enemy_rect_list.append(
                    spike_block_surf.get_rect(
                        bottomleft=(
                            randint(0, 1200 - spike_block_rect.width),
                            randint(-300, 0),
                        )
                    )
                )

    # In game display
    if game_active:
        screen.blit(background_surf, (0, 0))
        screen.blit(floor_surf, (0, 800))
        current_time = display_time()
        display_score()

        # Enemy
        # red_block_rect.y += 5
        # if red_block_rect.bottom >= 800:
        #     red_block_rect.bottomleft = (randint(0, 1200-red_block_rect.w), 0)
        # screen.blit( red_block_rect)

        # Pickup
        pickup_rect.y += 5
        if pickup_rect.bottom >= 800:
            pickup_rect.bottomleft = (randint(0, 1200 - pickup_rect.w), 0)
        screen.blit(pickup_surf, pickup_rect)

        # Player
        if accelerating_left:
            if velocity < -8:
                velocity = -8
            velocity += -1
        if accelerating_right:
            if velocity > 8:
                velocity = 8
            velocity += 1
        if not accelerating_left and not accelerating_right:
            velocity = velocity * 0.9
            if abs(velocity) < 0.1:
                velocity = 0
        player_rect.x += velocity
        if player_rect.left <= 0:
            player_rect.left = 0
            velocity = 0
            accelerating_left = False
        if player_rect.right >= 1200:
            player_rect.right = 1200
            velocity = 0
            accelerating_right = False
        screen.blit(player_surf, player_rect)

        # Enemy movement
        enemy_rect_list = enemy_movement(enemy_rect_list)

        # Update game_active based on enemy to player collision
        game_active = enemy_collisions(player_rect, enemy_rect_list)

        # Update score pased on pickup to player / enemy collision
        score = pickup_collisions(pickup_rect, score, enemy_rect_list, player_rect)

    # Intro / Game over screen display
    else:
        screen.blit(background_surf, (0, 0))
        screen.blit(floor_surf, (0, 800))

        screen.blit(title_surf, title_rect)
        screen.blit(controls_surf, controls_rect)

        enemy_rect_list.clear()
        velocity = 0
        accelerating_left = False
        accelerating_right = False

        time_message = font_goldeneye.render(
            f"Your time {current_time}", False, (255, 255, 255)
        )
        time_message_rect = time_message.get_rect(center=(600, 450))
        score_message = font_goldeneye.render(
            f"Your score {score}", False, (255, 255, 255)
        )
        score_message_rect = score_message.get_rect(center=(600, 350))

        # Intro screen
        if current_time == 0:
            screen.blit(start_surf, start_rect)
            screen.blit(quit_surf, quit_rect)
            screen.blit(select_surf, select_rect)

        # Game over screen
        else:
            screen.blit(time_message, time_message_rect)
            screen.blit(score_message, score_message_rect)

    # This is one way you can check mouse position and collision
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
