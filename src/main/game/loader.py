import pygame, debug, os  # @UnusedImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from debug import debug  # @Reimport

pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.init()


"""SCREEN INFORMATION"""
user_screen_data = pygame.display.Info()
window_width = user_screen_data.current_w
window_height = user_screen_data.current_h
pygame.display.set_caption('RGB - Beta v4')

def make_gamescreen(fullBool):
    # Making a screen, w/ 4 different possible outcomes.
    if fullBool == True:
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

# --FUNCTIONS to create our resources//--
def load_image(c, name, colorkey=None):
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

def load_song(c, name):
    fullname = os.path.join(c.MUSC_DIR, name)
    try:
        song = pygame.mixer.music.load(fullname)
    except pygame.error:
        debug(c.DEBUG, ('COULD NOT LOAD MUSIC: ', fullname))
        raise SystemExit(str(geterror()))
    return song
