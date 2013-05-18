import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image, load_song
from time import sleep
from constants import Constants
from debug import *  # @UnusedWildImport
# ignore the mouse:
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)


def menu(c, background):
    background_rect = background.get_rect()


    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 3  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    playButton = 1  # represents placeholder for button
    optionsButton = 2  # represents placeholder for button
    alphaButton = 3
    entered = False  # tells if the user has chosen a button




    load_song(c, 'menuV2.ogg')
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play()

    corners, corners_rect = load_image(c, "menu/menuBox.png")
    play, play_rect = load_image(c, 'menu/play.png')
    options, options_rect = load_image(c, 'menu/options.png')
    logo, logo_rect = load_image(c, 'menu/logo.png')
    alpha, alpha_rect= load_image(c, 'menu/alpha.png')

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
        playPos = c.CENTER[0], c.CENTER[1] - 100  # adjusting by specific pixels
        play_rect.center = playPos
        logoPos = c.CENTER[0], c.CENTER[1] - 300  # adjusting by specific pixels
        logo_rect.center = logoPos
        optionsPos = c.CENTER[0], c.CENTER[1] + 20  # adjusting by specific pixels
        options_rect.center = optionsPos
        alphaPos = c.CENTER[0], c.CENTER[1] + 130
        alpha_rect.center = alphaPos
        # and then the corners, seperate
        corners_rect.center = c.CENTER

    # set original images
    OGOptions = options
    OGPlay = play
    OGAlpha = alpha


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
            if unselected == playButton:
                play = OGPlay
                play_rect.center = playPos
            elif unselected == optionsButton:
                options = OGOptions
                options_rect.center = optionsPos
            elif unselected == alphaButton:
                alpha = OGAlpha
                alpha_rect.center = alphaPos
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
            elif selected == alphaButton:
                alpha = pygame.transform.smoothscale(alpha, (alpha_rect.width + 7, \
                                                        alpha_rect.height + 5))
                pgext.color.setColor(alpha, (0, 255, 255))
                alpha_rect.center = alphaPos                    
            

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
        c.DISPLAYSURFACE.blit(alpha, alpha_rect)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def test():
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')
    # CUTTING the background to fit the DISPLAYSURFACE
    # take the center's x value, and move it left to the end of the display's
    # edge, so from center, minus the half value of width (CENTER_X) is the edge
    xCut = background_rect.centerx - c.CENTER_X
    yCut = background_rect.centery - c.CENTER_Y
    background = background.subsurface((xCut, yCut), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    
    menu(c, background)
# test()
