import pygame, random

# initialize pygame
pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Bunny Picnic')

# FPS
FPS = 60
clock = pygame.time.Clock()

# game data
VELOCITY = 5
MUSHROOM_SCORE = 1
TULIP_SCORE = 2
CARROT_SCORE = 3

mushroom_count = 0
tulip_count = 0
carrot_count = 0
pickup_score = 1
is_collectable = True
is_cursor_spade = False
is_flipped = False


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASSGREEN = (0,154,23)
RED = (255, 0, 0)

# fonts
title_font = pygame.font.Font('data/fonts/BunnyFunny.ttf', 64)
pickup_font = pygame.font.Font('data/fonts/BunnyFunny.ttf', 20)

# text
title_text = title_font.render('Bunny Picnic', True, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.centery = 50

mushroom_score_text = pickup_font.render('Mushrooms: ' + str(mushroom_count), True, WHITE)
mushroom_score_rect = mushroom_score_text.get_rect()
mushroom_score_rect.topright = (WINDOW_WIDTH - 20, 10)

tulip_score_text = pickup_font.render('Tulips: ' + str(tulip_count), True, WHITE)
tulip_score_rect = tulip_score_text.get_rect()
tulip_score_rect.topright = (WINDOW_WIDTH - 20, 38)

carrot_score_text = pickup_font.render('Carrots: ' + str(carrot_count), True, WHITE)
carrot_score_rect = carrot_score_text.get_rect()
carrot_score_rect.topright = (WINDOW_WIDTH - 20, 64)

# sounds
eat_sound = pygame.mixer.Sound('data/sounds/eat.wav')
dig_sound = pygame.mixer.Sound('data/sounds/dig.wav')

pygame.mixer.music.load('data/sounds/bg-music.mp3')
pygame.mixer.music.set_volume(.1)
pygame.mixer.music.play(-1, 0.0)

# images
bg_image = pygame.image.load('data/images/grass.jpg')
bg_rect = bg_image.get_rect()
bg_rect.topleft = (0, 100)

bunny_image = pygame.image.load('data/images/rabbit.png')
bunny_rect = bunny_image.get_rect()
bunny_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

mushroom_image = pygame.image.load('data/images/toadstool.png')
grass_image = pygame.image.load('data/images/grass.png')
plant_image = pygame.image.load('data/images/plant.png')

tulip_image = pygame.image.load('data/images/tulip.png')
carrot_image = pygame.image.load('data/images/carrots.png')

pickups = [(mushroom_image, MUSHROOM_SCORE), (grass_image, TULIP_SCORE), (plant_image, CARROT_SCORE)]

def generate_pickup_x(bunny_rect):
    x = random.randint(0, WINDOW_WIDTH - 32)
    while bunny_rect.left <= x <= bunny_rect.right:
        x = random.randint(0, WINDOW_WIDTH - 32)
    return x

def generate_pickup_y(bunny_rect):
    y = random.randint(110, WINDOW_HEIGHT - 32)
    while bunny_rect.top <= y <= bunny_rect.bottom:
        y = random.randint(110, WINDOW_HEIGHT - 32)
    return y

pickup_image = mushroom_image
pickup_rect = pickup_image.get_rect()

pickup_rect.x = generate_pickup_x(bunny_rect)
pickup_rect.y = generate_pickup_y(bunny_rect)

# cursor
spade_cursor = pygame.image.load('data/cursors/spade.png')

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not is_collectable:
            if pickup_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_visible(False)
                is_cursor_spade = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left mouse button is clicked
                    if event.button == 1 and pickup_score == 2:
                        dig_sound.play()
                        pickup_image = tulip_image
                        is_collectable = True
                        is_cursor_spade = False
                        pygame.mouse.set_visible(True)
                    # Right mouse button is clicked
                    if event.button == 3 and pickup_score == 3:
                        dig_sound.play()
                        pickup_image = carrot_image
                        is_collectable = True
                        is_cursor_spade = False
                        pygame.mouse.set_visible(True)

            else:
                pygame.mouse.set_visible(True)
                is_cursor_spade = False

    # move bunny
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bunny_rect.left > 0:
        if is_collectable:
            bunny_rect.x -= VELOCITY
        else:
            delta = bunny_rect.left - pickup_rect.right
            if (delta > 10 or delta < 0) or bunny_rect.bottom < pickup_rect.top or bunny_rect.top > pickup_rect.bottom:
                bunny_rect.x -= VELOCITY
    if keys[pygame.K_RIGHT] and bunny_rect.right < WINDOW_WIDTH:
        if is_collectable:
            bunny_rect.x += VELOCITY
        else:
            delta = pickup_rect.left - bunny_rect.right
            if (delta > 10 or delta < 0) or bunny_rect.bottom < pickup_rect.top or bunny_rect.top > pickup_rect.bottom:
                bunny_rect.x += VELOCITY
    if keys[pygame.K_UP] and bunny_rect.top > 110:
        if is_collectable:
            bunny_rect.y -= VELOCITY
        else:
            delta = bunny_rect.top - pickup_rect.bottom
            if (delta > 10 or delta < 0) or bunny_rect.right < pickup_rect.left or bunny_rect.left > pickup_rect.right:
                bunny_rect.y -= VELOCITY
    if keys[pygame.K_DOWN] and bunny_rect.bottom < WINDOW_HEIGHT:
        if is_collectable:
            bunny_rect.y += VELOCITY
        else:
            delta = pickup_rect.top - bunny_rect.bottom
            if (delta > 10 or delta < 0) or bunny_rect.right < pickup_rect.left or bunny_rect.left > pickup_rect.right:
                bunny_rect.y += VELOCITY

    # check collision
    if bunny_rect.colliderect(pickup_rect):
        if is_collectable:
            eat_sound.play()
            if pickup_score == 1:
                mushroom_count += MUSHROOM_SCORE
            elif pickup_score == 2:
                tulip_count += TULIP_SCORE
            else:
                carrot_count += CARROT_SCORE


            # get random pickup
            pickup = random.choice(pickups)
            pickup_image = pickup[0]
            pickup_score = pickup[1]

            pickup_rect.x = generate_pickup_x(bunny_rect)
            pickup_rect.y = generate_pickup_y(bunny_rect)

            if pickup_score > 1:
                is_collectable = False

            if pickup_score == 3:
                if not is_flipped:
                    spade_cursor = pygame.transform.flip(spade_cursor, True, False)
                    is_flipped = True
            else:
                if is_flipped:
                    spade_cursor = pygame.transform.flip(spade_cursor, True, False)
                    is_flipped = False



    # fill screen
    screen.fill(GRASSGREEN)

    screen.blit(title_text, title_rect)
    screen.blit(mushroom_score_text, mushroom_score_rect)
    screen.blit(tulip_score_text, tulip_score_rect)
    screen.blit(carrot_score_text, carrot_score_rect)
    mushroom_score_text = pickup_font.render('Mushrooms: ' + str(mushroom_count), True, WHITE)
    tulip_score_text = pickup_font.render('Tulips: ' + str(tulip_count), True, WHITE)
    carrot_score_text = pickup_font.render('Carrots: ' + str(carrot_count), True, WHITE)
    pygame.draw.line(screen, BLACK, (0, 100), (WINDOW_WIDTH, 100), 5)
    screen.blit(bg_image, bg_rect)

    screen.blit(bunny_image, bunny_rect)
    # pygame.draw.rect(screen, RED, bunny_rect, 1)

    screen.blit(pickup_image, pickup_rect)
    # pygame.draw.rect(screen, WHITE, pickup_rect, 1)

    if is_cursor_spade:
        screen.blit(spade_cursor, pygame.mouse.get_pos())

    # update screen
    pygame.display.update()

    # tick the clock
    clock.tick(FPS)

pygame.quit()
