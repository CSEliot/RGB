import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image, load_song
from time import sleep
from constants import Constants
from debug import *


def menu(c, background):
    background_rect = background.get_rect()


    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 2  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    playButton = 1  # represents placeholder for button
    optionsButton = 2  # represents placeholder for button
    entered = False  # tells if the user has chosen a button




    load_song(c, 'menuV2.ogg')
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play()

    corners, corners_rect = load_image(c, "menu/menuBox.png")
    play, play_rect = load_image(c, 'menu/play.png')
    options, options_rect = load_image(c, 'menu/options.png')
    logo, logo_rect = load_image(c, 'menu/logo.png')

    if c.DISPLAY_W < corners_rect.width or \
    c.DISPLAY_H < corners_rect.height + (logo.get_height() / 2):
        # RESIZE TO FIT THE SMALL SCREEN.
        playHeight = int(play.get_height() * .5)
        playWidth = int(play.get_width() * .5)
        play = pygame.transform.smoothscale(play, (playWidth, playHeight))
        play_rect = play.get_rect()
        logoHeight = int(logo.get_height() * .5)
        logoWidth = int(logo.get_width() * .5)
        logo = pygame.transform.smoothscale(logo, (logoWidth, logoHeight))
        logo_rect = logo.get_rect()
        optionsHeight = int(options.get_height() * .5)
        optionsWidth = int(options.get_width() * .5)
        options = pygame.transform.smoothscale(options, (optionsWidth, optionsHeight))
        options_rect = options.get_rect()
        cornersHeight = int(corners.get_height() * .5)
        cornersWidth = int(corners.get_width() * .5)
        corners = pygame.transform.smoothscale(corners, (cornersWidth, cornersHeight))
        corners_rect = corners.get_rect()
        # menu locations
        playPos = c.CENTER[0], c.CENTER[1] - 25  # adjusting by specific pixels
        play_rect.center = playPos
        logoPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
        logo_rect.center = logoPos
        optionsPos = c.CENTER[0], c.CENTER[1] + 25  # adjusting by specific pixels
        options_rect.center = optionsPos
        corners_rect.center = c.CENTER
    else:
        playPos = c.CENTER[0], c.CENTER[1] - 50  # adjusting by specific pixels
        play_rect.center = playPos
        logoPos = c.CENTER[0], c.CENTER[1] - 300  # adjusting by specific pixels
        logo_rect.center = logoPos
        optionsPos = c.CENTER[0], c.CENTER[1] + 50  # adjusting by specific pixels
        options_rect.center = optionsPos
        corners_rect.center = c.CENTER

    # set original images
    OGOptions = options
    OGPlay = play


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
            newSelected = False
            # revert unselected button back
            if unselected == playButton:
                play = OGPlay
                play_rect.center = playPos
            elif unselected == optionsButton:
                options = OGOptions
                options_rect.center = optionsPos
            # change image of newly selected
            if selected == playButton:
                play = pygame.transform.smoothscale(play, (play_rect.width + 7, \
                                                        play_rect.height + 5))
                pgext.color.setColor(play, (0, 255, 255))
                play_rect.center = playPos
            elif selected == optionsButton:
                options = pygame.transform.smoothscale(options, (options_rect.width + 7, \
                                                        options_rect.height + 5))
                pgext.color.setColor(options, (0, 255, 255))
                options_rect.center = optionsPos

        # leave menu screen
        if entered:
            sleep(1)
            pygame.mixer.music.stop()
            return selected

        c.DISPLAYSURFACE.blit(background, background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(logo, logo_rect)
        c.DISPLAYSURFACE.blit(play, play_rect)
        c.DISPLAYSURFACE.blit(options, options_rect)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# def test():
#    c = Constants()
#    menu(c)
# test()
