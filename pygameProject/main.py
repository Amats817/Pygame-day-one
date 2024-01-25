import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #display window gui
pygame.display.set_caption("first pygame!!")

WHITE = (255,255,255)
BLACK= (20,20,20)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) #x y width height

bulletHitSound = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
bulletFireSound =  pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

healthFont = pygame.font.SysFont('comcsans', 40)
winnerFont = pygame.font.SysFont('comicsans', 100)
FPS = 60
VEL = 5 #velocity/how fast the spaceship
bulletsVel = 15
maxBullets = 8

spaceshipWidth, spaceshipHeight = 55, 40

yellowHit = pygame.USEREVENT + 1
redHit = pygame.USEREVENT + 2

yellowSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellowSpaceship = pygame.transform.rotate(pygame.transform.scale(yellowSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 90)

redSpaceshipImage = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
redSpaceship = pygame.transform.rotate(pygame.transform.scale(redSpaceshipImage, (spaceshipWidth, spaceshipHeight)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','spaceBackground.png')), (WIDTH, HEIGHT))

def yellowMovement(keysPressed, yellow):
    if keysPressed[pygame.K_a] and yellow.x - VEL > 0:  # left #cant get over the border
        yellow.x -= VEL
    if keysPressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + BORDER.width + 5:  # right
        yellow.x += VEL
    if keysPressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keysPressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # down #below is the highest y and up is the highest y
        yellow.y += VEL

def redMovement(keysPressed, red):
    if keysPressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keysPressed[pygame.K_RIGHT] and  red.x + VEL + red.width < WIDTH + 15:  # right
        red.x += VEL
    if keysPressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keysPressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # down
        red.y += VEL

def handleBullets(yellowBullets, redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += bulletsVel
        if red.colliderect(bullet): #only works when both objects are rectangle
            pygame.event.post(pygame.event.Event(redHit))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH: #elif so we dont remove bullet twice
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= bulletsVel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellowHit))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove((bullet))

def drawWinner(text):
    drawText = winnerFont.render(text, 1, WHITE)
    WIN.blit(drawText, (WIDTH/2 - drawText.get_width()/2, HEIGHT/2 - drawText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)


def drawWindow(red, yellow, redBullets, yellowBullets, redHealth, yellowHealth):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) #where were drawing it, color, what were drawing

    redHealthText = healthFont.render("Health:" + str(redHealth), 1, WHITE)
    yellowHealthText = healthFont.render("Health:" + str(yellowHealth), 1, WHITE)
    WIN.blit(redHealthText, (WIDTH - redHealthText.get_width() - 10, 10))
    WIN.blit(yellowHealthText, (10, 10))

    WIN.blit(yellowSpaceship, (yellow.x, yellow.y))
    WIN.blit(redSpaceship, (red.x,red.y))


    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()
def main():
    #rectangle/character
    red = pygame.Rect(700, 300, spaceshipWidth, spaceshipHeight)
    yellow = pygame.Rect(100, 300, spaceshipWidth, spaceshipHeight)

    redBullets = []
    yellowBullets = []

    redHealth = 10
    yellowHealth = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get(): #list of events and loop through them
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellowBullets) < maxBullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellowBullets.append(bullet)
                    bulletFireSound.play()

                if event.key == pygame.K_RCTRL and len(redBullets) < maxBullets:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    redBullets.append(bullet)
                    bulletFireSound.play()

            if event.type == redHit:
                redHealth -= 1
                bulletHitSound.play()

            if event.type == yellowHit:
                yellowHealth -= 1
                bulletHitSound.play()

        winnerText = ""

        if redHealth <= 0:
            winnerText = "Yellow Wins!"

        if yellowHealth <= 0:
            winnerText = "Red Wins!"

        if winnerText != "":
            drawWinner(winnerText)
            break

        keysPressed = pygame.key.get_pressed()
        yellowMovement(keysPressed, yellow)
        redMovement(keysPressed, red)

        handleBullets(yellowBullets, redBullets, yellow, red)

        drawWindow(red,yellow, redBullets, yellowBullets, redHealth, yellowHealth) #rectangle

    pygame.quit()

if __name__ == "__main__": #just so it doesn't run randomly
    main()

