# File:   RGB - alpha
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.

import sys, os, pygame.gfxdraw, pgext
from pygame.locals import *  # @UnusedWildImport
from constants import Constants
from loader import load_image
# from cgi import escape
# from PIL.Image import ANTIALIAS
# from IPython.utils.timing import clock
import math as m
from debug import debug

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

# --constants//--
"""_________ALL_VARIABLES_BELOW_MAY_BE_MODIFIED_FOR_EXPERIMENTING____________"""
CIRCLE_GROWTH_SPEED = 3
FPS = 30  # frames per second ceiling setting
RED = pygame.color.Color('red')
GREEN = pygame.color.Color('green')
BLUE = pygame.color.Color('blue')
pygame.mouse.set_visible(0)
"""_________ALL_VARIABLES_ABOVE_MAY_BE_MODIFIED_FOR_EXPERIMENTING____________"""
WHITE = (255, 255, 255)
BLANK = (0, 233, 0, 10)
BLACK = (0, 0, 0)
fpsClock = pygame.time.Clock()
fontObj_large = pygame.font.Font('freesansbold.ttf', 32)


# --main//--
def gameAlpha(c):

    debug(c.DEBUG, "ENTERING: Alpha")

    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)
# --Initialize Everything//--
    CENTER_X = (c.DISPLAYSURFACE.get_width() / 2)
    CENTER_Y = (c.DISPLAYSURFACE.get_height() / 2)
    # a^2 + b^2 = c^2. This calculates the longest distance from rectangle center.
    C_LENGTH = m.sqrt((CENTER_X) ** 2 + (CENTER_Y) ** 2)
    r = 0
    g = 0
    b = 0
    rotate_by = 0
    paused = False
    total_input = 0
    circle_size_list = []
    circle_color_list = []
    toggle_color_r = BLACK
    toggle_color_g = BLACK
    toggle_color_b = BLACK
    display_sprites = True
    orig_stdout = sys.stdout
    current_circle_quantity = 0
    display_antialiasing = False
    BACKGROUND_COLOR = pygame.color.Color('white')  # background color
    inverted = False
    rotation_speed = 2
    pygame.transform.set_smoothscale_backend('GENERIC')

    # throw down splash screen before beginning
    splashInfo, splashInfo_rect = load_image(c, 'splashInfoAlpha.png')
    # adjusting image cuz i can't make images.
    splashInfo_rect.center = (c.CENTER_X - 50, c.CENTER_Y)

    # fill background
    c.DISPLAYSURFACE.fill((0, 0, 0))
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
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False
            break
    while inInfoScreen:
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False
    fade = 255
    pgext.color.setAlpha(splashInfo, fade, 1)




# --Main Game Loop//--
    going = True
    while going:

    # Paint the background color, which CAN change.
        c.DISPLAYSURFACE.fill(BACKGROUND_COLOR)

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
        # if u is pressed, toggle AAing.
            elif event.type == KEYDOWN and event.key == K_u:
                if display_antialiasing == True:
                    display_antialiasing = False
                else:
                    display_antialiasing = True
        # if i is pressed, toggle context display
            elif event.type == KEYDOWN and event.key == K_i:
                if display_sprites == True:
                    display_sprites = False
                else:
                    display_sprites = True
        # if q is pressed, print output to file log.txt
            elif event.type == KEYDOWN and False:
                if orig_stdout == sys.stdout:
                    rep_log = open('data/log.txt', 'a')
                    sys.stdout = rep_log
                    print "LOGGING TO FILE BEGINNING--"
                else:
                    print "LOGGING TO FILE ENDING--"
                    sys.stdout = orig_stdout
                    rep_log.close()
        # if p is pressed, pause game.
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
        # if l is pressed, toggle black auto-black circle.
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
                pygame.gfxdraw.filled_circle(c.DISPLAYSURFACE,
                                             CENTER_X, CENTER_Y,
                                             circle_size_list[i], (
                                             circle_color_list[i][0],
                                             circle_color_list[i][1],
                                             circle_color_list[i][2]))
            if display_antialiasing == True:
                # an anti-aliasing ring is drawn on top of the circle edge.
                pygame.gfxdraw.aacircle(c.DISPLAYSURFACE,
                                        CENTER_X, CENTER_Y,
                                        circle_size_list[i] - 1, (
                                        circle_color_list[i][0],
                                        circle_color_list[i][1],
                                        circle_color_list[i][2]))
                pygame.gfxdraw.filled_circle(c.DISPLAYSURFACE,
                                             CENTER_X, CENTER_Y,
                                             circle_size_list[i], (
                                             circle_color_list[i][0],
                                             circle_color_list[i][1],
                                             circle_color_list[i][2]))
                pygame.gfxdraw.aacircle(c.DISPLAYSURFACE,
                                        CENTER_X, CENTER_Y,
                                        circle_size_list[i], (
                                        circle_color_list[i][0],
                                        circle_color_list[i][1],
                                        circle_color_list[i][2]))
                pygame.gfxdraw.aacircle(c.DISPLAYSURFACE,
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




        """DISPLAY SPRITE TOGGLE"""
        if display_sprites == True:
            c.DISPLAYSURFACE.blit(r_SurfaceObj, r_RectObj)
            c.DISPLAYSURFACE.blit(g_SurfaceObj, g_RectObj)
            c.DISPLAYSURFACE.blit(b_SurfaceObj, b_RectObj)
            c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)

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
#     pygame.quit()
#     sys.exit()

if __name__ == '__main__':
    c = Constants()
    gameAlpha(c)
