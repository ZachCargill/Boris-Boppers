import pygame
from pygame import mixer
import math
import random
import time

# Initialize pygame module
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
display_width = 800
display_height = 600

# Background
background = pygame.image.load('space1.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Boris Boppers')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Player
playerImg = pygame.image.load('boris.png')
playerX = 370
playerY = 480
player = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (150, 0, 0)
GREEN = (0, 150, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('corb.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet

# Ready - You cant see the bullet on the screen
# Fire - The bullet is current moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480

bulletY_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Clock
clock = pygame.time.Clock()


def show_score(x, y):
    score = font.render('score : ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (0, 255, 0))
    screen.blit(over_text, (200, 250))



def playerloc(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            screen.fill(BLACK)
            largeText = pygame.font.Font('freesansbold.ttf', 105)
            TextSurf, TextRect = text_objects('Boris Boppers', largeText)
            TextRect.center = ((display_width / 2), 200)
            screen.blit(TextSurf, TextRect)

            button('Start Invasion', 325, 350, 150, 50, GREEN, BRIGHT_GREEN, 'play')
            button('Quit Mission', 325, 450, 150, 50, RED, BRIGHT_RED, 'quit')

            pygame.display.update()
            clock.tick(15)


# Game Loop

def game_loop():
    running = True
    while running:
        global bulletX
        global bulletY
        global bulletY_change
        global bullet_state


        # RGB         R    G    B
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # If keystroke is pressed check whether its left or right
            if event.type == pygame.KEYDOWN:
                global player
                global playerX
                global playerY
                if event.key == pygame.K_LEFT:
                    player = -5
                if event.key == pygame.K_RIGHT:
                    player = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is 'ready':
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        # Get the current x coordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player = 0

        # boundary for spaceship

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        playerX += player

        # Enemy movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]
            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                global score_value
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'
        if bullet_state is 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        playerloc(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()


def button(msg, x, y, w, h, inactivecolour, activecolour, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, activecolour, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == 'play':
                game_loop( )
            if action == 'quit':
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(screen, inactivecolour, (x, y, w, h))

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


game_intro()
