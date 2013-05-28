import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image
import math as m  # @UnusedImport
from time import sleep


def pauseScreen(c):

    paused = True

    OGDisplay = c.DISPLAYSURFACE.copy()
    OGRect = OGDisplay.get_rect()

    pixelize = 0
    for pixelize in range(1, 15, 1):
        c.DISPLAYSURFACE.blit(OGDisplay, OGRect)
        pgext.filters.pixelize(c.DISPLAYSURFACE, pixelize)
        pygame.display.flip()
        sleep(0.1)
    pygame.display.flip()

    while paused:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                paused = False

    return False



if __name__ == "__main__":
    pauseScreen()
