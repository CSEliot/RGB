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
os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'


c = Constants()



# --FUNCTIONS to create our resources//--
def load_image(name, colorkey=None):
    fullname = os.path.join(c.GFX_DIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        debug(c.DEBUG, ('Cannot load image:', fullname))
        raise SystemExit(str(geterror()))
    # image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    return image.convert_alpha(), image.get_rect()





def main():
    
    playList = commander(c)
    '''CREATE IMAGES'''
    circ_img, __ = load_image('R_small.png')
    ring_img, ring_rect = load_image('ring_silver.png')
    ring_rect.center = c.CENTER
    box_img, box_rect = load_image('letter_box.png')
    background, background_rect = load_image('starBG.png')
    fadeBG, _ = load_image('fadeBG.png')
    # circle = Circle()
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
    frame = 0
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
    cSpeed = 3
    allSprites = pygame.sprite.Group()
    circSprites = pygame.sprite.Group()
    buttonSprites = pygame.sprite.Group()
    starSprites = pygame.sprite.Group()
    
    
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
        # Paint the background
        c.DISPLAYSURFACE.blit(background, background_rect)

        """RECORD UNCHANGED RGB"""
        # record unchanged r, g, b values.
        old_rgb = [r, g, b]

        """LOGGING output information: FPS, event info, AA, etc."""
        frame += 1
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if frame == c.FPS:
            debug(c.DEBUG, (mean(fpsList)))
            frame = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []
            if len(circle_size_list) > 0:
                debug(c.DEBUG, 'Size: ' + str(circle_size_list[0]))
            

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
                for p in pygame.key.get_pressed():
                        if p == True:
                            debug(c.DEBUG, "A KEY IS PRESSED, CAN NOT PAUSE")
                            paused = False
                            # break
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

        """DRAW CIRCLES SCREEN DISPLAYSURFACE"""
        # for each circle to be drawn
        for i in range(current_circle_quantity):
            # increase the circle size
            circle_size_list[i] += cSpeed
            # draw circle to the screen, grabbing each color amount: R, G, B
            pygame.gfxdraw.filled_circle(c.DISPLAYSURFACE,
                                         c.CENTER_X, c.CENTER_Y,
                                         circle_size_list[i], (
                                         circle_color_list[i][0],
                                         circle_color_list[i][1],
                                         circle_color_list[i][2]))
        """POP DELETE LARGE CIRCLES"""
        # get rid of big circles
        if len(circle_size_list) >= 1:
            if circle_size_list[0] >= 265:
                circle_size_list.pop(0)
                allSprites.empty()
                # DISPLAYSURFACE.blit(background, background_rect)
                # paint the background to the color of the last circle
                circle_color_list.pop(0)
                current_circle_quantity += -1







        """DISPLAY SPRITE TOGGLE"""
        if display_sprites == True:
            allSprites.update()

            allSprites.draw(c.DISPLAYSURFACE)
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
