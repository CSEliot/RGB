import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport @UnresolvedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
import math as m  # @UnusedImport
from time import sleep


def pauseScreen(c, stock, background):

    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 3  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    bReturnButton = 1  # represents placeholder for button
    optionsButton = 2  # represents placeholder for button
    bQuitButton = 3
    entered = False  # tells if the user has chosen a button

    # first in list are original copies, unmodified, then the second gets changed.
    backgrounds = [background.copy(), background.copy()]
    background_rect = background.get_rect(center = c.CENTER)


    #create a copy of our original surface that we can manipulate.
    #pgext.color.greyscale(c.DISPLAYSURFACE)
    #pgext.color.multiply(c.DISPLAYSURFACE, .3)

    pixelize = 0
    for pixelize in range(1, 10):
        # we incrementally pixelize from the OriGinal image in order to cleanly
        # modify the image.
        c.DISPLAYSURFACE.blit(backgrounds[0], background_rect)
        backgrounds[0] = backgrounds[1].copy()
        pgext.filters.pixelize(backgrounds[0], pixelize)
        pygame.display.flip()
        sleep(0.05)#
    
    
    corners = stock.pause["Corners"]
    bReturn = stock.pause["Return"]
    options = stock.pause["Options"]
    paused = stock.pause["Paused"]
    bQuit = stock.pause["Quit"]

    bReturn_rect = bReturn.get_rect()
    paused_rect = paused.get_rect()
    options_rect = options.get_rect()
    corners_rect = corners.get_rect()
    bQuit_rect = bQuit.get_rect()
    # menu locations
    bReturnPos = c.CENTER[0], c.CENTER[1] - 50  # adjusting by specific pixels
    bReturn_rect.center = bReturnPos
    bQuitPos = c.CENTER[0], c.CENTER[1] + 4
    bQuit_rect.center = bQuitPos
    pausedPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
    paused_rect.center = pausedPos
    optionsPos = c.CENTER[0], c.CENTER[1] + 50  # adjusting by specific pixels
    options_rect.center = optionsPos
    corners_rect.center = c.CENTER


    # set original images
    OGOptions = options
    OGbReturn = bReturn
    OGbQuit = bQuit


    # --Main Game Loop//--
    game_paused = True
    while game_paused:
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                sleep(2)
                game_paused = False
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                game_paused = False
                sleep(2)
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_DOWN:
                # set the unselected as the previous selected one.
                unselected = selected
                selected -= 1
                newSelected = True
                if selected == 0:
                    selected = 3
            elif event.type == KEYDOWN and event.key == K_UP:
                unselected = selected
                selected += 1
                newSelected = True
                if selected == 4:
                    selected = 1
            elif event.type == KEYDOWN and event.key == K_RETURN:
                entered = True

        if newSelected:
            # revert unselected button back
            newSelected = False
            if unselected == bReturnButton:
                bReturn = OGbReturn
                bReturn_rect.center = bReturnPos
            elif unselected == optionsButton:
                options = OGOptions
                options_rect.center = optionsPos
            elif unselected == bQuitButton:
                bQuit = OGbQuit
                bQuit_rect.center = bQuitPos
            # change image of newly selected
            if selected == bReturnButton:
                bReturn = pygame.transform.smoothscale(bReturn, (bReturn_rect.width + 7, \
                                                        bReturn_rect.height + 5))
                pgext.color.setColor(bReturn, (255, 255, 0))
                bReturn_rect.center = bReturnPos
            elif selected == optionsButton:
                options = pygame.transform.smoothscale(options, (options_rect.width + 7, \
                                                        options_rect.height + 5))
                pgext.color.setColor(options, (0, 255, 255))
                options_rect.center = optionsPos
            elif selected == bQuitButton:
                bQuit = pygame.transform.smoothscale(bQuit, (bQuit_rect.width + 7, \
                                                        bQuit_rect.height + 5))
                pgext.color.setColor(bQuit, (255, 0, 255))
                bQuit_rect.center = bQuitPos


        # leave menu screen
        if entered:
            sleep(1)
            return selected
        c.DISPLAYSURFACE.blit(backgrounds[0], background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(paused, paused_rect)
        c.DISPLAYSURFACE.blit(bReturn, bReturn_rect)
        c.DISPLAYSURFACE.blit(options, options_rect)
        c.DISPLAYSURFACE.blit(bQuit, bQuit_rect)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()



if __name__ == "__main__":
    from constants import Constants
    from stock import Stock
    c = Constants()
    stock = Stock(c)
    pauseScreen(c, stock, c.DISPLAYSURFACE)
