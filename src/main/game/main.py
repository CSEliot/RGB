#===============================================================================
# File:   RGB - alpha
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.
#===============================================================================

import pygame, sys, os,  datetime, platform # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface # @UnusedImport
from numpy import *# @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror # @UnusedImport
import math as m # @UnusedImport
from constants import Constants 
from commander import commander 
from debug import debug
from log import log
from circle import Circle
import circle
from loader import load_image, load_song
os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'


c = Constants()






class playBox():
    #This class holds all our variables to access while playing.
    def __init__(self):
        self.cSpeed = 0
        self.fSpeed = 0
        self.cWait = 0
        self.fWait = 0
        self.isPlaying = False
        self.isFirst = True
        self.layer = 0


def main():
    
    pBox = playBox()
    playList = commander(c)
    playIt = iter(playList)
    '''CREATE IMAGES'''
    circ_img, __ = load_image(c, 'R_small.png')
    ring_img, ring_rect = load_image(c, 'ringNew.png')
    ring_rect.center = c.CENTER
    box_img, box_rect = load_image(c, 'letter_box.png')
    background, background_rect = load_image(c, 'starBG.png')
    fadeBG, _ = load_image(c, 'fadeBG.png')
    mySong = load_song(c, 'song.ogg')
    # CUTTING the background to fit the DISPLAYSURFACE
    # take the center's x value, and move it left to the end of the display's
    # edge, so from center, minus the half value of width (CENTER_X) is the edge
    xCut = background_rect.centerx - c.CENTER_X
    yCut = background_rect.centery - c.CENTER_Y
    background = background.subsurface((xCut, yCut), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    # CUTTING the same way for the fadeBG.png
    fadeBG = fadeBG.subsurface((xCut, yCut), (c.DISPLAY_W, c.DISPLAY_H))
    fadeBG_rect = fadeBG.get_rect()
    fadeBG_rect.center = c.CENTER

    '''INSTANTIATING OTHER VARIABLES'''
    # tracks the number of frames passed. Gets reset when == to FPS.
    mainFrame = 0
    testFrame = 0
    waiting = False
    firstAction = True
    r = 0
    g = 0
    b = 0
    angle = 0
    rotate_by = 0
    paused = False
    total_input = 0
    fpsList = []
    circle_size_list = []
    circle_color_list = []
    toggle_color_r = False
    toggle_color_g = False
    toggle_color_b = False
    display_sprites = True
    current_circle_quantity = 0
    inverted = False
    rotation_speed = 3
    allSprites = pygame.sprite.Group()
    circSprites = pygame.sprite.LayeredUpdates()
    buttonSprites = pygame.sprite.Group()
    starSprites = pygame.sprite.LayeredUpdates()
    
    
    
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

    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)

    # --Main Game Loop//--
    going = True
    while going:
        testFrame += 1
        mainFrame += 1
        # Paint the background
        c.DISPLAYSURFACE.blit(background, background_rect)

        """RECORD UNCHANGED RGB"""
        # record unchanged r, g, b values.
        old_rgb = [r, g, b]

        """LOGGING output information: FPS, event info, AA, etc."""
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if testFrame == c.FPS:
            debug(c.DEBUG, (mean(fpsList)))
            testFrame = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []
            if len(circle_size_list) > 0:
                debug(c.DEBUG, 'Size: ' + str(circle_size_list[0]))
            
        
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
            if action[0] == 'C':
                if mainFrame >= c.FPS*pBox.cWait or firstAction:
                    if action[2] == '':
                        # if there is no given speed, then it's the general
                        # speed. . .
                        tempSpeed = pBox.cSpeed
                    else:
                        tempSpeed = action[2]
                    tempColor = action[1]
                    tempCirc = Circle(c.CENTER, tempSpeed, tempColor, circ_img,\
                                       pBox.layer)
                    circSprites.add(tempCirc)
                    #allSprites.add(tempCirc)
                    pBox.layer += 1
                    waiting = False
                    mainFrame = 0
            firstAction = False
                    
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_r:
                r = 255
                toggle_color_r = True
                total_input += 1
            elif event.type == KEYUP and event.key == K_r:
                r = 0
                toggle_color_r = False
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_g:
                g = 255
                toggle_color_g = True
                total_input += 1
            elif event.type == KEYUP and event.key == K_g:
                g = 0
                toggle_color_g = False
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_b:
                b = 255
                toggle_color_b = True
                total_input += 1
            elif event.type == KEYUP and event.key == K_b:
                b = 0
                toggle_color_b = False
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_o:
                if inverted == False:
                    inverted = True
                else:
                    inverted = False
            # Ring Spinning
            elif event.type == KEYDOWN and event.key == K_LEFT:
                rotate_by += -rotation_speed
                # ring.set_direction(1)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                rotate_by += rotation_speed
                # ring.set_direction(-1)
            elif event.type == KEYUP and event.key == K_LEFT:
                rotate_by += rotation_speed
                # ring.set_direction
            elif event.type == KEYUP and event.key == K_RIGHT:
                rotate_by += -rotation_speed
            #====================================
            # --non-game-play events//--
            #====================================
            # if I is pressed, toggle context display
            elif event.type == KEYDOWN and event.key == K_i:
                if display_sprites == True:
                    display_sprites = False
                else:
                    display_sprites = True
            # if Q is pressed, print output to file log.txt
            elif event.type == KEYDOWN and event.key == K_q:
                if c.DEBUG == True:
                    logFile = log(c)
                    c.DEBUG = True
                else:
                    c.DEBUG = True
                    logFile.close()
            # if P is pressed, pause game.
            elif event.type == KEYUP and event.key == K_p:
                pygame.event.pump()
                keyPressed = pygame.key.get_pressed()
                if keyPressed:
                    debug(c.DEBUG, "A KEY IS PRESSED, CAN NOT PAUSE")
                    paused = False
                else:
                    paused = True
                    debug(c.DEBUG, "INTO PAUSE!!")
            # if L is pressed, toggle black auto-black circle.
            elif event.type == KEYDOWN and event.key == K_l:
                if total_input == 0:
                    total_input = 100
                else:
                    total_input = 0

            """LOGGING of inputs"""
            if event.type == KEYDOWN or event.type == KEYUP:
                debug(c.DEBUG, event.dict)
        # --function controls//--
        # if paused is set to true, wait for p to be pressed again.
        """PAUSE WAIT STOP"""
        while paused:
                x_event = pygame.event.wait()
                if x_event.type == KEYUP and event.key == K_p:
                    pygame.event.pump()
                    for p in pygame.key.get_pressed():
                        if p == True:
                            debug(c.DEBUG, "A KEY IS PRESSED, CAN NOT UNPAUSE")
                            paused = True
                            # break
                        else:
                            paused = False
                            debug(c.DEBUG, "OUT OF PAUSE!")
                if x_event.type == QUIT:
                    sys.exit()
                    pygame.quit()
                elif x_event.type == KEYDOWN and x_event.key == K_ESCAPE:
                    sys.exit()
                    pygame.quit()

        
        """SPIN ROTATE"""
        oldAngle = angle
        # --Spin the Ring//--
        if inverted == True:
            angle += -rotate_by * 2
        else:
            angle += rotate_by * 2
        # ring_imgNew = pygame.transform.scale(ring_img, (angle, angle))
        ring_imgNew = pygame.transform.rotozoom(ring_img, angle, 1)
        ring_rectNew = ring_imgNew.get_rect(center=(c.CENTER_X, c.CENTER_Y))

        """RECORD CHANGES RGB"""
        # record the changes to R, G, and B
        new_rgb = [r, g, b]

        """ADD NEW CIRCLES LISTS"""
        # if the color to print has not changed, a new circle will not be made
        if total_input > 0:
            if not new_rgb == old_rgb:
                    circle_color_list.append(new_rgb)
                    circle_size_list.append(0)
                    current_circle_quantity += 1

        """POP DELETE LARGE CIRCLES"""
        # get rid of big circles
        if len(circSprites.sprites()) > 0:
            if len(circSprites.sprites()) >= 4:
                print circSprites.get_sprite(0).size
                print circSprites.get_sprite(0).color
                print circSprites.get_sprite(1).size
                print circSprites.get_sprite(1).color
            tempSize = circSprites.get_top_sprite().size
            tempLen = len(circSprites.sprites())
            debug(c.DEBUG, ('Sprite Size: ', tempSize))
            debug(c.DEBUG, ('# Sprites: ', len(circSprites.sprites())) )
            if circSprites.get_top_sprite().size >= 265:
                debug(c.DEBUG, ('# Sprites: ', len(circSprites.sprites())) )
                circSprites.get_top_sprite().kill()

        """DISPLAY SPRITE TOGGLE"""
        if display_sprites == True:
            circSprites.update()

            circSprites.draw(c.DISPLAYSURFACE)
#             if not(len(circle_size_list) == 0):
#                 if circle_size_list[0] > 265:
#                     c.DISPLAYSURFACE.blit(fadeBG, fadeBG_rect)
            c.DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            if toggle_color_r:
                c.DISPLAYSURFACE.blit(r_letter, r_letter_rect)
            if toggle_color_g:
                c.DISPLAYSURFACE.blit(g_letter, g_letter_rect)
            if toggle_color_b:
                c.DISPLAYSURFACE.blit(b_letter, b_letter_rect)
            c.DISPLAYSURFACE.blit(box_img, box_rectR)
            c.DISPLAYSURFACE.blit(box_img, box_rectG)
            c.DISPLAYSURFACE.blit(box_img, box_rectB)
            c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)

        """UPDATE AND DELAY"""
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip() #update()

    try:
        logFile.close()
    except Exception:
        debug(c.DEBUG, "File never opened")
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
