import pygame, sys, os, datetime, platform  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
import math as m  # @UnusedImport
from loader import make_gamescreen
import cPickle

class Constants(object):
    '''
    holds all "global variables"
    '''

    def __init__(self):
        # we have to split MAIN DIR twice in order to get to RGB/src/main
        self.MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
        self.MAIN_DIR = os.path.split(self.MAIN_DIR)[0]
        self.DATA_DIR = os.path.join(self.MAIN_DIR, 'data')
        self.GFX_DIR = os.path.join(self.MAIN_DIR, 'graphics')
        self.SND_DIR = os.path.join(self.MAIN_DIR, 'sound')
        self.MUSC_DIR = os.path.join(self.MAIN_DIR, 'music')
        self.GAME_DIR = os.path.join(self.MAIN_DIR, 'game')
        # --controls and options//--
        setList = self.get_OPTIONS()
        # In order: R, G, B, Up, down, left, right, pause, debug
        self.CONTROL_LIST = [setList[2], setList[3], setList[4], setList[5], \
                             setList[6], setList[7], setList[8], setList[9], \
                             setList[10]]
        self.FULLSCREEN = setList[0]
        self.VOLUME = setList[1]
        ## BUILDING SCREEN FROM LOADER
        DISPLAYSURFACE, wDisplay, scnError, displayInfo = \
        make_gamescreen(self.FULLSCREEN)
        self.displayInfo = displayInfo
        self.OG_STDOUT = sys.stdout
        self.whichDisplay = wDisplay
        self.screenError = scnError
        # default game values
        self.DEBUG = True
        self.RING_SIZE = 540.0  # for circles  reference only!
        self.RING_RADIUS = 265.0  # for stars / speed
        self.BPM = 60.0
        self.C_SPEED = 10
        self.F_SPEED = 10
        self.WAIT = 1
        # --constants//--
        self.DISPLAYSURFACE = DISPLAYSURFACE
        self.FPS = 30  # frames per second ceiling setting
        self.RED = pygame.color.Color('red')
        self.GREEN = pygame.color.Color('green')
        self.BLUE = pygame.color.Color('blue')
        self.NO_MOUSE = pygame.mouse.set_visible(0)
        self.WHITE = (255, 255, 255)
        self.BLANK = (0, 233, 0, 10)
        self.BLACK = (0, 0, 0)
        self.FPSCLOCK = pygame.time.Clock()
        self.FONT_LARGE = pygame.font.SysFont('arial', 32, True)
        self.FONT_SMALL = pygame.font.SysFont('arial', 16)
        self.VERSION = 'betaV1.3e'
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
        
        # eventually, the background's spin will be constant, and always there.
        self.BgAngle = 0
    def get_OPTIONS(self):
        optFile = open(os.path.join(self.DATA_DIR, 'options.dat'), 'r')
        optList = cPickle.load(optFile)
        optFile.close()
        return optList

    def set_DEFAULT(self):
        defaultList = [True, 1.0, K_r, K_g, K_b, K_UP, K_DOWN, K_LEFT, K_RIGHT, \
                       K_p, K_i]
        optFile = open(os.path.join(self.DATA_DIR, 'options.dat'), 'w')
        cPickle.dump(defaultList, optFile)
