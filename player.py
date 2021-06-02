import pygame
import sys
import math

screen_width = 1250
screen_height = 950


class Ship:

    def __init__(self):
        self.bullet_group = []

        # self.image = ship_image
        # self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))

        self.rect = (screen_width / 2, screen_height / 2)

        # r is essentially the speed
        self.r = 1
        self.acc = 0.1

        # dy is the change in y, and dx is the change in x
        self.dy = 0
        self.dx = 0
        self.prev_x, self.prev_y = screen_width / 2, screen_height / 2
        self.health = 13

        self.angle = 0
        self.moving = False
        self.have_shot = False

    def update(self, moving):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # finds the distance between the current ship position and mouse
        rel_x, rel_y = mouse_x - (self.prev_x), mouse_y - (self.prev_y)

        # finds radians using arctan, then converts to degrees.
        self.angle = -(180 / math.pi) * math.atan2(rel_y, rel_x)

        # rotates ship according to the angle -- angle is also adjusted because it was previously crooked
        # self.image = pygame.transform.rotate(self.image, int(self.angle) - 90)
        self.image_angle = int(self.angle) - 90

        # 'moves' the ship, meaning that dx and dy (found in move()) are added to the position
        # self.rect = self.image.get_rect(center=(self.prev_x + self.dx, self.prev_y - self.dy))

        self.rect = (self.prev_x + self.dx, self.prev_y - self.dy)

        if self.moving:
            self.prev_x += self.dx
            self.prev_y -= self.dy

    def move(self):
        # makes sure the ship does not go too fast
        if self.r < 7:
            self.r += self.acc

        # Use the trig formula y/r=cos(theta) and x/r=sin(theta) to find dx and dy.
        self.dy = self.r * math.sin(math.radians(self.angle))
        self.dx = self.r * math.cos(math.radians(self.angle))

    def create_bullet(self):
        # adds Bullet object with the ship position and mouse position at the time the mouse was clicked

        self.bullet_group.append(Bullet(self.prev_x, self.prev_y, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

class Bullet:
    def __init__(self, prev_x, prev_y, mouse_x, mouse_y):
        super().__init__()
        # same logic as ship.update() and ship.move(), except that rel_x, rel_y, and angle are constant
        self.x = prev_x
        self.y = prev_y
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        self.angle = ((180 / math.pi) * math.atan2(rel_x, rel_y)) / 55
        # self.image = pygame.transform.rotate(bullet_image, self.angle + 90)
        self.image_angle = self.angle + 90
        # self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect = (self.x, self.y)
        self.r = 2
        self.acc = 15
        self.dx = 0
        self.dy = 0

    def bullet_update(self):
        self.r += self.acc
        self.dx = self.r * math.cos(self.angle + 180 + 0.7)
        self.dy = self.r * math.sin(self.angle + 180 + 0.7)
        # self.rect = self.image.get_rect(center=(self.x + self.dx, self.y - self.dy))
        self.rect = (self.x + self.dx, self.y - self.dy)
