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


def campaign(c, background):
    
    debug(c.DEBUG, "ENTERING: campaign")
    
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
    dieingSprites = pygame.sprite.GroupSingle()
    scoreSprite = pygame.sprite.GroupSingle()
    pBox = playBox()
    playList = commander(c)
    playIt = iter(playList)
    '''CREATE IMAGES'''
    ring = Ring(c, c.CENTER)
    ring.add(ringSprite, allSprites)
    scoreboard = Scoreboard(c.DISPLAY_W, c.DISPLAY_H)
    scoreboard.add(scoreSprite, allSprites)
    box_img, _box_rect = load_image(c, 'campaign/letter_box.png')
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    OGBackground = background.copy()
    logging = False

    '''INSTANTIATING OTHER VARIABLES'''
    frameCount = 0      # tracks the number of frames passed.
    bgRotAngle = 0      # background rotation angle
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
    startTime = 0

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
    splashInfo, splashInfo_rect = load_image(c, 'campaign/splashInfo.png')

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
        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        """ROTATION TESTING"""
        # rotate the background, but only 15 times/second, not 30.
        # if the frame rate is 30/sec, then rotate when its an odd frame.
        #=======================================================================
        # if frameCount%5 == 0:
        #     bgRotAngle += .03
        #     background = pygame.transform.rotozoom(OGBackground, bgRotAngle%360 , 1)
        #     background_rect = background.get_rect()
        #     background_rect.center = c.CENTER
        # frameCount += 1
        #=======================================================================


        """LOGGING output information: FPS, event info, AA, etc."""
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if testFrame == c.FPS:
            debug(c.DEBUG, ("Average FPS: {0}".format(mean(fpsList))))
            debug(c.DEBUG, ("Current Score: {0}".format(scoreboard.scoreString)))
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
            elif action[0] == 'J':
                startTime = action[1]
            elif action[0] == 'P':
                pygame.mixer.music.play(1, startTime)
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
                    now = datetime.datetime.now()
                    waiting = True
                    waitMade = datetime.datetime.now()
                elif action[0] == 'WG':
                    pBox.cWait = action[1]
                    pBox.fWait = action[1]
                elif action[0] == 'WC':
                    pBox.cWait = action[1]
                elif action[0] == 'WF':
                    pBox.fWait = action[1]
            elif action[0] == 'S':
                pygame.mixer.music.stop()
                going = False
        if waiting:
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
                    circMade = datetime.datetime.now()
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
                change = datetime.datetime.now() - now
                # if the action is to JUST wait x amount of time
                if change.total_seconds() >= action[1] / 30.0:
                    waiting = False
                    totalWaitTime = datetime.datetime.now() - waitMade 
                    debug(c.DEBUG, ("Wait Time: ", totalWaitTime.total_seconds()))
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
                pygame.quit()
                sys.exit()
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
                # catchable becomes true when the circle comes in contact 
                # with the ring.
                debug(c.DEBUG, (circle.color, (r, g, b)))
                circle.add(caughtSprite)
                circle.remove(circSprites)
                circle.catch()
                totalCircTime = datetime.datetime.now() - circMade

        """REPEATED POINTS HOLDING COLORS CAUGHT"""
        # every .1 seconds should add or remove points based on accuracy
        if not (caughtSprite.sprite is None):
            for circle in caughtSprite.sprites():
                if circle.color == (r, g, b) and not(circle.dieing):
                    debug(c.DEBUG, ("CIRCTIME: ", totalCircTime.total_seconds()))
                    #if the circle is more than 1 color, than we give bonus
                    if circle.color[0]+circle.color[1]+circle.color[2] >255:
                        scoreboard.addScore(40)
                    else:
                        scoreboard.addScore(20)
                    circle.remove(caughtSprite)
                    circle.add(dieingSprites)
                else:
                    circle.remove(caughtSprite)
                    circle.add(dieingSprites)
                    scoreboard.addScore(-10)


        # a circle begins in circSprites, then hits the ring, gets caught, and
        # goes into "caughtSprite" group. From there, it tries to match with
        # the user's input, then dies and goes into the "dieingCircs" group.
        # the purpose of the last group is just to have it animate the fading
        # or "dieing" sequence before disappearing.
        for circle in dieingSprites.sprites():
            circle.death()



        """DELETE FREE STARS SHOOTING"""
        for star in starSprites.sprites():
            if star.travDist >= 255:
                if not(ringSprite.sprite.angle == star.angleDeg):
                    star.kill()
                    scoreboard.addScore(-30)
            elif star.shooting:
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
#         for sprite in killGroup:
#             scoreboard.addScore(-30)
#             sprite.kill()


        """DISPLAY SPRITE TOGGLE"""
        allSprites.update()
        if display_sprites == True:
            dieingSprites.draw(c.DISPLAYSURFACE)
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


    return

if __name__ == "__main__":
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')

    # CUTTING the background to fit the DISPLAYSURFACE
    background = background.subsurface((0,0), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    
    campaign(c, background)


