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
from RGB_alpha import gameAlpha as alpha  # @UnresolvedImport
from time import sleep  # @UnusedImport @Reimport
from mode_1 import game as campaign
os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'

# SCREEN IS LOADED HERE, environment is instantiated within constants.py
# for convenience purposes.
c = Constants()
# since constants doesn't know about 'debug', and it is where the boolean is
# made, we'll print the 'whichDisplay' here for debugging.
debug(c.DEBUG, (c.whichDisplay, c.screenError))
debug(c.DEBUG, c.displayInfo)

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

    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)


    # TESTING FILE CHANGES FROM VMWARE PART 2
    PygLogo, PygLogo_rect = load_image(c, 'pygame_logo.png')  # @UnusedVariable
    PygLogo = pygame.transform.smoothscale(PygLogo, (600, 350))
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
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
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
    #     xCut = background_rect.centerx - c.CENTER_X
    #     yCut = background_rect.centery - c.CENTER_Y
    #     background = background.subsurface((xCut, yCut), (c.DISPLAY_W , c.DISPLAY_H))
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
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(background, fade, 1)


    mode1 = 1  # the menu option for campaign mode
    mode2 = 2
    mode3 = 3

    playing = True
    while playing:
        selected = menu(c, background)
        if selected == mode1:
            campaign(c, background)
        elif selected == mode2:
            pass
        elif selected == mode3:
            alpha(c)
    # parent loop, for the whole game. Keep looping till proper option given
        # call the menu function, an option is what it will return.
        # if option is not quit, do one of the following:
            # run game mode 1: campaign
            # run game mode 2: creative
            # run game mode 3: alpha
            # run credits
            # run options
if __name__ == '__main__':
    main()
