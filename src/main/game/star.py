import pygame, pgext  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
from loader import load_image
import math

class Star (pygame.sprite.Sprite):

    def __init__(self, c, CENTER, speed, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(c, 'dstar.png')
        self.OGImage = self.image
        self.dimage, _ = load_image(c, 'star.png')
        self.speed = speed
        self.radius = 40
        self.OGPos = CENTER
        self.pos = CENTER
        self.rect.center = self.pos
        self.angle = (angle * 1.0) * (3.141 / 180)
        self.spinBy = 10
        self.spinAngle = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.shooting = False
        self.travDist = 0

    def update(self):
        # get the horizontal and verital changes to the star
        xPos = self.speed * math.cos(self.angle)
        yPos = self.speed * math.sin(self.angle)
        # add them to the new self.pos, and reassign the new .rect placement
        self.pos = (self.pos[0] + xPos, self.pos[1] + yPos)
        # spin the star
        self.spinAngle += self.spinBy
        self.image = pygame.transform.rotozoom(self.OGImage, self.spinAngle, 1)
        self.rect = self.image.get_rect(center=(self.pos))
        self.mask = pygame.mask.from_surface(self.image)
        # the distance traveled is the change in x and y powered and squared.
        self.travDist = math.sqrt((self.pos[0] - self.OGPos[0]) ** 2 + (self.pos[1] - self.OGPos[1]) ** 2)
        if self.travDist >= 265:
            if not self.shooting:
                self.shooting = True
                self.shoot(self.shooting)

    def shoot(self, shooting):
        if shooting:
            self.OGImage = self.dimage
            self.speed = self.speed + 10
            self.spinBy = self.spinBy + 10
