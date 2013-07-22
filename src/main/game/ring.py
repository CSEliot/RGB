import pygame, pgext  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport

class Ring(pygame.sprite.Sprite):


    def __init__(self, c, CENTER):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = c.RING_IMG.copy(), c.RING_RECT
        self.OGImage = self.image.copy()
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self.MAX_COLLIDE_SIZE = 290
        self.MIN_COLLIDE_SIZE = 280
        self.radius = 300
        self.angle = 0.0
        self.rotate_by = 0.0
        self.rotation_speed = 5
        self.mask = c.RING_MASK

    def spin(self, direction):  # Will change ring angle, based on direction
        # --Spin the Ring//--
        if direction == 'left':
            self.angle = 180
        elif direction == 'upleft':
            self.angle = 135
        elif direction == 'upright':
            self.angle = 45
        elif direction == 'up':
            self.angle = 90
        elif direction == 'right':
            self.angle = 0
        elif direction == 'downleft':
            self.angle = 225
        elif direction == 'downright':
            self.angle = 315
        elif direction == 'down':
            self.angle = 270

    def update(self):
        # self.angle += self.rotate_by
        self.image = pygame.transform.rotozoom(self.OGImage, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.OGCenter))

