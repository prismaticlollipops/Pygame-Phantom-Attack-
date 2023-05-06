import pygame
import os
pygame.font.init()
pygame.mixer.init()

#display window screen
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phantom Attack!")


size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

#colours used throughout game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,138,216)
RED = (235,33,46)

#border split in the middle of the screen
BORDER = pygame.Rect(0, HEIGHT//2 -5, WIDTH, 10)

#sound effects
BULLET_SOUND = pygame.mixer.Sound(os.path.join('assets', 'bloop.mp3'))
BULLET_HIT = pygame.mixer.Sound(os.path.join('assets', 'sparkle.mp3'))
BACKGROUND_MUSIC = pygame.mixer.Sound(os.path.join('assets', 'when the morning comes.mp3'))
BACKGROUND_MUSIC.play(-1)

HEALTH_FONT = pygame.font.SysFont('pixelmixregular', 25)
WINNER_FONT = pygame.font.SysFont('Pixel_Bug', 35)

FPS = 60 
VEL = 5
BULLET_VEL = 12
MAX_BULLETS = 4
GHOST_WIDTH, GHOST_HEIGHT = 110, 145
STARS_WIDTH, STARS_HEIGHT = 25, 25

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#load images
BLUE_GHOST_IMAGE = pygame.image.load(
    os.path.join('assets', 'ghost.png'))
BLUE_GHOST = pygame.transform.rotate(pygame.transform.scale(BLUE_GHOST_IMAGE, (GHOST_WIDTH, GHOST_HEIGHT)), 0)

RED_GHOST_IMAGE = pygame.image.load(
    os.path.join('assets', 'ghost2.png'))
RED_GHOST = pygame.transform.rotate(pygame.transform.scale(RED_GHOST_IMAGE, (GHOST_WIDTH, GHOST_HEIGHT)), 0)

BULLET_IMAGE = pygame.image.load(os.path.join('assets', 'star.png'))
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (STARS_WIDTH, STARS_HEIGHT))

BULLET_IMAGE2 = pygame.image.load(os.path.join('assets', 'image2.png'))
BULLET_IMAGE2 = pygame.transform.scale(BULLET_IMAGE2, (STARS_WIDTH, STARS_HEIGHT))


#load background photo
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background2.png')), (1200, 700))

def draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health):
    WIN.blit(bg,(0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() - 10, 10))
    WIN.blit(red_health_text, (10,10))

    WIN.blit(BLUE_GHOST, (blue.x, blue.y))
    WIN.blit(RED_GHOST, (red.x , red.y))

    for bullet in blue_bullets:
        WIN.blit(BULLET_IMAGE, bullet)

    for bullet in red_bullets:
        WIN.blit(BULLET_IMAGE2, bullet)


    pygame.display.update()
    


def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: #moves left
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < 900: #moves right and creates a barrier at which the blue ghost can move
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0: #moves up
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < 380: #moves down and creates a barrier at which the blue ghost can move
        blue.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0: #moves left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < 900: #moves right 
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 333: #moves up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < 720: #moves down
        red.y += VEL

def handle_bullets(blue_bullets, red_bullets, blue, red):
    for bullet in blue_bullets:
        bullet.y += BULLET_VEL
        WIN.blit(BULLET_IMAGE, bullet)
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x > HEIGHT:
            blue_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        WIN.blit(BULLET_IMAGE, bullet)
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2.2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)

def main():
    blue = pygame.Rect(400, 118, GHOST_WIDTH, GHOST_HEIGHT)
    red = pygame.Rect(400, 470, GHOST_WIDTH, GHOST_HEIGHT)

    blue_bullets = []
    red_bullets = []

    blue_health = 10
    red_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        pygame.event.set_allowed([pygame.QUIT, BLUE_HIT, RED_HIT])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x + blue.width, blue.y + blue.height//2 -2, 5, 10)
                    blue_bullets.append(bullet)
                    BULLET_SOUND.play()

                if event.key == pygame.K_PAGEUP and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 -2, 5, 10)
                    red_bullets.append(bullet)
                    BULLET_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()

        keys_pressed = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)

        handle_bullets(blue_bullets, red_bullets, blue, red)

        draw_window(blue, red, blue_bullets, red_bullets, blue_health, red_health)
        winner_text = ""
        if blue_health <= 0:
            winner_text = "RED GHOST WINS! Better Luck Next Time!"

        if red_health <= 0:
            winner_text = "BLUE GHOST WINS! Better Luck Next Time!"

        if winner_text != "":
            draw_winner(winner_text)
            break


    pygame.quit()

if __name__ == "__main__":
    main()