import pygame, sys, os, datetime, platform  # @UnusedImport
import math as m # @UnusedImport

class Constants(object):
    '''
    holds all "global variables"
    '''

    def __init__(self, DISPLAYSURFACE):
        self.DEBUG = True
        self.MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
        self.DATA_DIR = os.path.join(self.MAIN_DIR, 'data')
        # --constants//--
        self.DISPLAYSURFACE = DISPLAYSURFACE
        self.CIRCLE_GROWTH_SPEED = 3
        self.FPS = 30  # frames per second ceiling setting
        self.RED = pygame.color.Color('red')
        self.GREEN = pygame.color.Color('green')
        self.BLUE = pygame.color.Color('blue')
        self.NO_MOUSE = pygame.mouse.set_visible(1)
        self.WHITE = (255, 255, 255)
        self.BLANK = (0, 233, 0, 10)
        self.BLACK = (0, 0, 0)
        self.FPSCLOCK = pygame.time.Clock()
        self.FONT_LARGE = pygame.font.Font('freesansbold.ttf', 32)
        self.FONT_SMALL = pygame.font.Font('freesansbold.ttf', 8)
        self.VERSION = 'v0.2-BETA'
        self.DISPLAY_W = self.DISPLAYSURFACE.get_width()
        self.CENTER_X = (self.DISPLAY_W / 2)
        self.DISPLAY_H = self.DISPLAYSURFACE.get_height()
        self.CENTER_Y = (self.DISPLAY_H / 2)
        self.CENTER = (self.CENTER_X, self.CENTER_Y)
        # equates screen diagonal.
        self.C_LENGTH = m.sqrt((self.CENTER_X) ** 2 + (self.CENTER_Y) ** 2)  
        self.DATE = datetime.date.timetuple(datetime.date.today())[0] , \
                    datetime.date.timetuple(datetime.date.today())[1] , \
                    datetime.date.timetuple(datetime.date.today())[2]
                