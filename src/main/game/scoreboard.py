import pygame  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport

class Scoreboard(pygame.sprite.Sprite):

    def __init__(self, DISPLAY_W, DISPLAY_H):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.FONT_LARGE = pygame.font.SysFont('arial', 32, True)
        self.scoreString = ''
        self.WHITE = (255, 255, 255)
        self.image = self.FONT_LARGE.render(self.scoreString, True, self.WHITE)
        self.rect = self.image.get_rect()
        self.DISPLAY_W = DISPLAY_W
        self.DISPLAY_H = DISPLAY_H
#         self.rect.topright = (self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.rect.topright = (self.DISPLAY_W - 50, 50)

    def addScore(self, score):
        # we prevent the score from going negative.
        if self.score + score > 0:
            # though it's +, it could be plus a negative.
            self.score += score
        else:
            self.score = 0
        self.scoreString = str(self.score)

    def update(self):
        self.image = self.FONT_LARGE.render(self.scoreString, True, self.WHITE)
        self.rect = self.image.get_rect()
#         self.rect.center = (self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.rect.topright = (self.DISPLAY_W - 50, 50)
