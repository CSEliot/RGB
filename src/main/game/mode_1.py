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
from constants import Constants
from commander import commander
from debug import debug
from log import log  # @UnusedImport @Reimport
from circle import Circle
from star import Star
from ring import Ring
from scoreboard import Scoreboard
from loader import load_image, load_song
from pause import pauseScreen




class playBox():
    # This class holds all our variables to access while playing.
    def __init__(self):
        self.cSpeed = 0
        self.fSpeed = 0
        self.cWait = 0
        self.fWait = 0
        self.isPlaying = False
        self.isFirst = True
        self.layer = 0


def game(c, background):
    
    
    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)

#    pygame.key.set_repeat(0, 0)

    allSprites = pygame.sprite.Group()
    ringSprite = pygame.sprite.GroupSingle()
    circSprites = pygame.sprite.LayeredUpdates()
    buttonSprites = pygame.sprite.Group()  # @UnusedVariable
    starSprites = pygame.sprite.LayeredUpdates()
    caughtSprite = pygame.sprite.GroupSingle()
    scoreSprite = pygame.sprite.GroupSingle()
    pBox = playBox()
    playList = commander(c)
    playIt = iter(playList)
    '''CREATE IMAGES'''
    ring = Ring(c, c.CENTER)
    ring.add(ringSprite, allSprites)
    scoreboard = Scoreboard(c.DISPLAY_W, c.DISPLAY_H)
    scoreboard.add(scoreSprite, allSprites)
    box_img, _box_rect = load_image(c, 'letter_box.png')
    # CUTTING the background to fit the DISPLAYSURFACE
    # take the center's x value, and move it left to the end of the display's
    # edge, so from center, minus the half value of width (CENTER_X) is the edge
    #     xCut = background_rect.centerx - c.CENTER_X
    #     yCut = background_rect.centery - c.CENTER_Y
    #     background = background.subsurface((xCut, yCut), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    OGBackground = background.copy()
    logging = False

    '''INSTANTIATING OTHER VARIABLES'''
    # tracks the number of frames passed. Gets reset when == to FPS.
    bgRotAngle = 0
    frameCount = 0
    logFile = file
    mainFrame = 0
    testFrame = 0
    waiting = False
    firstAction = True
    r = 0
    g = 0
    b = 0
    paused = False
    total_input = 0
    fpsList = []
    toggle_color_r = False
    toggle_color_g = False
    toggle_color_b = False
    display_sprites = True
    controls = c.CONTROL_LIST
    leftHold = False
    rightHold = False
    upHold = False
    downHold = False
    quitGame = False  # if user returns a True from pause, we quit game, etc.


    """BUTTON / SPRITE RENDERING"""
    r_letter = c.FONT_LARGE.render('R', True, c.RED)
    r_letter.scroll(2, 0)
    r_letter_rect = r_letter.get_rect()
    r_letter_rect.center = (c.CENTER_X - 50, (c.CENTER_Y * 2) - 20)
    box_rectR = r_letter_rect

    g_letter = c.FONT_LARGE.render('G', True, c.GREEN)
    g_letter.scroll(1, 0)
    g_letter_rect = g_letter.get_rect()
    g_letter_rect.center = (c.CENTER_X, (c.CENTER_Y * 2) - 20)
    box_rectG = g_letter_rect

    b_letter = c.FONT_LARGE.render('B', True, c.BLUE)
    b_letter.scroll(2, 0)
    b_letter_rect = b_letter.get_rect()
    b_letter_rect.center = (c.CENTER_X + 50, (c.CENTER_Y * 2) - 20)
    box_rectB = b_letter_rect




    # throw down splash screen before beginning
    splashInfo, splashInfo_rect = load_image(c, 'splashInfo.png')
    # adjusting image cuz i can't make images.
    splashInfo_rect.center = (c.CENTER_X - 50, c.CENTER_Y)

    # fade info in and out
    fade = 0
    pgext.color.setAlpha(splashInfo, fade, 1)
    pygame.event.clear()
    # fade in
    inInfoScreen = True
    for fade in range(255):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(splashInfo, splashInfo_rect)
        pgext.color.setAlpha(splashInfo, fade, 1)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False
            break
    # if the info is still being read/no button pressed, just wait.
    while inInfoScreen:
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False
    fade = 255
    pgext.color.setAlpha(splashInfo, fade, 1)
    load_song(c, "It's Melting.ogg")  # stops other music from playing too


    # --Main Game Loop//--
    going = True
    while going:
        testFrame += 1
        mainFrame += 1
        # Paint the background
        c.DISPLAYSURFACE.blit(background, background_rect)
        """ROTATION TESTING"""
        # rotate the background, but only 15 times/second, not 30.
        # if the frame rate is 30/sec, then rotate when its an odd frame.
        if frameCount%5 == 0:
            bgRotAngle += .05
            background = pygame.transform.rotozoom(OGBackground, bgRotAngle%360 , 1)
            background_rect = background.get_rect()
            background_rect.center = c.CENTER
        frameCount += 1


        """LOGGING output information: FPS, event info, AA, etc."""
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if testFrame == c.FPS:
            debug(c.DEBUG, (mean(fpsList)))
            debug(c.DEBUG, scoreboard.scoreString)
            testFrame = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []


        """TAKE ACTION COMMAND LIST"""
        # for every new action, if the wait was long enough, perform the action
        if not waiting:
            action = playIt.next()
            if action[0] == 'B':
                # if the command is BPM, set the proper variables.
                pBox.cWait = action[1]
                pBox.fWait = action[2]
                pBox.cSpeed = action[3]
                pBox.fSpeed = action[4]
            elif action[0] == 'P':
                now = datetime.datetime.now()
                pygame.mixer.music.play()
            # if the action is to spawn a circle/star, gotta que it up.
            elif action[0] == 'C' or action[0] == 'F':
                waiting = True
            # change the general speed for circles/stars
            elif action[0] == 'CS'or action[0] == 'FS':
                if action[0] == 'CS':
                    pBox.cSpeed = action[1]
                else:
                    pBox.fSpeed = action[1]
                    debug(c.DEBUG, ('Star speed set to: ', action[1]))
            elif action[0][0] == 'W':
                if action[0] == 'W':
                    waiting = True
                elif action[0] == 'WG':
                    pBox.cWait = action[1]
                    pBox.fWait = action[1]
                elif action[0] == 'WC':
                    pBox.cWait = action[1]
                else:
                    pBox.fWait = action[1]
            elif action[0] == 'S':
                pygame.mixer.music.stop()
        if waiting:
            change = datetime.datetime.now() - now
            if action[0] == 'C':
                if mainFrame >= pBox.cWait or firstAction:
                    if action[2] == '':
                        # if there is no given speed, then it's the general
                        # speed. . .
                        tempSpeed = pBox.cSpeed
                    else:
                        tempSpeed = action[2]
                    tempColor = action[1]
                    tempCirc = Circle(c, c.CENTER, tempSpeed, tempColor, \
                                      pBox.layer)
                    tempCirc.add(circSprites, allSprites)
                    # circSprites.add(tempCirc)
                    # allSprites.add(tempCirc)
                    pBox.layer += 1
                    waiting = False
                    mainFrame = 0
            elif action[0] == 'F':
                if mainFrame >= pBox.fWait or firstAction:
                    if action[2] == '':
                        tempSpeed = pBox.fSpeed
                    else:
                        tempSpeed = action[2]
                    tempAngle = action[1]
                    tempStar = Star(c, c.CENTER, tempSpeed, tempAngle)
                    tempStar.add(starSprites, allSprites)
                    # no longer waiting, bring on the next action!
                    waiting = False
                    mainFrame = 0
            elif action[0] == 'W':
                # if the action is to JUST wait x amount of time
                print "LINE 213: ", change.total_seconds(), action[1] / 30.0
                if change.total_seconds() >= action[1] / 30.0:
                    waiting = False
                    mainFrame = 0
                    # we must also set the wait for the next action to 0,
                    # or else the wait would be Wx + Wcircle/star.
                    firstAction = True
            # since the first action has just occurred, we must wait now.
            if firstAction:
                firstAction = False


        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                if c.DEBUG:
                    going = False
                else:
                    paused = True
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == controls[0]:
                r = 255
                toggle_color_r = True
                total_input += 1
            elif event.type == KEYUP and event.key == controls[0]:
                r = 0
                toggle_color_r = False
                total_input += -1
            elif event.type == KEYDOWN and event.key == controls[1]:
                g = 255
                toggle_color_g = True
                total_input += 1
            elif event.type == KEYUP and event.key == controls[1]:
                g = 0
                toggle_color_g = False
                total_input += -1
            elif event.type == KEYDOWN and event.key == controls[2]:
                b = 255
                toggle_color_b = True
                total_input += 1
            elif event.type == KEYUP and event.key == controls[2]:
                b = 0
                toggle_color_b = False
                total_input += -1
            # Ring Spinning
            elif event.type == KEYDOWN and event.key == controls[5]:
                leftHold = True
                if upHold:
                    ring.spin('upleft')
                elif downHold:
                    ring.spin('downleft')
                else:
                    ring.spin('left')
            elif event.type == KEYUP and event.key == controls[5]:
                leftHold = False
            elif event.type == KEYDOWN and event.key == controls[6]:
                rightHold = True
                if upHold:
                    ring.spin('upright')
                elif downHold:
                    ring.spin('downright')
                else:
                    ring.spin('right')
            elif event.type == KEYUP and event.key == controls[6]:
                rightHold = False
            elif event.type == KEYDOWN and event.key == controls[3]:
                upHold = True
                if leftHold:
                    ring.spin('upleft')
                elif rightHold:
                    ring.spin('upright')
                else:
                    ring.spin('up')
            elif event.type == KEYUP and event.key == controls[3]:
                upHold = False
            elif event.type == KEYDOWN and event.key == controls[4]:
                downHold = True
                if leftHold:
                    ring.spin('downleft')
                elif rightHold:
                    ring.spin('downright')
                else:
                    ring.spin('down')
            elif event.type == KEYUP and event.key == controls[4]:
                downHold = False

            #====================================
            # --non-game-play events//--
            #====================================
            # if O is pressed, toggle context display -------TO BE REMOVED SOON
            elif event.type == KEYDOWN and event.key == K_o:
                if display_sprites == True:
                    display_sprites = False
                else:
                    display_sprites = True
            # if I is pressed, print output to file log.txt
            elif event.type == KEYDOWN and event.key == controls[8]:
                if logging:
                    log(c)
                    try:
                        logFile.close()
                    except:
                        raise
                    c.DEBUG = False
                    logging = False
                else:
                    logging = True
                    c.DEBUG = True
                    logFile = log(c)
            # if P is pressed, pause game.
            elif event.type == KEYUP and event.key == controls[7]:
                paused = True

            """LOGGING of inputs"""
            if event.type == KEYDOWN or event.type == KEYUP:
                debug(c.DEBUG, event.dict)

        """CATCH CIRCLES MATCHING COLORS"""
        # catch matching circles!!
        for circle in circSprites.sprites():
            if circle.catchable:
                debug(c.DEBUG, (circle.color, (r, g, b)))
                if circle.color == (r, g, b):
                    circle.remove(circSprites)
                    circle.add(caughtSprite)
                    scoreboard.addScore(200)
                else:
                    circle.catch()
                    scoreboard.addScore(-10)
                    #circle.remove(circSprites)
                    #circle.add(caughtSprite)

        """REPEATED POINTS HOLDING COLORS"""
        # every .1 seconds should add or remove points based on accuracy
        if not caughtSprite.sprite is None:
            for circle in caughtSprite.sprites():
                circle.catch()
                circle.remove(caughtSprite)
            #===================================================================
            # if caughtSprite.sprite.color == (r, g, b):
            #     scoreboard.addScore(1)
            # else:
            #     scoreboard.addScore(-1)
            #===================================================================





        """DELETE FREE STARS SHOOTING"""
        for star in starSprites.sprites():
            if star.shooting:
                debug(c.DEBUG, 'I AM SHOOTING1!')
                # if the star has gone off the screen in the x or y direction
                # kill it and add points!!
                if star.pos[0] > c.DISPLAY_W or star.pos[0] < 0:
                    star.kill()
                    debug(c.DEBUG, 'KILLED A STAR')
                    scoreboard.addScore(50)
                elif star.pos[1] > c.DISPLAY_H or star.pos[1] < 0:
                    star.kill()
                    debug(c.DEBUG, 'KILLED A STAR')
                    scoreboard.addScore(50)
            debug(c.DEBUG, ('Stars #: ', len(starSprites.sprites())))


        """KILL STARS COLLISION DETECTION"""
        killGroup = pygame.sprite.spritecollide(ring, starSprites, False, \
                                    pygame.sprite.collide_mask)
        for sprite in killGroup:
            scoreboard.addScore(-300)
            sprite.kill()


        """DISPLAY SPRITE TOGGLE"""
        allSprites.update()
        if display_sprites == True:
            caughtSprite.draw(c.DISPLAYSURFACE)
            circSprites.draw(c.DISPLAYSURFACE)
            starSprites.draw(c.DISPLAYSURFACE)
            ringSprite.draw(c.DISPLAYSURFACE)
            if toggle_color_r:
                c.DISPLAYSURFACE.blit(r_letter, r_letter_rect)
            if toggle_color_g:
                c.DISPLAYSURFACE.blit(g_letter, g_letter_rect)
            if toggle_color_b:
                c.DISPLAYSURFACE.blit(b_letter, b_letter_rect)
            c.DISPLAYSURFACE.blit(box_img, box_rectR)
            c.DISPLAYSURFACE.blit(box_img, box_rectG)
            c.DISPLAYSURFACE.blit(box_img, box_rectB)
            scoreSprite.draw(c.DISPLAYSURFACE)
            c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)

        """DELAY"""
        c.FPSCLOCK.tick_busy_loop(c.FPS)

        """PAUSE UNPAUSE"""
        if paused:
            pygame.mixer.music.pause()
            quitGame = pauseScreen(c)
            if quitGame == 3:
                going = False
            pygame.mixer.music.unpause()
            paused = False

        """UPDATE"""
        pygame.display.flip()  # update()

    try:
        logFile.close()
    except Exception:
        debug(c.DEBUG, "File never opened")
    return

if __name__ == "__main__":
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')

    # CUTTING the background to fit the DISPLAYSURFACE
    #     background = background.subsurface((0,0), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    
    game(c, background)


