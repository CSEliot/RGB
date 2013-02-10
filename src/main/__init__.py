# File:   RGB - alpha
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.

import pygame, sys, os, pygame.gfxdraw, pygame.surface
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror
# from cgi import escape
# from PIL.Image import ANTIALIAS
# from IPython.utils.timing import clock
import math as m

pygame.init()

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
'''
_______________________________________________________________________________
KEY:

"""KEYWORDS""" -For quick code finding, a few key words are entered in all caps

#explanation   -A short description of the code, sometimes in pseudo-code

#--title//--   -A separation of specific sections.
_______________________________________________________________________________
'''

"""FULLSCREEN ON STARTUP?"""
FULLSCREEN_RES = True
"""||||||||||||||||||||||"""

"""SCREEN INFORMATION"""
user_screen_data = pygame.display.Info()
window_width = user_screen_data.current_w
window_height = user_screen_data.current_h
pygame.display.set_caption('RGB - The Game of COLORS by Eliot C-S')
if FULLSCREEN_RES == True:
    try:
        options = (FULLSCREEN | DOUBLEBUF | HWSURFACE)
        std_res = (window_width, window_height)
        DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
        which_display = "Display 1"
    except Exception as e:
        options = 0
        std_res = (window_width - 100, window_height - 100)
        DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
        which_display = "Display 2"
        screen_error = "Window Error {0}: {1}".format(e.errno, e.strerror)
else:
    try:
        options = (DOUBLEBUF | HWSURFACE)
        std_res = (1000, 700)
        DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
        which_display = "Display 3"
    except Exception as e:
    # If for some reason this resolution does not fit user's display, it will
    # fit to their native resolution.
        options = 0
        std_res = (window_width - 100, window_height - 100)
        DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
        which_display = "Display 4"
        screen_error = "Window Error {0}: {1}".format(e.errno, e.strerror)


# --constants//--
"""_________ALL_VARIABLES_BELOW_MAY_BE_MODIFIED_FOR_EXPERIMENTING____________"""
CIRCLE_GROWTH_SPEED = 3
FPS = 60  # frames per second ceiling setting
RED = pygame.color.Color('red')
GREEN = pygame.color.Color('green')
BLUE = pygame.color.Color('blue')
pygame.mouse.set_visible(0)
# ring_img = pygame.image.load("ring_gray.png")
"""_________ALL_VARIABLES_ABOVE_MAY_BE_MODIFIED_FOR_EXPERIMENTING____________"""
WHITE = (255, 255, 255)
BLANK = (0, 233, 0, 10)
BLACK = (0, 0, 0)
fpsClock = pygame.time.Clock()
fontObj_large = pygame.font.Font('freesansbold.ttf', 32)
fontObj_small = pygame.font.Font('freesansbold.ttf', 8)
version_num = 'v0.1.4c'
CENTER_X = (DISPLAYSURFACE.get_width() / 2)
CENTER_Y = (DISPLAYSURFACE.get_height() / 2)
# a^2 + b^2 = c^2. This calculates the longest distance from rectangle center.
C_LENGTH = m.sqrt((CENTER_X) ** 2 + (CENTER_Y) ** 2)





class Circle (pygame.sprite.Sprite):

    def __init__(self):
        # self.image, self.rect = load_image('ring.png', None)
        self.size = 0
        self.color = (0, 0, 0)

    def increase_size(self):
        self.size += CIRCLE_GROWTH_SPEED

    def set_color(self, r=0, g=0, b=0):
        self.color = (r, g, b)


def fullscreen_test():
    # --TESTING the full-screen function//--
    for i in range(2):
        try:
            # toggle_fullscreen returns a 1/0 based on if it worked
            attempt_fullscreen = pygame.display.toggle_fullscreen()
            scn_tst = "About the full-screen, there were no errors boss!"
        except Exception as e:
            scn_tst = "Full-screen error({0}): {1}".format(e.errno, e.strerror)

# --FUNCTIONS to create our resources//--
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    # image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# --main//--
def main():

# --Initialize Everything//--
    r = 0
    g = 0
    b = 0
    angle = 0
    rotate_by = 0
    paused = False
    total_input = 0
    circle_size_list = []
    circle_color_list = []
    toggle_color_r = BLACK
    toggle_color_g = BLACK
    toggle_color_b = BLACK
    display_sprites = True
    rep_log = file.__class__
    orig_stdout = sys.stdout
    current_circle_quantity = 0
    display_antialiasing = False
    ring_img, ring_rect = load_image('ring_silver.png', None)
    box_img, box_rect = load_image('letter_box.png', None)
    BACKGROUND_COLOR = pygame.color.Color('white')  # background color
    box_rect.center = (CENTER_X, CENTER_Y)
    ring_rect.center = (CENTER_X, CENTER_Y)
    inverted = False
    rotation_speed = 2
#    pygame.transform.set_smoothscale_backend('GENERIC')

# --Main Game Loop//--
    made_background = False
    going = True
    while going:

    # Paint the background color, which CAN change.
        DISPLAYSURFACE.fill(BACKGROUND_COLOR)

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
                toggle_color_r = RED
                total_input += 1
            elif event.type == KEYUP and event.key == K_r:
                r = 0
                toggle_color_r = BLACK
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_g:
                g = 255
                toggle_color_g = GREEN
                total_input += 1
            elif event.type == KEYUP and event.key == K_g:
                g = 0
                toggle_color_g = BLACK
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_b:
                b = 255
                toggle_color_b = BLUE
                total_input += 1
            elif event.type == KEYUP and event.key == K_b:
                b = 0
                toggle_color_b = BLACK
                total_input += -1
            elif event.type == KEYDOWN and event.key == K_o:
                if inverted == False:
                    inverted = True
                else:
                    inverted = False
        # Ring Spinning
            elif event.type == KEYDOWN and event.key == K_LEFT:
                rotate_by += -rotation_speed
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                rotate_by += rotation_speed
            elif event.type == KEYUP and event.key == K_LEFT:
                rotate_by += rotation_speed
            elif event.type == KEYUP and event.key == K_RIGHT:
                rotate_by += -rotation_speed
        # --non-game-play events//--
        # if U is pressed, toggle AAing.
            elif event.type == KEYDOWN and event.key == K_u:
                if display_antialiasing == True:
                    display_antialiasing = False
                else:
                    display_antialiasing = True
        # if I is pressed, toggle context display
            elif event.type == KEYDOWN and event.key == K_i:
                if display_sprites == True:
                    display_sprites = False
                else:
                    display_sprites = True
        # if Q is pressed, print output to file log.txt
            elif event.type == KEYDOWN and event.key == K_q:
                if orig_stdout == sys.stdout:
                    rep_log = open('data/log.txt', 'a')
                    sys.stdout = rep_log
                    print "LOGGING TO FILE BEGINNING--"
                    print "Display Info: {0}".format(which_display)
                    print attempt_fullscreen, scn_tst
                else:
                    print "LOGGING TO FILE ENDING--"
                    sys.stdout = orig_stdout
                    rep_log.close()
        # if P is pressed, pause game.
            elif event.type == KEYUP and event.key == K_p:
                pygame.event.pump()
                for p in pygame.key.get_pressed():
                        if p == True:
                            print "A KEY IS PRESSED, CAN NOT PAUSE"
                            paused = False
                            break
                        else:
                            paused = True
                            print "INTO PAUSE!!"
        # if L is pressed, toggle black auto-black circle.
            elif event.type == KEYDOWN and event.key == K_l:
                if total_input == 0:
                    total_input = 100
                else:
                    total_input = 0
            """LOGGING of inputs"""
            if event.type == KEYDOWN or event.type == KEYUP:
                print event.dict

    # --function controls//--
    # if paused is set to true, wait for p to be pressed again.
        """PAUSE WAIT STOP"""
        while paused:
                x_event = pygame.event.wait()
                if x_event.type == KEYUP and event.key == K_p:
                    pygame.event.pump()
                    for p in pygame.key.get_pressed():
                        if p == True:
                            print "A KEY IS PRESSED, CAN NOT UNPAUSE"
                            paused = True
                            break
                        else:
                            paused = False
                            print "OUT OF PAUSE!"
                if x_event.type == QUIT:
                    sys.exit()
                    pygame.quit()
                elif x_event.type == KEYDOWN and x_event.key == K_ESCAPE:
                    sys.exit()
                    pygame.quit()

        """SPIN ROTATE"""
    # --Spin the Ring//--
        if inverted == True:
            angle += -rotate_by * 2
        else:
            angle += rotate_by * 2
        ring_imgNew = ring_img  # .convert()
        ring_imgNew = pygame.transform.rotozoom(ring_img, angle, 1)
        ring_rectNew = ring_imgNew.get_rect(center=(CENTER_X, CENTER_Y))

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
            circle_size_list[i] += CIRCLE_GROWTH_SPEED
            if display_antialiasing == False:
    # draw circle to the screen, grabbing each color amount: R, G, B
                pygame.gfxdraw.filled_circle(DISPLAYSURFACE,
                                             CENTER_X, CENTER_Y,
                                             circle_size_list[i], (
                                             circle_color_list[i][0],
                                             circle_color_list[i][1],
                                             circle_color_list[i][2]))
            if display_antialiasing == True:
    # an anti-aliasing ring is drawn on top of the circle edge.
                pygame.gfxdraw.aacircle(DISPLAYSURFACE,
                                        CENTER_X, CENTER_Y,
                                        circle_size_list[i] - 1, (
                                        circle_color_list[i][0],
                                        circle_color_list[i][1],
                                        circle_color_list[i][2]))
                pygame.gfxdraw.filled_circle(DISPLAYSURFACE,
                                             CENTER_X, CENTER_Y,
                                             circle_size_list[i], (
                                             circle_color_list[i][0],
                                             circle_color_list[i][1],
                                             circle_color_list[i][2]))
                pygame.gfxdraw.aacircle(DISPLAYSURFACE,
                                        CENTER_X, CENTER_Y,
                                        circle_size_list[i], (
                                        circle_color_list[i][0],
                                        circle_color_list[i][1],
                                        circle_color_list[i][2]))
                pygame.gfxdraw.aacircle(DISPLAYSURFACE,
                                        CENTER_X, CENTER_Y,
                                        circle_size_list[i] + 1, (
                                        circle_color_list[i][0],
                                        circle_color_list[i][1],
                                        circle_color_list[i][2]))




        """POP LARGE CIRCLES"""
    # get rid of big circles
        if len(circle_size_list) >= 1:
            if circle_size_list[0] >= C_LENGTH:
                circle_size_list.pop(0)
    # paint the background to the color of the last circle
                BACKGROUND_COLOR = circle_color_list[0]
                circle_color_list.pop(0)
                current_circle_quantity += -1

        """BUTTON / SPRITE RENDERING"""
        r_SurfaceObj = fontObj_large.render('R', True, toggle_color_r)
        r_RectObj = r_SurfaceObj.get_rect()
        r_RectObj.center = (CENTER_X - 50, (CENTER_Y * 2) - 25)

        g_SurfaceObj = fontObj_large.render('G', True, toggle_color_g)
        g_RectObj = g_SurfaceObj.get_rect()
        g_RectObj.center = (CENTER_X, (CENTER_Y * 2) - 25)

        b_SurfaceObj = fontObj_large.render('B', True, toggle_color_b)
        b_RectObj = b_SurfaceObj.get_rect()
        b_RectObj.center = (CENTER_X + 50, (CENTER_Y * 2) - 25)

    # display the version ID
        font_renderObj = fontObj_small.render(version_num, False, BLACK, WHITE)
        versionID_SurfaceObj = font_renderObj
        versionID_RectObj = versionID_SurfaceObj.get_rect()
        versionID_RectObj.topleft = (0, 0)




        """DISPLAY SPRITE TOGGLE"""
        if display_sprites == True:
            DISPLAYSURFACE.blit(r_SurfaceObj, r_RectObj)
            DISPLAYSURFACE.blit(g_SurfaceObj, g_RectObj)
            DISPLAYSURFACE.blit(b_SurfaceObj, b_RectObj)
            DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
            DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            DISPLAYSURFACE.blit(ring_imgNew, ring_rectNew)
            DISPLAYSURFACE.blit(box_img, r_RectObj)
            DISPLAYSURFACE.blit(box_img, g_RectObj)
            DISPLAYSURFACE.blit(box_img, b_RectObj)
            # pygame.draw.circle(DISPLAYSURFACE, BLACK, ring_imgNew.get_rect().center, 5, 2)
            print pygame.transform.get_smoothscale_backend()

        """LOGGING output information: FPS, event info, AA, etc."""
        num_compare = "%d:%d" % (current_circle_quantity, len(circle_size_list))
        print fpsClock.get_fps(), num_compare
        if len(circle_size_list) > 0:
            print circle_size_list[0]

        """UPDATE AND DELAY"""
        fpsClock.tick_busy_loop(FPS)
        pygame.display.flip()

    try:
        rep_log.close()
    except Exception:
        print "File never opened"
    pygame.quit()
    sys.exit()
if __name__ == '__main__':
    main()
