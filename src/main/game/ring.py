import pygame, pgext  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport

class Ring(pygame.sprite.Sprite):


    def __init__(self, CENTER, image, glow):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = image, image.get_rect()
        self.glow, self.glow_rect = glow, glow.get_rect()
        self.glow_center = (CENTER[0]-63, CENTER[1]-10)
        self.glow_rect.center = self.glow_center
        self.OGImage = self.image.copy()
        self.OGCenter = CENTER
        pgext.color.setColor(self.glow, (0,0,0))
        self.rect.center = self.OGCenter
        self.MAX_COLLIDE_SIZE = 290
        self.MIN_COLLIDE_SIZE = 280
        self.radius = 300
        self.angle = 0.0
        self.rotate_by = 10
        self.rotation_speed = 5

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
        tempImage = self.OGImage.copy()
        tempImage.blit(self.glow, self.glow_rect)
        self.image = pygame.transform.rotozoom(tempImage, self.angle, 1)
#         self.glow = pygame.transform.rotozoom(self.OGGlow, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.OGCenter))
#         self.glow_rect = self.glow.get_rect()
#         self.glow_rect.center = self.glow_center
        
    def glowColor(self, color):
        pgext.color.setColor(self.glow, color)

