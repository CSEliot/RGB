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
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
import math as m  # @UnusedImport
from constants import Constants  # @UnusedImport
from debug import debug  # @UnusedImport
from log import log as logger # @UnusedImport @Reimport
from loader import load_image, load_song  # @UnusedImport
from menu import menu  # @UnusedWildImport
from time import sleep  # @UnusedImport @Reimport
from campaign import campaign
from stock import Stock
from creative import creative




def main():
    
    # A holding object for transferring major variables and constants.
    c = Constants()
    # holds and loads all game's images.
    stock = Stock(c)
    if c.DEBUG:
        logFile = logger(c)
    # since constants doesn't know about 'debug', and it is where the boolean is
    # made, we'll print the 'whichDisplay' here for debugging.
    debug(c.DEBUG, (c.whichDisplay, c.screenError))
    debug(c.DEBUG, c.displayInfo)
    
    # SCREEN IS LOADED HERE, environment is instantiated within constants.py
    # for convenience purposes.

    debug(c.DEBUG, "ENTERING: main")

    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)


    

    PygLogo = load_image(c, 'pygame_logo.png')
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

    mult = 1.7
    background = load_image(c, 'starBG.png')#.convert_alpha()
    #cut the background into a smaller, more manageable size.
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    fade = 0
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    pgext.color.setAlpha(background, fade, 1)
    pygame.event.clear()
    # fade in BACKGROUND
    for fade in range(0, 200, 3):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        pgext.color.setAlpha(background, fade, 1)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(background, fade, 1)


    playing = True
    while playing:
        selected = menu(c, background, stock)
        # menu will return a list, [gamemode,option,quit]. if it's gamemode
        # we have to look at the second number in the list.
        if selected == 'campaign':
            campaign(c, background, stock)
        elif selected == 'creative':
            creative(c, background, stock)
        elif selected == 'options':
            creative(c, background, stock)
        elif selected == "QUIT":
            playing = False
    # parent loop, for the whole game. Keep looping till proper option given
        # call the menu function, an option is what it will return.
        # if option is not quit, do one of the following:
            # run game mode 1: campaign
            # run game mode 2: creative
            # run game mode 3: alpha
            # run credits
            # run options
            
    Credits = load_image(c, 'credits/Credits.png')
#     credits = pygame.transform.smoothscale(credits, (c.DISPLAY_W, c.DISPLAY_H))
    pygame.event.clear()
    Credits = pygame.transform.smoothscale(Credits, (500,500))
    credits_rect = Credits.get_rect()
    credits_rect.center = c.CENTER
    c.DISPLAYSURFACE.blit(Credits, credits_rect)
    c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
    pygame.display.flip()
    for time in range(100):
        sleep(0.1)
        if pygame.event.poll().type != NOEVENT:
            break
            
            
    try:
        logger(c)
        logFile.close()
    except Exception:
        debug(c.DEBUG, "File never opened")

        
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
