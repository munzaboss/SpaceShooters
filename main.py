
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
FPS = 60
VEL = 5 #Moves 5 per tick
BULLET_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans",  40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPACEBLUE = (0, 59, 89)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

#creates window: set_mode() initializes a window obect with width, height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#creates a Rect() instance set to variable MIDDLE
MIDDLE = pygame.Rect((WIDTH//2) - (10/2), 0, 10, HEIGHT)
#sets name of window
pygame.display.set_caption("SUPER SPACESHIP GAME")

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))
#os.path.join --> join >=2 path components with either directory seperators depending on OS. Parameters : (path, *path)
#load() given string of path to image, creates image object
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
#creates new spaceship object which scales the yellow spaceship to a specified width, height and rotates it 90
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE_IMAGE = pygame.image.load(
    os.path.join("Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))


def handle_yellow_movement(yellow, keys_pressed):
    #Left
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left(checks if bool at that index is true)
        yellow.x -= VEL
    #Right 
    if keys_pressed[pygame.K_d] and (yellow.x + VEL + yellow.width) < MIDDLE.x: #checks if yellow space ship is always to left of divider
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y + VEL + yellow.height) < HEIGHT: #Down
        yellow.y += VEL
def handle_red_movement(red, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and  red.x - VEL > (MIDDLE.x + MIDDLE.width):#Left(checks if bool at that index is true)    
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x + VEL + red.width) < WIDTH : #Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN]and (red.y + VEL + red.height) < HEIGHT: #Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += VEL
        # colliderect() checks if two Rect instances are colliding ie their dimensions overlap
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
            bullet.x -= VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x <= 0:
                red_bullets.remove(bullet)



def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):

    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, MIDDLE)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, ((WIDTH - red_health_text.get_width() - 10), 10))
    WIN.blit(yellow_health_text, (10, 10))
    #blit() displays surfaces ontop of screen; user for images, text, sprites
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update() #updates display

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    #1. pygame.rect arguments(x , y, width, height)
    #2. creates an instance with an x ,y coordinate and height width specifications
    #3. ollision rect hitbox for yellow and red spaceship in which the images are printed
    # inside of it via draw_window()

    #4. BUG : pygame.rect takes width, height in that order but when creating the instances we flip it because
    #the image of spaceships drawn is rotated 90/270 degrees. Therefore, the width and height of the rotated triangle are flipped
    #[check geomeetry for proof]
    yellow = pygame.Rect(100, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    red = pygame.Rect(700, 300, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    red_bullets=[]
    yellow_bullets=[]
    
    red_health = 10
    yellow_health = 10

    run = True
    gameclock = pygame.time.Clock() #defines a clock object
    while run:
        gameclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()


        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        #gets a list of a bool corresponding to every key and is searched through via index. True if presseddw
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(yellow, keys_pressed)
        handle_red_movement(red, keys_pressed)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health)
    
    main()
        

if __name__ == "__main__":
    main()