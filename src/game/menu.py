#@PydevCodeAnalysisIgnore
import pygame, pgext, sys
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from RGB_alpha import gameAlpha

def repositionButton(c,buttonRects):
    position = -50
    for buttonRect in buttonRects:
        buttonRect.center = (c.CENTER[0], c.CENTER[1] + position)
        position += 50
    return
    
    
def menu(c, background, stock, store):

    

    from time import time
    from numpy import mean
    from debug import debug
    
    debug(c.DEBUG, "Entering: mainMenu")
    # the background is the current information from the screen. It's faster
    # than grabbing it from the constants file.
    background_rect = background.get_rect()
    background_rect.center = c.CENTER


    # menu elements
    selected = 1  # tells which button is currently highlighted
    newSelected = True  # tells if something new has been highlighted
    unselected = 0  # used to change unhighlighted button back
    button1 = 1  # represents placeholder for button
    button2 = 2  # represents placeholder for button
    button3 = 3  
    button4 = 4  # is always the quit button
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
                   stock.menu["Alpha"]
    ]
    
    #a button independent of everything else, return. first in list is original,. second gets modified
    returnButtons = [stock.menu["Return"].copy(), stock.menu["Return"].copy()] 
    pgext.color.setColor(returnButtons[1], (100, 100, 100))
    returnButton_rect = returnButtons[0].get_rect(center = (c.CENTER[0], c.CENTER[1] + 145))
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
    
    # create the version ID object 
    versionID_SurfaceObj = stock.version
    
    store.music['menu'].set_volume(1)
    store.music['menu'].play()
    store.music['menu'].fadeout(3000)
    # --Main Game Loop//--
    going = True
    oldTime = time()
    while going:
        
        # rotation causes the game to lag in fullscreen, so we don't rotate when in fullscreen.
        if not c.FULLSCREEN:
            """ROTATION TESTING"""
            # rotate the background, but only 15 times/second, not 30.
            # if the frame rate is 30/sec, then rotate when its an odd frame.
            if frameCount%2 == 0:
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
                pygame.quit()
                sys.exit()
                return 'QUIT'
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                entered = True
                newSelected = True
                unselected = selected
                selected = button4 # 2 is always the return/quit button
                store.sounds['scroll'].play()
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_DOWN:
                # set the unselected as the previous selected one.
                unselected = selected
                selected += 1
                newSelected = True
                if selected > button4:
                    selected = button1
                if selected == button1:
                    store.sounds['Enter 1'].play()
                elif selected == button2:
                    store.sounds['Enter 2'].play()
                elif selected == button3:
                    store.sounds['Enter 3'].play()
            elif event.type == KEYDOWN and event.key == K_UP:
                unselected = selected
                selected -= 1
                newSelected = True
                if selected < button1:
                    selected = button4 
                if selected == button1:
                    store.sounds['Enter 1'].play()
                elif selected == button2:
                    store.sounds['Enter 2'].play()
                elif selected == button3:
                    store.sounds['Enter 3'].play()
            elif event.type == KEYDOWN and \
            (event.key == K_RETURN or event.key == K_SPACE):
            # if the key is Enter or Spacebar, a button was selected.
                entered = True
                unselected = 0
                store.sounds['scroll'].play()
            elif event.type == KEYDOWN and event.key == K_a:
                gameAlpha(c)

        if newSelected:
            # revert unselected button back
            if unselected:
                if unselected == button1:
                    buttons[0] = buttonsOrig[0]
                elif unselected == button2:
                    buttons[1] = buttonsOrig[1]
                elif unselected == button3:
                    buttons[2] = buttonsOrig[2]
                elif unselected == button4:
                    returnButtons[1] = returnButtons[0].copy()
                    pgext.color.setColor(returnButtons[1], (100, 100, 100))
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
            elif selected == button4:
                returnButtons[1] = pygame.transform.smoothscale(returnButtons[1], (returnButton_rect.width + 2, \
                                                        returnButton_rect.height + 2))
                returnButtons[1] = returnButtons[0].copy()
                
            newSelected = False
            
        # this function controls what each button means/does.
        if entered:
            if menuLocation == "main":
                if selected == button1:
                    buttons[0] = buttonsOrig[0]
                    # make buttons a reference to the play buttons
                    buttons = playButtons
                    # copy the button surfaces, so they're independent, not a reference.
                    buttons = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
                    # make a set that are unmodified, so modified button can be turned back
                    buttonsOrig = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
                    # make a reference to the pay button rects, but leave it that way
                    buttonRects = playButtonRects
                    newSelected = True
                    menuLocation = "play"
                    selected = button1
                    unselected = 0
                elif selected == button2:
                    # do nothing, options not made yet :/
                    None
                elif selected == button3 or selected == button4:
                    return "QUIT"
            elif menuLocation == "play":
                if selected == button1:
                    return 'campaign'
                elif selected == button2:
                    return 'creative'
                elif selected == button3:
                    print "LAUNCHING GAME ALPHA"
                    gameAlpha(c)
                elif selected == button4:
                    buttons[2] = buttonsOrig[2]
                    buttons = mainButtons
                    buttonRects = mainButtonRects
                    buttonsOrig = [buttons[0].copy(), buttons[1].copy(), buttons[2].copy()]
                    pgext.color.setColor(returnButtons[1], (100, 100, 100))
                    newSelected = True
                    menuLocation = "main"
                    selected = button1
                    unselected = 0
            entered = False


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
        if frameCount >= c.FPS:
            frameCount = 0
            


        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(logo, logo_rect)
        c.DISPLAYSURFACE.blit(buttons[0], buttonRects[0])
        c.DISPLAYSURFACE.blit(buttons[1], buttonRects[1])
        c.DISPLAYSURFACE.blit(buttons[2], buttonRects[2])
        # we always blit the second image in the buttons list, since it gets 
        # changed to show it being selected.
        c.DISPLAYSURFACE.blit(returnButtons[1], returnButton_rect)
        if c.DEBUG:
            c.DISPLAYSURFACE.blit(versionID_SurfaceObj, (0,0))
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()
        #         pygame.transform.set_smoothscale_backend(SSE)



if __name__ == "__main__":
    
    from constants import Constants
    from stock import Stock
    from store import Store
    from loader import load_image
    
    c = Constants()
    stock = Stock(c)
    store = Store(c)
    background = load_image(c, 'starBG.png')
    mult = 1.6
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    menu(c, background, stock, store)
