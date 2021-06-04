# Author: Vince Qiu, Kai Xiong, Yushu Chen
import pygame
from sys import exit
from pygame.locals import *
import random

# set up the screen size
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed

class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # The list storing player's statue pictures
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # initialize the rectangle of the player
        self.rect.topleft = init_pos
        self.speed = 8                                  # Initialize the player's speed
        self.bullets = pygame.sprite.Group()            
        self.is_hit = False                             # The group of player's bullet

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed
       
    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2

    def move(self):
        self.rect.top += self.speed

# initialize pygame
pygame.init()

# Set up the screen size in pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title
pygame.display.set_caption('Plane_Fight')

# Background image
background = pygame.image.load('resources/image/background.png').convert()

# Game Over image
game_over = pygame.image.load('resources/image/gameover.png')

# The imagie involved plane and bullet
plane_img = pygame.image.load('resources/image/shoot.png')

#  Set up the different statues of player's plane
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))

player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# Bullet image
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# Enemy plane's image & explode image
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = plane_img.subsurface(pygame.Rect(267, 347, 57, 43))

# Storing enemies objects
enemies1 = pygame.sprite.Group()

# String explode enemies objects
enemies_down = pygame.sprite.Group()


def main():
    # intitialize the shooting and enemies frequency
    shoot_frequency = 0
    enemy_frequency = 0

    # initialize the score
    score = 0

    # fps setting
    clock = pygame.time.Clock()

    # Boolean to decide stop or not
    running = True

    # main loop for the game
    while running:
        # set the max fps is 60
        clock.tick(60)

        # create billet when player not down (every 15 frequency/ 1 bullet)
        if not player.is_hit:
            if shoot_frequency % 15 == 0:
                player.shoot(bullet_img)
            shoot_frequency += 1
            if shoot_frequency >= 15:
                shoot_frequency = 0

        # create enemy per 50 frequency
        if enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
            enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
            enemies1.add(enemy1)
        enemy_frequency += 1
        if enemy_frequency >= 100:
            enemy_frequency = 0

        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:  # if bullet reach edge of screen, delete it
                player.bullets.remove(bullet)   

        for enemy in enemies1:
            enemy.move()
            # if player hit the enemy plane
            if pygame.sprite.collide_circle(enemy, player):
                enemies_down.add(enemy)
                enemies1.remove(enemy)
                player.is_hit = True
                break
            # if enemy move out the screen, delete it.
            if enemy.rect.top < 0:
                enemies1.remove(enemy)

        # set up the action of the fall down enemies (and let it into group of enemy_down group)
        enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down)

        # Set up background
        screen.fill(0)
        screen.blit(background, (0, 0))

        # Set up player's plane
        if not player.is_hit:
            screen.blit(player.image[0], player.rect)   # normal plane
        else:
            # if player down, draw it on screen
            screen.blit(player.image[1], player.rect)   # explode plane
            running = False

        # enemies hitted by the plane
        for enemy_down in enemies_down:
            enemies_down.remove(enemy_down)
            score += 1
            screen.blit(enemy_down.down_imgs, enemy_down.rect) # explode plane( enemy )


        # show up bullets on screen
        player.bullets.draw(screen)
        # show up enemies on screen
        enemies1.draw(screen)

        # show up the score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render('score: '+str(score), True, (128, 128, 128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # renew the image
        pygame.display.update() # .flip()have same effect

        # pygame.time.delay(50)

        # exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # get keyborad statue
        key_pressed = pygame.key.get_pressed()

        # deal with statue (make plane move)
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()

    # show up "Game over" and stop the game
    font = pygame.font.Font(None, 64)
    text = font.render('Final Score: '+ str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, text_rect)

    # Show up the score and exit the game
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

if __name__ == '__main__':
    main()
