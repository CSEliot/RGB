import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image
import math as m  # @UnusedImport
from time import sleep


def pauseScreen(c):

    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 3  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    bReturnButton = 1  # represents placeholder for button
    optionsButton = 2  # represents placeholder for button
    bQuitButton = 3
    entered = False  # tells if the user has chosen a button



    paused = True

    #create a copy of our original surface that we can manipulate.
    pgext.color.greyscale(c.DISPLAYSURFACE)
    pgext.color.multiply(c.DISPLAYSURFACE, .3)
    OGDisplay = c.DISPLAYSURFACE.copy()
    OGRect = OGDisplay.get_rect()

    pixelize = 0
    for pixelize in range(1, 15, 1):
        # we incrementally pixelize from the OriGinal image in order to cleanly
        # modify the image.
        c.DISPLAYSURFACE.blit(OGDisplay, OGRect)
        pgext.filters.pixelize(c.DISPLAYSURFACE, pixelize)
        pygame.display.flip()
        #         sleep(0.01)#
    OGDisplay = c.DISPLAYSURFACE.copy()
    pygame.display.flip()
    
    
    
    corners, corners_rect = load_image(c, "pause/scrbx.png")
    bReturn, bReturn_rect = load_image(c, 'pause/return.png')
    options, options_rect = load_image(c, 'pause/options.png')
    paused, paused_rect = load_image(c, 'pause/paused.png')
    bQuit, bQuit_rect = load_image(c, 'pause/quit.png')

    if c.DISPLAY_W < corners_rect.width or \
    c.DISPLAY_H < corners_rect.height + (paused.get_height() / 2):
        # RESIZE TO FIT THE SMALL SCREEN.
        bReturnHeight = int(bReturn.get_height() * .5)
        bReturnWidth = int(bReturn.get_width() * .5)
        bReturn = pygame.transform.smoothscale(bReturn, (bReturnWidth, bReturnHeight))
        bReturn_rect = bReturn.get_rect()
        pausedHeight = int(paused.get_height() * .5)
        pausedWidth = int(paused.get_width() * .5)
        paused = pygame.transform.smoothscale(paused, (pausedWidth, pausedHeight))
        paused_rect = paused.get_rect()
        optionsHeight = int(options.get_height() * .5)
        optionsWidth = int(options.get_width() * .5)
        options = pygame.transform.smoothscale(options, (optionsWidth, optionsHeight))
        options_rect = options.get_rect()
        cornersHeight = int(corners.get_height() * .5)
        cornersWidth = int(corners.get_width() * .5)
        corners = pygame.transform.smoothscale(corners, (cornersWidth, cornersHeight))
        corners_rect = corners.get_rect()
        # menu locations
        bReturnPos = c.CENTER[0], c.CENTER[1] - 25  # adjusting by specific pixels
        bReturn_rect.center = bReturnPos
        pausedPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
        paused_rect.center = pausedPos
        optionsPos = c.CENTER[0], c.CENTER[1] + 25  # adjusting by specific pixels
        options_rect.center = optionsPos
        corners_rect.center = c.CENTER
    else:
        bReturnPos = c.CENTER[0], c.CENTER[1] - 100  # adjusting by specific pixels
        bReturn_rect.center = bReturnPos
        pausedPos = c.CENTER[0], c.CENTER[1] - 300  # adjusting by specific pixels
        paused_rect.center = pausedPos
        optionsPos = c.CENTER[0], c.CENTER[1] + 20  # adjusting by specific pixels
        options_rect.center = optionsPos
        bQuitPos = c.CENTER[0], c.CENTER[1] + 130
        bQuit_rect.center = bQuitPos
        # and then the corners, seperate
        corners_rect.center = c.CENTER

    # set original images
    OGOptions = options
    OGbReturn = bReturn
    OGbQuit = bQuit


    # --Main Game Loop//--
    going = True
    while going:
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if selected < buttons:
                    # set the unselected as the previous selected one.
                    unselected = selected
                    selected += 1
                    newSelected = True
            elif event.type == KEYDOWN and event.key == K_UP:
                if selected > 1:
                    unselected = selected
                    selected -= 1
                    newSelected = True
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

        c.DISPLAYSURFACE.blit(OGDisplay , OGRect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(paused, paused_rect)
        c.DISPLAYSURFACE.blit(bReturn, bReturn_rect)
        c.DISPLAYSURFACE.blit(options, options_rect)
        c.DISPLAYSURFACE.blit(bQuit, bQuit_rect)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()



if __name__ == "__main__":
    pauseScreen()
