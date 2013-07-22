import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image, load_song
from time import sleep
from time import time
from constants import Constants
from debug import *  # @UnusedWildImport

def mainMenu(c, background):
    
    debug(c.DEBUG, "Entering: mainMenu")
    # the background is the current information from the screen. It's faster
    # than grabbing it from the constants file.
    background_rect = background.get_rect()


    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 3  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    playButton = 1  # represents placeholder for button
    optionsButton = 2  # represents placeholder for button
    quitButton = 3
    entered = False  # tells if the user has chosen a button

    #Other Variables
    c.BgAngle = 0
    fpsList = []
    fpsWait = 2 #how many seconds till we report the game's FPS.
    frameCount = 0

    corners, __corners_rect = load_image(c, "menu/menuBox.png")
    play,__play_rect = load_image(c, 'menu/play.png')
    options, __options_rect = load_image(c, 'menu/options.png')
    logo, __logo_rect = load_image(c, 'menu/logo.png')
    alpha, __alpha_rect = load_image(c, 'menu/alpha.png')  # @UnusedVariable
    quit, __quit_rect = load_image(c, 'menu/quit.png')  # @ReservedAssignment

    # RESIZE TO FIT THE SCREEN.
    # RESIZING VVVVVVVVVVVVVVVVV
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
    quitHeight = int(quit.get_height() * .5)
    quitWidth = int(quit.get_width() * .5)
    quit = pygame.transform.smoothscale(quit, (quitWidth, quitHeight))  # @ReservedAssignment
    quit_rect = quit.get_rect()
    cornersHeight = int(corners.get_height() * .5)
    cornersWidth = int(corners.get_width() * .5)
    corners = pygame.transform.smoothscale(corners, (cornersWidth, cornersHeight))
    corners_rect = corners.get_rect()
    # RESIZING ^^^^^^^^^^^^^^^^^
    # menu locations, done both resizing or not.
    playPos = c.CENTER[0], c.CENTER[1] - 25  # adjusting by specific pixels
    play_rect.center = playPos
    logoPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
    logo_rect.center = logoPos
    optionsPos = c.CENTER[0], c.CENTER[1] + 25  # adjusting by specific pixels
    options_rect.center = optionsPos
    quitPos = c.CENTER[0], c.CENTER[1] + 75
    quit_rect.center = quitPos
    # and then the corners, seperate
    corners_rect.center = c.CENTER

    # set original images
    OGOptions = options.copy()
    OGPlay = play.copy()
    OGquit = quit.copy()
    OGBackground = background.copy()
    
    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)
    
    
    # --Main Game Loop//--
    going = True
    oldTime = time()
    while going:
        """ROTATION TESTING"""
        # rotate the background, but only 15 times/second, not 30.
        # if the frame rate is 30/sec, then rotate when its an odd frame.
        if frameCount%3 == 0:
            c.BgAngle += .03
            background = pygame.transform.rotozoom(OGBackground, c.BgAngle%360 , 1)
            background_rect = background.get_rect()
            background_rect.center = c.CENTER
        frameCount += 1
        
        
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                going = False
                entered = True
                selected = "QUIT"
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                entered = True
                selected = "QUIT"
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
            elif unselected == quitButton:
                quit = OGquit
                quit_rect.center = quitPos
            # change image of newly selected
            if selected == playButton:
                play = pygame.transform.smoothscale(play, (play_rect.width + 7, \
                                                        play_rect.height + 5))
                pgext.color.setColor(play, (255, 255, 0))
                play_rect.center = playPos
            elif selected == optionsButton:
                options = pygame.transform.smoothscale(options, (options_rect.width + 7, \
                                                        options_rect.height + 5))
                pgext.color.setColor(options, (0, 255, 255))
                options_rect.center = optionsPos
            elif selected == quitButton:
                quit = pygame.transform.smoothscale(quit, (quit_rect.width + 7, \
                                                        quit_rect.height + 5))
                pgext.color.setColor(quit, (255, 0, 255))
                quit_rect.center = quitPos






        fpsList.append(c.FPSCLOCK.get_fps())
        # report the frame rate every 5 seconds
        newTime = time()
        if newTime - oldTime >= fpsWait:
            avgFPS = mean(fpsList)
            debug(c.DEBUG, avgFPS)
            pygame.display.set_caption('RGB. FPS: {0}'.format(avgFPS))
            fpsList = []
            oldTime = time()

        # reset frame count once it exceeds 30 frames
        if frameCount >= 30:
            frameCount = 0
            


        # leave menu screen
        if entered:
            sleep(1)
            return selected
        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(logo, logo_rect)
        c.DISPLAYSURFACE.blit(play, play_rect)
        c.DISPLAYSURFACE.blit(options, options_rect)
        c.DISPLAYSURFACE.blit(quit, quit_rect)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()
        #         pygame.transform.set_smoothscale_backend(SSE)



if __name__ == "__main__":
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')
    mult = 1.6
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    mainMenu(c, background)
