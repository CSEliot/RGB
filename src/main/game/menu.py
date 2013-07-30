import pygame, pgext
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_song
from RGB_alpha import gameAlpha
def repositionButton(c,buttonRects):
    position = -50
    for buttonRect in buttonRects:
        buttonRect.center = (c.CENTER[0], c.CENTER[1] + position)
        position += 50
    return
    
    

def menu(c, background, stock):

    load_song(c, 'menuV3.ogg')
    pygame.mixer.music.play()

    if c.DEBUG:
        from time import time
        from numpy import mean
        from debug import debug
    
    debug(c.DEBUG, "Entering: mainMenu")
    # the background is the current information from the screen. It's faster
    # than grabbing it from the constants file.
    background_rect = background.get_rect()
    background_rect.center = c.CENTER


    # menu elements
    selected = 0  # tells which button is currently highlighted
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    button1 = 0  # represents placeholder for button
    button2 = 1  # represents placeholder for button
    button3 = 2
    entered = False  # tells if the user has chosen a button

    #Other Variables
    c.BgAngle = 0
    fpsList = []
    fpsWait = 3 #how many seconds till we report the game's FPS.
    frameCount = 0
    menuLocation = "main" #controls WHERE we are in the menu

    corners = stock.menu["Corners"]
    logo = stock.menu["Title"]
    # setup our button lists and sections
    mainButtons = [
               stock.menu["Play"], 
               stock.menu["Options"], 
               stock.menu["Quit"]
    ]
    playButtons = [
                   stock.menu["Campaign"],
                   stock.menu["Creative"],
                   stock.menu["Return"]
    ]
    # start with main buttons.
    buttons = mainButtons
    # same with rects
    mainButtonRects = [
                   buttons[0].get_rect(), 
                   buttons[1].get_rect(), 
                   buttons[2].get_rect()
    ]
    playButtonRects = [
                       playButtons[0].get_rect(), 
                       playButtons[1].get_rect(), 
                       playButtons[2].get_rect()
    ]
    buttonRects = mainButtonRects
    
    
    # menu button locations
    repositionButton(c, buttonRects)
    repositionButton(c, playButtonRects)
    # and then the corners and logo
    logo_rect = logo.get_rect()
    logoPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
    logo_rect.center = logoPos
    corners_rect = corners.get_rect()
    corners_rect.center = c.CENTER

    # set original images
    buttonsOrig = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
    backgroundOrig = background.copy()
    
    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)
    
    
    # --Main Game Loop//--
    going = True
    oldTime = time()
    while going:
        """ROTATION TESTING"""
        # rotate the background, but only 15 times/second, not 30.
        # if the frame rate is 30/sec, then rotate when its an odd frame.
        if frameCount%3 == 0:
            c.BgAngle += .03
            background = pygame.transform.rotozoom(backgroundOrig, c.BgAngle%360 , 1)
            background_rect = background.get_rect()
            background_rect.center = c.CENTER
        frameCount += 1
        
        
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                return 'QUIT'
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                entered = True
                selected = 2 # 2 is always the return/quit button
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if selected < 2:
                    # set the unselected as the previous selected one.
                    unselected = selected
                    selected += 1
                    newSelected = True
            elif event.type == KEYDOWN and event.key == K_UP:
                if selected > 0:
                    unselected = selected
                    selected -= 1
                    newSelected = True
            elif event.type == KEYDOWN and event.key == K_RETURN:
                entered = True
            elif event.type == KEYDOWN and event.key == K_a:
                gameAlpha(c)

        # this function controls what each button means/does.
        if entered:
            if menuLocation == "main":
                if selected == 0:
                    buttons[0] = buttonsOrig[0]
                    buttons = playButtons
                    buttonRects = playButtonRects
                    buttonsOrig = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
                    newSelected = True
                    menuLocation = "play"
                    selected = 0
                elif selected == 1:
                    # do nothing, options not made yet :/
                    None
                elif selected == 2:
                    return "QUIT"
            elif menuLocation == "play":
                if selected == 0:
                    return 'campaign'
                elif selected == 1:
                    return 'creative'
                elif selected == 2:
                    buttons[2] = buttonsOrig[2]
                    buttons = mainButtons
                    buttonRects = mainButtonRects
                    buttonsOrig = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
                    newSelected = True
                    menuLocation = "main"
                    selected = 0
            entered = False
            
        if newSelected:
            # revert unselected button back
            if unselected == button1:
                buttons[0] = buttonsOrig[0]
            elif unselected == button2:
                buttons[1] = buttonsOrig[1]
            elif unselected == button3:
                buttons[2] = buttonsOrig[2]
            # change image of newly selected
            if selected == button1:
                buttons[0] = pygame.transform.smoothscale(buttons[0], (buttonRects[0].width + 2, \
                                                        buttonRects[0].height + 2))
                pgext.color.setColor(buttons[0], (255, 255, 0))
            elif selected == button2:
                buttons[1] = pygame.transform.smoothscale(buttons[1], (buttonRects[1].width + 2, \
                                                        buttonRects[1].height + 2))
                pgext.color.setColor(buttons[1], (0, 255, 255))
            elif selected == button3:
                buttons[2] = pygame.transform.smoothscale(buttons[2], (buttonRects[2].width + 2, \
                                                        buttonRects[2].height + 2))
                pgext.color.setColor(buttons[2], (255, 0, 255))
            newSelected = False
            



        fpsList.append(c.FPSCLOCK.get_fps())
        # report the frame rate every 5 seconds
        newTime = time()
        if newTime - oldTime >= fpsWait:
            avgFPS = mean(fpsList)
            debug(c.DEBUG, avgFPS)
            pygame.display.set_caption('RGB. FPS: {0}'.format(avgFPS))
            fpsList = []
            oldTime = time()

        # reset frame count once it exceeds 30 frames
        if frameCount >= 30:
            frameCount = 0
            


        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(logo, logo_rect)
        c.DISPLAYSURFACE.blit(buttons[0], buttonRects[0])
        c.DISPLAYSURFACE.blit(buttons[1], buttonRects[1])
        c.DISPLAYSURFACE.blit(buttons[2], buttonRects[2])
        if c.DEBUG:
            c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()
        #         pygame.transform.set_smoothscale_backend(SSE)



if __name__ == "__main__":
    
    from constants import Constants
    from stock import Stock
    from loader import load_image
    
    c = Constants()
    stock = Stock(c)
    background = load_image(c, 'starBG.png')
    mult = 1.6
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    menu(c, background, stock)
