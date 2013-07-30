import pygame, os, platform
from pygame.locals import FULLSCREEN , DOUBLEBUF , HWSURFACE, RLEACCEL
from pygame.compat import geterror  # @UnusedImport
from debug import debug  # @Reimport






"""So ONE of these settings should work for windows, please try different ones
if you get an error about the mixer"""
#frequency, size, channels, buffersize = 22050, 16, 2, 4096
#frequency, size, channels, buffersize = 44100, 16, 2, 2048
#frequency, size, channels, buffersize = 44100, 16, 2, 1024
frequency, size, channels, buffersize = 22050, 16, 2, 1024
# if none of the above work, comment them all out and comment out pre_init line.
pygame.mixer.pre_init(frequency, -size, channels, buffersize)

os.environ['SDL_VIDEO_CENTERED'] = '1' # centers the window
try:
    if platform.system()== 'Windows':
        os.environ['SDL_VIDEODRIVER'] = 'directx'
except:
    if platform.system()== 'Windows':
        os.environ['SDL_VIDEODRIVER'] = 'windib'

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
#ignore mouse motion input
pygame.event.set_blocked((pygame.MOUSEMOTION, pygame.ACTIVEEVENT))

"""SCREEN INFORMATION"""
user_screen_data = pygame.display.Info()
window_width = user_screen_data.current_w
window_height = user_screen_data.current_h

def make_gamescreen(fullBool):
    # Making a screen, w/ 4 different possible outcomes.
    if fullBool == True:
        try:
            options = (FULLSCREEN | DOUBLEBUF | HWSURFACE)
            std_res = (window_width, window_height)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 1"
            screenError = "Window Error: None"
            displayInfo = "{0}\n{1}\n{2}\n{3}\n".format(
                          platform.system(),
                          pygame.display.get_driver(),
                          pygame.display.Info(),
                          pygame.display.get_wm_info(),
                          pygame.display.list_modes(32),
                          )
        except Exception as e:
            options = (FULLSCREEN)
            std_res = (window_width - 100, window_height - 100)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 2"
            screenError = "Window Error {0}".format(e)
            displayInfo = "{0}{1}\n{2}\n{3}\n".format(
                          pygame.display.get_driver(),
                          pygame.display.Info(),
                          pygame.display.get_wm_info(),
                          pygame.display.list_modes(32)
                          )
    else:
        try:
            options = (DOUBLEBUF | HWSURFACE)
            std_res = (800, 700)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 3"
            screenError = "Window Error: None"
            displayInfo = "{0}\n{1}\n{2}\n{3}\n".format(
                          pygame.display.get_driver(),
                          pygame.display.Info(),
                          pygame.display.get_wm_info(),
                          pygame.display.list_modes(32)
                          )
        except Exception as e:
            # If for some reason this resolution does not fit user's display it will
            # fit to their native resolution.
            options = 0
            std_res = (window_width - 100, window_height - 100)
            DISPLAYSURFACE = pygame.display.set_mode(std_res, options, 32)
            whichDisplay = "Display 4"
            screenError = "Window Error: {0}".format(e)
            displayInfo = "{0}\n{1}\n{2}\n{3}\n".format(
                          pygame.display.get_driver(),
                          pygame.display.Info(),
                          pygame.display.get_wm_info(),
                          pygame.display.list_modes(32)
                          )
    return DISPLAYSURFACE, whichDisplay, screenError, displayInfo

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
        return image
    return image.convert_alpha()

def load_song(c, name):
    fullname = os.path.join(c.MUSC_DIR, name)
    pygame.mixer.music.set_volume(c.VOLUME)
    try:
        pygame.mixer.music.load(fullname)
    except pygame.error:
        debug(c.DEBUG, ('COULD NOT LOAD MUSIC: ', fullname))
        raise SystemExit(str(geterror()))
    return

#this function only gets used in the Constants class, because Constants can't
#call itself.
def load_image_C(gfx_dir, DEBUG, name, colorkey=None):
    fullname = os.path.join(gfx_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        debug(DEBUG, ('Cannot load image:', fullname))
        raise SystemExit(str(geterror()))
    # image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
    return image.convert_alpha(), image.get_rect()
