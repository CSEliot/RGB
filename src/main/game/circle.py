import pygame, pgext  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
from debug import debug
from loader import load_image
import math as m

class Circle (pygame.sprite.Sprite):

    def __init__(self, c, CENTER, speed, color, layer):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.speed = speed
        self.radius = 300  # for collision detection w/ stars . . . wtf?
        self.color = color
        self.image, self.rect = load_image(c, 'R_small.png')
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self._layer = layer
        debug(c.DEBUG, "IN THE CIRCLE CLASS")
        pgext.color.setColor(self.image, color)
        self.imageOG = self.image
        self.MAX_SIZE = c.RING_SIZE
        self.fadeBy = 2
        self.captured = False
        self.catchable = False
        debug(c.DEBUG, self.speed)

    def update(self):
        if not(self.captured):
            self.size += int(round(self.speed))
            self.image = pygame.transform.smoothscale(self.imageOG, (self.size, self.size))
            self.rect = self.rect = self.image.get_rect(center=(self.OGCenter))
        if self.size >= self.MAX_SIZE:
            self.catchable = True
        if self.size >= self.MAX_SIZE + 30:
            self.death()

    def death(self):
#        pgext.color.setAlpha(self.image, self.fadeBy, )
#        if self.fadeBy >= 90:
        self.kill()

    def catch(self):
        self.captured = True


