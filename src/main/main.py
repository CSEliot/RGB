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
from constants import Constants # @UnusedImport
from commander import commander 
from debug import debug

os.environ['SDL_VIDEO_CENTERED'] = '1'
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()

'''
_______________________________________________________________________________
KEY:

"""KEYWORDS""" -For quick code finding, a few key words are entered in all caps

#explanation   -A short description of the code, sometimes in pseudo-code

#--title//--   -A separation of specific sections.
_______________________________________________________________________________
'''


"""FULLSCREEN ON STARTUP?"""
FULLSCREEN_RES = False
"""||||||||||||||||||||||"""

"""SCREEN INFORMATION"""
user_screen_data = pygame.display.Info()
window_width = user_screen_data.current_w
window_height = user_screen_data.current_h
pygame.display.set_caption('RGB - Beta v1.00')

def make_gamescreen():
    # Making a screen, w/ 4 different possible outcomes.
    if FULLSCREEN_RES == True:
        try:
            options = (FULLSCREEN | DOUBLEBUF | HWSURFACE)
            std_res = (window_width, window_height)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 1"
            screenError = "Window Error: None"
        except Exception as e:
            options = 0
            std_res = (window_width - 100, window_height - 100)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 2"
            screenError = "Window Error {0}: {1}".format(e.errno, e.strerror)
    else:
        try:
            options = 0
            std_res = (1000, 700)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 3"
            screenError = "Window Error: None"
        except Exception as e:
            # If for some reason this resolution does not fit user's display it will
            # fit to their native resolution.
            options = 0
            std_res = (window_width - 100, window_height - 100)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 4"
            screenError = "Window Error {0}: {1}".format(e.errno, e.strerror)
    return DISPLAYSURFACE, whichDisplay, screenError

DISPLAYSURFACE, whichDisplay, screenError = make_gamescreen()
c = Constants(DISPLAYSURFACE)

DEBUG = True


# class Ring(pygame.sprite.Sprite):
#
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)
#        self.image, self.rect = load_image('ring.png', -1)
#        self.MAX_COLLIDE_SIZE = 290
#        self.MIN_COLLIDE_SIZE = 280
#        self.angle = 0.0
#        self.rotate_by = 0.0
#        self.rotation_speed = 2
#
#    def set_direction(self, direction):  # 1 for left, -1 for right
#        if direction == -1:
#            self.rotate_by += self.rotation_speed
#
#
#
#    def spin(self):  # Will change ring angle, based on direction
#        # --Spin the Ring//--
#        if self.direction == -1:
#            self.angle += -self.rotate_by * 2
#        else:
#            self.angle += self.rotate_by * 2
#        ring_rectNew = ring_imgNew.get_rect(center=(CENTER_X, CENTER_Y))
class Circle (pygame.sprite.Sprite):

    def __init__(self, speed, color, image):
        pygame.sprite.Sprite.__init__(self)
        self.size = 1
        self.color = color
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = c.CENTER
        self.imageOG = self.image
        self.speed = speed
        #pgext.color.setColor(self.image, self.color)

    def update(self):
        self.size += int(self.speed)
        self.image = pygame.transform.smoothscale(self.imageOG, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = c.CENTER

# --FUNCTIONS to create our resources//--
def load_image(name, colorkey=None):
    fullname = os.path.join(c.DATA_DIR, name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error:
        debug(DEBUG, ('Cannot load image:', fullname))
        raise SystemExit(str(geterror()))
    # image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



def log(orig_stdout, rep_log):
    saveDir = os.path.join(c.DATA_DIR, 'log.txt')
    # --TESTING the full-screen function//--
    for i in range(2):  # @UnusedVariable
        try:
            # toggle_fullscreen returns a 1/0 based on if it worked
            attempt_fullscreen = pygame.display.toggle_fullscreen()
            scn_tst = "About the full-screen, there were no errors boss!"
        except Exception as e:
            attempt_fullscreen = "Fullscreen Failed"
            scn_tst = "Full-screen error({0}): {1}".format(e.errno, e.strerror)
    # --LOGGING
    if orig_stdout == sys.stdout:
        rep_log = open(saveDir, 'a')
        sys.stdout = rep_log
        debug(DEBUG, "LOGGING TO FILE BEGINNING--")
        debug(DEBUG, c.DATE)
        debug(DEBUG, "Display Info: {0}, {1}".format(whichDisplay, screenError))
        debug(DEBUG, (attempt_fullscreen, scn_tst))
        return rep_log
    else:
        debug(DEBUG, "LOGGING TO FILE ENDING--")
        sys.stdout = orig_stdout
        rep_log.close()
        


def main():
    
    playList = commander(c)
    DEBUG = False
    '''CREATE IMAGES'''
    circ_img, __ = load_image('R_small.png')
    ring_img, ring_rect = load_image('ring_silver.png')
    ring_rect.center = c.CENTER
    box_img, box_rect = load_image('letter_box.png')
    background, background_rect = load_image('starBG.png')
    fadeBG, _ = load_image('fadeBG.png')
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
    command_list = []
    rep_log = file.__class__  # logging file
    orig_stdout = sys.stdout
    current_circle_quantity = 0
    inverted = False
    rotation_speed = 3
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
        DISPLAYSURFACE.blit(background, background_rect)

        """RECORD UNCHANGED RGB"""
        # record unchanged r, g, b values.
        old_rgb = [r, g, b]

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
                rep_log = log(orig_stdout, rep_log)
                DEBUG = True
            # if P is pressed, pause game.
            elif event.type == KEYUP and event.key == K_p:
                pygame.event.pump()
                for p in pygame.key.get_pressed():
                        if p == True:
                            debug(DEBUG, "A KEY IS PRESSED, CAN NOT PAUSE")
                            paused = False
                            # break
                        else:
                            paused = True
                            debug(DEBUG, "INTO PAUSE!!")
            # if L is pressed, toggle black auto-black circle.
            elif event.type == KEYDOWN and event.key == K_l:
                if total_input == 0:
                    total_input = 100
                else:
                    total_input = 0

            """LOGGING of inputs"""
            if event.type == KEYDOWN or event.type == KEYUP:
                debug(DEBUG, event.dict)

        # --function controls//--
        # if paused is set to true, wait for p to be pressed again.
        """PAUSE WAIT STOP"""
        while paused:
                x_event = pygame.event.wait()
                if x_event.type == KEYUP and event.key == K_p:
                    pygame.event.pump()
                    for p in pygame.key.get_pressed():
                        if p == True:
                            debug(DEBUG, "A KEY IS PRESSED, CAN NOT UNPAUSE")
                            paused = True
                            # break
                        else:
                            paused = False
                            debug(DEBUG, "OUT OF PAUSE!")
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
            circle_size_list[i] += c.CIRCLE_GROWTH_SPEED
            # draw circle to the screen, grabbing each color amount: R, G, B
            pygame.gfxdraw.filled_circle(DISPLAYSURFACE,
                                         c.CENTER_X, c.CENTER_Y,
                                         circle_size_list[i], (
                                         circle_color_list[i][0],
                                         circle_color_list[i][1],
                                         circle_color_list[i][2]))
        """POP DELETE LARGE CIRCLES"""
        # get rid of big circles
        if len(circle_size_list) >= 1:
            if circle_size_list[0] >= c.C_LENGTH / 2:
                circle_size_list.pop(0)
                allSprites.empty()
                # DISPLAYSURFACE.blit(background, background_rect)
                # paint the background to the color of the last circle
                circle_color_list.pop(0)
                current_circle_quantity += -1







        """DISPLAY SPRITE TOGGLE"""
        if display_sprites == True:
            allSprites.update()

            allSprites.draw(DISPLAYSURFACE)
            if not(len(circle_size_list) == 0):
                if circle_size_list[0] > 300:
                    DISPLAYSURFACE.blit(fadeBG, fadeBG_rect)
            DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            if toggle_color_r:
                DISPLAYSURFACE.blit(r_letter, r_letter_rect)
            if toggle_color_g:
                DISPLAYSURFACE.blit(g_letter, g_letter_rect)
            if toggle_color_b:
                DISPLAYSURFACE.blit(b_letter, b_letter_rect)
            DISPLAYSURFACE.blit(box_img, box_rectR)
            DISPLAYSURFACE.blit(box_img, box_rectG)
            DISPLAYSURFACE.blit(box_img, box_rectB)
            DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        """LOGGING output information: FPS, event info, AA, etc."""
        frame += 1
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if frame == c.FPS:
            debug(DEBUG, (mean(fpsList)))
            frame = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []
            if len(circle_size_list) > 0:
                debug(DEBUG, 'Size: ' + str(circle_size_list[0]))

        """UPDATE AND DELAY"""
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.update()  # flip()

    try:
        rep_log.close()
    except Exception:
        debug(DEBUG, "File never opened")
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
