#===============================================================================
# File:   RGB - beta
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.
#===============================================================================

import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
import math as m  # @UnusedImport
from constants import Constants  # @UnusedImport
from debug import debug  # @UnusedImport
from log import log  # @UnusedImport @Reimport
from loader import load_image, load_song  # @UnusedImport
from menu import *  # @UnusedWildImport
from time import sleep  # @UnusedImport @Reimport
from mode_1 import game as campaign
os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'


c = Constants()

class playBox():
    # This class holds all our variables to access while playing.
    def __init__(self):
        self.cAccel = 0
        self.fAccel = 0
        self.cWait = 0
        self.fWait = 0
        self.isPlaying = False
        self.isFirst = True
        self.layer = 0


def main():

    PygLogo, PygLogo_rect = load_image(c, 'pygame_logo.png')  # @UnusedVariable
    PygLogo = pygame.transform.smoothscale(PygLogo, (c.DISPLAY_W - 250, c.DISPLAY_H - 500))
    PygLogo_rect = PygLogo.get_rect()
    PygLogo_rect.center = c.CENTER
    # fade logo in and out
    fade = 0
    pgext.color.setAlpha(PygLogo, fade, 1)
    pygame.event.clear()
    # fade in
    for fade in range(255):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(PygLogo, PygLogo_rect)
        pgext.color.setAlpha(PygLogo, fade, 1)
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(PygLogo, fade, 1)
    c.DISPLAYSURFACE.fill((0, 0, 0))

    background, background_rect = load_image(c, 'starBG.png')
    # CUTTING the background to fit the DISPLAYSURFACE
    # take the center's x value, and move it left to the end of the display's
    # edge, so from center, minus the half value of width (CENTER_X) is the edge
    xCut = background_rect.centerx - c.CENTER_X
    yCut = background_rect.centery - c.CENTER_Y
    background = background.subsurface((xCut, yCut), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    fade = 0
    pgext.color.setAlpha(background, fade, 1)
    pygame.event.clear()
    # fade in BACKGROUND
    for fade in range(150):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        pgext.color.setAlpha(background, fade, 1)
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(background, fade, 1)


    mode1 = 1  # the menu option for campaign mode
    options = 2

    playing = True
    while playing:
        selected = menu(c, background)
        if selected == mode1:
            campaign(c)
        elif selected == options:
            pass
    # parent loop, for the whole game. Keep looping till proper option given
        # call the menu function, an option is what it will return.
        # if option is not quit, do one of the following:
            # run game mode 1: campaign
            # run game mode 2: creative
            # run game mode 3: classic
            # run credits
            # run options


if __name__ == '__main__':
    main()
