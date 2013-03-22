import pygame, pgext # @UnusedImport
from pygame.locals import *  # @UnusedWildImport

class Circle (pygame.sprite.Sprite):

    def __init__(self, CENTER, speed, color, image, layer):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.color = color
        self.image = image
        self.rect = image.get_rect()
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self.speed = speed
        self._layer = layer
        pgext.color.setColor(self.image, color)
        self.imageOG = self.image

    def update(self):
        self.size += int(self.speed)
        self.image = pygame.transform.smoothscale(self.imageOG, (self.size, self.size))
        self.rect = self.imageOG.get_rect()
        self.rect.center = self.OGCenter
        