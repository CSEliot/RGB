import pygame, pgext # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
from loader import load_image

class Ring(pygame.sprite.Sprite):
    

    def __init__(self,c, CENTER):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(c, 'ringNew.png')
        self.OGImage = self.image
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self.MAX_COLLIDE_SIZE = 290
        self.MIN_COLLIDE_SIZE = 280
        self.radius = 300
        self.angle = 0.0
        self.rotate_by = 0.0
        self.rotation_speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def spin(self, direction):  # Will change ring angle, based on direction
        # --Spin the Ring//--
        if direction == -1:
            self.rotate_by += self.rotation_speed
        elif direction == 1:
            self.rotate_by += -self.rotation_speed
        
    def update(self):
        self.angle += self.rotate_by * 2
        self.image = pygame.transform.rotozoom(self.OGImage, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.OGCenter))
        self.mask = pygame.mask.from_surface(self.image)
        
        