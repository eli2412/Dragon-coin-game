import pygame, random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

#set FPS
FPS = 60
clock = pygame.time.Clock()

#set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 1
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

#set colors
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)

#set fonts
font = pygame.font.Font("AttackGraffiti.ttf", 32)

#set text
score_text = font.render(f"Score: {score}", True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10,10) #sets to top left with 10px down and 10px

title_text = font.render("Feed the Dragon", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render(f"Lives: {player_lives}", True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH -10, 10) #puts it on right edge with 10px left to match with score from above

game_over_text = font.render("GAME OVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32) #puts it below game over text

#set sounds and music, can use .set_volume to adjust volume level
coin_hit = pygame.mixer.Sound("coin_hit.wav")
coin_miss = pygame.mixer.Sound("coin_miss.wav")
pygame.mixer.music.load("ftd_bckground.wav")

#set images
player_image = pygame.image.load("dragon2.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load("coin1.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32) # 64 to avoid top screen and 32 for image size


#main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #check for keys being pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_s] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= PLAYER_VELOCITY
    if keys[pygame.K_d] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += PLAYER_VELOCITY

    #coin movement
    if coin_rect.x < 0:
        #play sounds
        player_lives -= 1
        coin_miss.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        coin_rect.x -= coin_velocity

    #check for collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_hit.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    #update hud
    score_text = font.render(f"Score: {score}", True, GREEN, DARKGREEN)
    lives_text = font.render(f"Lives: {player_lives}", True, GREEN, DARKGREEN)

    #check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #pause game until player press key, then reset game
        pygame.mixer.pause()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                #player want to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_pause = False
                #player wants to quit
                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False

    #fill display
    display_surface.fill((0,0,0))

    #blit hud
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0,64), (WINDOW_WIDTH, 64), 2)

    #blit images
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    #update display
    pygame.display.update()
    clock.tick(FPS)



pygame.quit()

