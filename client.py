import time
import pygame
import sys
from network import Network
import math
from player import Ship

pygame.init()
clock = pygame.time.Clock()
game_active = True

# sets background
screen_width = 1250
screen_height = 950
screen = pygame.display.set_mode((screen_width, screen_height))

full_energy = pygame.transform.scale(pygame.image.load('full energy.png').convert_alpha(), (500, 500))
three_energy = pygame.transform.scale(pygame.image.load('3 energy.png').convert_alpha(), (500, 500))
two_energy = pygame.transform.scale(pygame.image.load('2 energy.png').convert_alpha(), (500, 500))
one_energy = pygame.transform.scale(pygame.image.load('1 energy.png').convert_alpha(), (500, 500))
no_energy = pygame.transform.scale(pygame.image.load('no energy.png').convert_alpha(), (500, 500))

bullet_image = pygame.transform.scale(pygame.image.load('bullet.png').convert_alpha(), (50, 50))
bullet_sound = pygame.mixer.Sound('laser.mp3')
ship_image = pygame.transform.scale(pygame.image.load('spaceship_sprite.png').convert_alpha(), (150, 150))

damaged_ship_image = pygame.transform.scale(pygame.image.load('spaceship_sprite_damaged.png').convert_alpha(), (150, 150))

full_health = pygame.transform.scale(pygame.image.load('full health.png').convert_alpha(), (500, 500))
_12_health = pygame.transform.scale(pygame.image.load('pixil-frame-0.png').convert_alpha(), (500, 500))
_11_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (1).png').convert_alpha(), (500, 500))
_10_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (2).png').convert_alpha(), (500, 500))
_9_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (3).png').convert_alpha(), (500, 500))
_8_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (4).png').convert_alpha(), (500, 500))
_7_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (5).png').convert_alpha(), (500, 500))
_6_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (6).png').convert_alpha(), (500, 500))
_5_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (7).png').convert_alpha(), (500, 500))
_4_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (8).png').convert_alpha(), (500, 500))
_3_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (9).png').convert_alpha(), (500, 500))
_2_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (10).png').convert_alpha(), (500, 500))
_1_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (11).png').convert_alpha(), (500, 500))
_0_health = pygame.transform.scale(pygame.image.load('pixil-frame-0 (12).png').convert_alpha(), (500, 500))


bg = pygame.image.load("space_background.png").convert()
bg = pygame.transform.scale2x(bg)
shooting = False
space = False
moving = False
bullet_num = 0
ammo = 4
bullet_time = 0
bullet_group = 0
print("hello!")
n = Network()
p = n.getP()

while True:
    print("is this working?")

    p2 = n.send(p)
    print("Maybe?")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shooting = True
            if ammo > 0:
                p.create_bullet()
                bullet_sound.play()
                ammo -= 1


        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shooting = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                moving = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                moving = False

    if ammo < 4:
        bullet_time += 1
        if bullet_time % 60 == 0:
            ammo += 1

    if moving:
        p.move()
    else:
        p.r = 0


    screen.blit(bg, (0, 0))
    screen.blit(p.image, p.rect)
    screen.blit(p2.image, p2.rect)



    for i in range(len(p.bullet_group)):
        screen.blit(p.bullet_group[i], p.bullet_group[i].rect)
        p.bullet_group[i].bullet_update()
        if p.bullet_group[i].colliderect(p2.rect):
            p2.health -= 1
            p2.image = damaged_ship_image
        if p.bullet_group[i].rect.x >= screen_height + 200 or p.bullet_group[i].rect.y >= 200:
            del p.bullet_group[i]

    for i in range(len(p2.bullet_group)):
        screen.blit(p2.bullet_group[i], p2.bullet_group[i].rect)
        p2.bullet_group[i].bullet_update()
        if p2.bullet_group[i].colliderect(p.rect):
            p.health -= 1
            p.image = damaged_ship_image
        if p2.bullet_group[i].rect.x >= screen_height + 200 or p2.bullet_group[i].rect.y >= 200:
            del p2.bullet_group[i]

    if ammo == 4:
        screen.blit(full_energy, (-100, -200))
    elif ammo == 3:
        screen.blit(three_energy, (-100, -200))
    elif ammo == 2:
        screen.blit(two_energy, (-100, -200))
    elif ammo == 1:
        screen.blit(one_energy, (-100, -200))
    elif ammo == 0:
        screen.blit(no_energy, (-100, -200))

    health_list = [_0_health, _1_health, _2_health, _3_health, _4_health, _5_health, _6_health, _7_health, _8_health, _9_health, _10_health, _11_health, _12_health, full_health]

    screen.blit(health_list[p.health], (-91, -130))

    p.update()
    p2.update()
    pygame.display.update()
    clock.tick(60)
