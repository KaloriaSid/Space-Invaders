import pygame
import math
import random
from pygame import mixer

# initialize the pygame
pygame.init()

# create screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Font
font = pygame.font.Font('utils/Valegandemo.otf', 32)

# Background
background = pygame.image.load('utils/bg3.jpg')
mixer.music.load('utils/background.wav')
mixer.music.play(-1)  # -1 means in-loop infinitely

# title and icons
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('utils/ufo.png')
pygame.display.set_icon(icon)

# Player initialize
player_icon = pygame.image.load('utils/spaceship.png')
playerX = 368
playerY = 515
playerX_change = 0
playerY_change = 0

# Enemy initialize
enemy_icon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_icon.append(pygame.image.load('utils/alien.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet initialize
bullet_icon = pygame.image.load('utils/bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 0.7
# ready - you can't see the bullet on the screen
# fire - the bullet is currently moving
bullet_state = "ready"

# Score
score_value = 0
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font('utils/Valegandemo.otf', 64)


def player(x, y):
    screen.blit(player_icon, (x, y))  # blit means draw


def enemy(x, y, p):
    screen.blit(enemy_icon[p], (x, y))  # blit means draw


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_icon, (x + 20, y + 10))


def isCollision(eX, eY, bX, bY):
    x = math.pow(eX - bX, 2)
    y = math.pow(eY - bY, 2)
    distance = math.sqrt(x + y)

    return True if distance < 25 else False


def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def reset(p):
    global score_value, bullet_state, bulletY, enemyY, enemyX
    bullet_state = "ready"
    bulletY = playerY
    score_value += 1
    enemyX[p] = random.randint(0, 730)
    enemyY[p] = random.randint(50, 200)
    print(score_value)


def gameOverText():
    game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (250, 250))


running = True
while running:
    # RGB - red, green, blue
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if any keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # Horizontal movement
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4

            # Vertical movement
            # if event.key == pygame.K_UP:
            #     playerY_change = -0.4
            # if event.key == pygame.K_DOWN:
            #     playerY_change = 0.4

            # Bullet firing
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        # keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            # if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #     playerY_change = 0

    playerX += playerX_change
    # playerY += playerY_change

    # Boundary conditions for Player spaceship
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # if playerY < 0:
    #     playerY = 0
    # elif playerY >= 536:
    #     playerY = 536

    player(playerX, playerY)

    # Enemy movement
    for i in range(no_of_enemies):

        # Game over
        if enemyY[i] > 500:
            for j in range(no_of_enemies):
                enemyY[j] = 1000
            gameOverText()
            break

        enemyX[i] += enemyX_change[i]
        # enemyY += enemyY_change

        # Boundary conditions for Enemy (enemy movement)
        if enemyX[i] < 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            reset(i)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = playerY
    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    showScore(textX, textY)

    pygame.display.update()
