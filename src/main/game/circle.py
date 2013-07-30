import pygame, pgext

class Circle (pygame.sprite.Sprite):

    def __init__(self, image, CENTER, speed, color, layer):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.speed = speed
        self.radius = 300  # for collision detection w/ stars . . . wtf?
        self.color = color # of the form: (r, g, b)
        self.image, self.rect = image.copy(), image.get_rect()
        self.OGCenter = CENTER
        self.rect.center = self.OGCenter
        self._layer = layer
        pgext.color.setColor(self.image, color)
        self.imageOG = self.image
        self.MAX_SIZE = 540
        self.fadeBy = 100
        self.captured = False
        self.catchable = False
        
        self.dieing = False
        
    def update(self):
        if not(self.captured):
            self.size += int(round(self.speed))
            self.image = pygame.transform.smoothscale(self.imageOG, (self.size, self.size))
            self.rect = self.rect = self.image.get_rect(center=(self.OGCenter))
        if self.size >= self.MAX_SIZE:
            self.catchable = True
        if self.dieing:
            self.fadeBy -= 10
            pgext.color.setAlpha(self.image, self.fadeBy, 2)
        if self.fadeBy <= 0:
            self.kill()
            

    def death(self):
        self.dieing = True

    def catch(self):
        self.captured = True


