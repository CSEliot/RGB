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
from debug import debug
from log import log  # @UnusedImport @Reimport
from ring import Ring
from scoreboard import Scoreboard
from loader import load_image, load_song
from pause import pauseScreen

class counter():
    # this class is meant to hold time variables, mostly for
    # organizational purposes.
    
    def __init__(self):
        self.timeIn = 0
        self.timeOut = 0
        self.timeList = []
        
    def getTime(self, choice):
        # get time in total seconds
        if choice == 1:
            return self.timeIn.total_seconds()
        elif choice == 2:
            return self.timeOut.total_seconds()
        elif choice == 3:
            return self.timeList
        else:
            raise Exception('time choice must be 1, 2 or 3.')
    
    def setTime(self, choice):
        if choice == 1:
            self.timeIn = datetime.datetime.now()
        elif choice == 2:
            self.timeOut = datetime.datetime.now()
        elif choice == 3:
            self.timeList.append(datetime.datetime.now())
            
    def getDelta(self, now): 
        # gives time difference of timeIn and timeOut in seconds
        # if now is true, then we will grab the timeOut also, and math it.
        if now:
            return (datetime.datetime.now() - self.timeIn).total_seconds()
        else:
            return (self.timeOut - self.timeIn).total_seconds()
    
    
def creative(c, background):

    debug(c.DEBUG, "ENTERING: creative")
    
    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)

#    pygame.key.set_repeat(0, 0)

    allSprites = pygame.sprite.Group()
    ringSprite = pygame.sprite.GroupSingle()
    scoreSprite = pygame.sprite.GroupSingle()
    '''CREATE IMAGES'''
    ring = Ring(c, c.CENTER)
    ring.add(ringSprite, allSprites)
    scoreboard = Scoreboard(c.DISPLAY_W, c.DISPLAY_H)
    scoreboard.add(scoreSprite, allSprites)
    box_img, _box_rect = load_image(c, 'letter_box.png')
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    OGBackground = background.copy()
    logging = False

    '''INSTANTIATING OTHER VARIABLES'''
    dataDir = os.path.join(c.DATA_DIR, 'newCommands.txt')
    frameCount = 0      # tracks the number of frames passed.
    bgRotAngle = 0      # background rotation angle
    logFile = file
    testFrame = 0
    newAction = True
    r = 0
    g = 0
    b = 0
    paused = False
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
    firstAction = True

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
    cmdFile = open(dataDir, 'w')
    cmdFile.write("BPM60 Play:")

    # --Main Game Loop//--
    going = True
    while going:
        

        # Paint the background
        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        """ROTATION TESTING"""
        # rotate the background, but only 15 times/second, not 30.
        # if the frame rate is 30/sec, then rotate when its an odd frame.
        if frameCount%3 == 0:
            bgRotAngle += .03
            background = pygame.transform.rotozoom(OGBackground, bgRotAngle%360 , 1)
            background_rect = background.get_rect()
            background_rect.center = c.CENTER
        frameCount += 1


        """LOGGING output information: FPS, event info, AA, etc."""
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if testFrame == c.FPS:
            debug(c.DEBUG, ("Average FPS: {0}".format(mean(fpsList))))
            debug(c.DEBUG, ("Current Score: {0}".format(scoreboard.scoreString)))
            testFrame = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []

        """Start the Song!"""
        beginning = True
        if beginning:
            pygame.mixer.music.play()
            beginning = False
            # record the beginning, since no action causes a new time recording
            counter.setTime(1)
        

        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if (event.type == KEYDOWN or event.type == KEYUP) and \
                (event.key in controls) and firstAction:
                # this is the very first action, and its a correct input,
                # we put a Wait action in, since there was nothing before the 
                # first action to tell us otherwise.
                cmdFile.write(' W%d'%counter.getDelta(True))
                # so we write how long it took to do the action above
                counter.setTime(1)
                # if any button is pressed, a change must be written in. . .
                firstAction = False
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
                # default key is R
                r = 255
                toggle_color_r = True
            elif event.type == KEYUP and event.key == controls[0]:
                r = 0
                toggle_color_r = False
            elif event.type == KEYDOWN and event.key == controls[1]:
                # default key is G
                g = 255
                toggle_color_g = True
            elif event.type == KEYUP and event.key == controls[1]:
                g = 0
                toggle_color_g = False
            elif event.type == KEYDOWN and event.key == controls[2]:
                # default key is B
                b = 255
                toggle_color_b = True
            elif event.type == KEYUP and event.key == controls[2]:
                b = 0
                toggle_color_b = False
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

        """DISPLAY SPRITE TOGGLE"""
        allSprites.update()
        if display_sprites == True:
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
        cmdFile.close()
    except Exception:
        debug(c.DEBUG, "File never opened")
    return

if __name__ == "__main__":
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')

    # CUTTING the background to fit the DISPLAYSURFACE
    background = background.subsurface((0,0), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    
    campaign(c, background)


