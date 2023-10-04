import pygame
import os

WIDTH, HEIGHT = 900, 500
FPS = 60

WHITE = (255, 255, 255)

#creates window: set_mode() initializes a window obect with width, height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#sets name of window
pygame.display.set_caption("SUPER SPACESHIP GAME")

#os.path.join --> join >=2 path components with either directory seperators depending on OS. Parameters : (path, *path)
#load() given string of path to image, creates image object
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))

POV_SUM_IMAGE = pygame.image.load(
    os.path.join("Assets", "pov_sum.png")
)

CRYING_MJ_IMAGE = pygame.image.load(
    os.path.join("Assets", "crying_mj.png")
)
CRYING_MJ = pygame.transform.scale(CRYING_MJ_IMAGE, (100, 100))

def draw_window():
    WIN.fill(WHITE) #fill() fills entiree screen with rgb color
    #blit() displays surfaces ontop of screen; user for images, text, sprites
    WIN.blit(POV_SUM_IMAGE, (50, 100))
    pygame.display.update() #updates display

def main():
    global CRYING_MJ
    run = True
    isMJdisplayed = False
    gameclock = pygame.time.Clock() #defines a clock object
    draw_window()
    while run:
        gameclock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                WIN.fill(WHITE)
                WIN.blit(CRYING_MJ, (300,200))
                isMJdisplayed = True
        if isMJdisplayed == True:
            CRYING_MJ = pygame.transform.rotate(CRYING_MJ, 10)
            WIN.fill(WHITE)
            WIN.blit(CRYING_MJ, (300,200))
        pygame.display.update()

        #draw_window()
    
    pygame.quit
        

if __name__ == "__main__":
    main()