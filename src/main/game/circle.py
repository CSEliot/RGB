import pygame, pgext # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
from debug import debug
from loader import load_image

class Circle (pygame.sprite.Sprite):

    def __init__(self, c, CENTER, speed, color, layer):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.radius = 300 # for collision detection w/ stars
        self.color = color
        self.image, self.rect = load_image(c, 'R_small.png')
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self.speed = speed
        self._layer = layer
        debug(c.DEBUG, "IN THE CIRCLE CLASS")
        pgext.color.setColor(self.image, color)
        self.imageOG = self.image
        self.killMe = False
        self.RING_SIZE = c.RING_SIZE
        self.fadeBy = 0
        self.captured = False

    def update(self):
        if not(self.captured):
            self.size += int(self.speed)
            self.image = pygame.transform.smoothscale(self.imageOG, (self.size, self.size))
            self.rect = self.rect = self.image.get_rect(center=(self.OGCenter))
        if self.size >= self.RING_SIZE+5:
            self.death()
            
    def death(self):
        
        
    def catch(self):
        self.captured = True
        
        
        