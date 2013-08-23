import pygame
from loader import load_image


class Stock(object):
    '''
    this object will be made to hold all the images, so loading only has to be
    done once.
    '''

    #stock holds dictionaries 
    def __init__(self, c):
        self.menu = {
                     "Title":load_image(c, 'menu/logo.png'), 
                     "Corners":load_image(c, "menu/menuBox.png"),
                     "Play":load_image(c, 'menu/play.png'),
                     "Options":load_image(c, 'menu/options.png'),
                     "Alpha":load_image(c, 'menu/alpha.png'),
                     "Quit":load_image(c, 'menu/quit.png'),
                     "Campaign":load_image(c, 'menu/campaign.png'),
                     "Creative":load_image(c, 'menu/creative.png'),
                     "Return":load_image(c, 'menu/return.png')
        }
        self.campaign = {
                         "Background":load_image(c, 'starBG.png'),
                         "Ring":load_image(c, 'campaign/ring.png'),
                         "Circle":load_image(c, 'campaign/circle.png'),
                         "Star Lit":load_image(c, 'campaign/lit_star.png'),
                         "Star Unlit":load_image(c, 'campaign/unlit_star.png'),
                         "RGB Light":load_image(c, 'campaign/letter_box.png'),
                         "Info Splash":load_image(c, 'campaign/splashInfo.png'),
                         "Ring Glow":load_image(c, 'campaign/ring_glow.png')
        }
        
        self.version = [c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE), None]
        self.version[1] = self.version[0].get_rect()
        
        self.creative = {
                         "Info Splash":load_image(c, "creative/Creative Control Scheme.png"),
                         "Circle Building":c.FONT_LARGE.render(
                                                            "Building: Circles",
                                                             False, 
                                                             c.BLACK, 
                                                             c.WHITE),
                         "Star Building":c.FONT_LARGE.render(
                                                            "Building: Stars",
                                                             False, 
                                                             c.BLACK, 
                                                             c.WHITE),
                         "Build Testing":c.FONT_LARGE.render(
                                                            "Build Testing",
                                                             False, 
                                                             c.BLACK, 
                                                             c.WHITE)}
        self.pause = {"Corners":load_image(c, "pause/scrbx.png"),
                      "Return":load_image(c, 'pause/return.png'),
                      "Options":load_image(c, 'pause/options.png'),
                      "Paused":load_image(c, 'pause/paused.png'),
                      "Quit":load_image(c, 'pause/quit.png')}
    
    def getVersion(self):
        return self.versionID
                        
                                           
