#===============================================================================
# File:   RGB - beta
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.
#===============================================================================

import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnresolvedImport @UnusedImport
from numpy import mean
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from constants import Constants
from debug import debug
from circle import Circle
from star import Star
from ring import Ring
from scoreboard import Scoreboard
from loader import load_image, load_song
from pause import pauseScreen
from commander import commander




class timer():
    # this class is meant to hold time variables, mostly for
    # organizational purposes.
    
    def __init__(self):
        self.timeIn = 0
        self.timeOut = 0
        self.timeList = []
        
    def getTime(self, choice):
        # get time in total seconds
        if choice == 1:
            return self.timeIn.total_seconds()
        elif choice == 2:
            return self.timeOut.total_seconds()
        elif choice == 3:
            return self.timeList
        else:
            raise Exception('time choice must be 1, 2 or 3.')
    
    def setTime(self, choice):
        if choice == 1:
            self.timeIn = datetime.datetime.now()
        elif choice == 2:
            self.timeOut = datetime.datetime.now()
        elif choice == 3:
            self.timeList.append(datetime.datetime.now())
            
    def getDelta(self, now): 
        # gives time difference of timeIn and timeOut in seconds
        # if now is true, then we will grab the timeOut also, and math it.
        if now:
            return (datetime.datetime.now() - self.timeIn).total_seconds()
        else:
            return (self.timeOut - self.timeIn).total_seconds()



class playBox():
    # This class holds all our variables to access while playing.
    def __init__(self):
        self.cSpeed = 0
        self.fSpeed = 0
        self.cWait = 0
        self.fWait = 0
        self.isPlaying = False
        self.isFirst = True
        self.layer = 0

def pause(c, stock, image):
    """PAUSE UNPAUSE"""
    pygame.mixer.music.pause()
    choice = pauseScreen(c, stock, image)
    pygame.mixer.music.unpause()
    return choice


def rotateBackground(center, background, counter, rotationAngle):
    """ROTATION TESTING"""
    # rotate the background, but only 15 times/second, not 30.
    # if the frame rate is 30/sec, then rotate when its an odd frame.
    rotationAngle += .03
    background = pygame.transform.rotozoom(background, rotationAngle%360 , 1)
    background_rect = background.get_rect()
    background_rect.center = center
    return background, background_rect, rotationAngle

def showSplashScreen(c, stock):
    # throw down splash screen before beginning
    splashInfo = stock.campaign["Info Splash"]
    splashInfo = pygame.transform.scale(splashInfo, (c.DISPLAY_W, c.DISPLAY_H))
    splashInfo_rect = splashInfo.get_rect(center=c.CENTER)
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
        c.DISPLAYSURFACE.blit(stock.version, (0,0))
        pygame.display.flip()
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False
            break
    # if the info is still being read/no button pressed, just wait.
    fade = 255
    pgext.color.setAlpha(splashInfo, fade, 1)
    while inInfoScreen:
        if pygame.event.poll().type != NOEVENT:
            inInfoScreen = False

def campaign(c, background, stock, store):
    
    debug(c.DEBUG, "ENTERING: campaign")
    load_song(c, "It's Melting.ogg")
    
    
    versionID = stock.getVersion()

#    pygame.key.set_repeat(0, 0)

    allSprites = pygame.sprite.Group()
    ringSprite = pygame.sprite.GroupSingle()
    circSprites = pygame.sprite.LayeredUpdates()
    buttonSprites = pygame.sprite.Group()  # @UnusedVariable
    starSprites = pygame.sprite.LayeredUpdates()
    caughtSprite = pygame.sprite.GroupSingle()
    dieingSprites = pygame.sprite.GroupSingle()
    scoreSprite = pygame.sprite.GroupSingle()
    pBox = playBox() # a jukebox for handling music settings.


    ring = Ring(c.CENTER, stock.campaign["Ring"], stock.campaign["Ring Glow"], c.FULLSCREEN)
    '''CREATE IMAGES'''
    ring.add(ringSprite, allSprites)
    scoreboard = Scoreboard(c.DISPLAY_W, c.DISPLAY_H)
    scoreboard.add(scoreSprite, allSprites)
    box_img = stock.campaign["RGB Light"]
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    OGBackground = background.copy()

    '''INSTANTIATING OTHER VARIABLES'''
    rotAngle = 0      # background rotation angle
    waitCounterCirc = 0
    waitCounterStar = 0
    circleWaitStart = 0
    circleWaitMade = 0
    starWaitStart = 0
    starWaitMade = 0
    finishedCircleActions = False
    finishedStarActions = False
    circleAction = '_'
    starAction = '_'
    counter = 0
    starWaiting = False
    circleWaiting = False
    pauseStartTime = None #datetime variable
    pauseEndTime = None #datetime variable
    r = 0
    g = 0
    b = 0
    pause_selection = 0
    total_input = 0
    fpsList = []
    toggle_color_r = False
    toggle_color_g = False
    toggle_color_b = False
    display_sprites = True
    controls = c.CONTROL_LIST
    leftHold = False
    rightHold = False
    upHold = False
    downHold = False
    #quitGame = False  # if user returns a True from pause, we quit game, etc.
    startTime = 0
    genList = os.path.join(c.DATA_DIR, 'campaign_commands/genCommands.txt')
    circleList = os.path.join(c.DATA_DIR, 'campaign_commands/circleCommands.txt')
    starList = os.path.join(c.DATA_DIR, 'campaign_commands/starCommands.txt')
    genList, circleList, starList = commander(c, 
                                              genList, 
                                              circleList, 
                                              starList ) # commander takes the 
    #                     commands.txt and converts it into a formatted list.
    circleList, starList = iter(circleList), iter(starList)
    
    # take in the genList parameters now, before the level begins.
    for loop in range(len(genList)):
        setting = genList[loop]
        if setting[0] == 'B':
            # if the command is BPM, set the proper variables.
            pBox.cWait = setting[1]
            pBox.fWait = setting[2]
            pBox.cSpeed = setting[3]
            pBox.fSpeed = setting[4]
        elif setting[0] == 'J':
            __startTime = setting[1] #different startTime, unused
        # change the general speed for circles/stars
        elif setting[0][0] == 'W':
            if setting[0] == 'WG':
                pBox.cWait = setting[1]
                pBox.fWait = setting[1]
            elif setting[0] == 'WC':
                pBox.cWait = setting[1]
            elif setting[0] == 'WF':
                pBox.fWait = setting[1]
    
    
    
    
    
    
    
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


    debug(c.DEBUG, "Variable and object instantiating successful.")
    showSplashScreen(c, stock)
    songLength = store.music["Spicy Chips"].get_length()
    #pygame.mixer.music.set_endevent(USEREVENT)
    debug(c.DEBUG, "Song loading successful, main game loop about to begin.")
    # --Main Game Loop//--
    playing_campaign = True
    startTime = datetime.datetime.now()
    pygame.mixer.music.play()
    while playing_campaign:
        counter += 1
        waitCounterCirc += 1
        waitCounterStar += 1
        # Paint the background
        #c.DISPLAYSURFACE.fill((0,0,0))
        #c.DISPLAYSURFACE.blit(background, background_rect)
        #if not c.FULLSCREEN:
         #   if counter%2 == 0:
          #      background, background_rect, rotAngle = \
           #     rotateBackground(c.CENTER, OGBackground, counter, rotAngle)
            
            
            
            
            
        """LOGGING output information: FPS, event info, AA, etc."""
        # for every 30 or FPS number of frames, print an average fps.
        fpsList.append(c.FPSCLOCK.get_fps())
        if counter == (c.FPS):
            AverageFPS = mean(fpsList)
            debug(c.DEBUG, ("Average FPS: {0}".format(AverageFPS)))
            debug(c.DEBUG, ("Current Score: {0}".format(scoreboard.scoreString)))
            counter = 0
            pygame.display.set_caption('RGB. FPS: {0}'.format(mean(fpsList)))
            fpsList = []
            
            #===================================================================
            # this includes other things that i feel like should only be done 
            # once a second, to save computation time, such as song ending check
            #===================================================================
            # test real quick to see if the song is over.
            deltaTime = (datetime.datetime.now() - startTime).total_seconds()
            if deltaTime > songLength  :
                timeMessage = "SongTime: {0}, GameTIme: {1}".format(songLength, 
                                                                    deltaTime)
                debug(c.DEBUG, timeMessage)
                pygame.mixer.music.stop()
                playing_campaign = False
                debug(c.DEBUG, "MUSIC ENDED, CAMPAIGN SESSION OVER")



        """TAKE ACTION COMMAND LIST"""
        # for every new action, if the wait was long enough, perform the action
        if not circleWaiting:
            if not finishedCircleActions:
                try:
                    circleAction = circleList.next()
                except:
                    finishedCircleActions = True
            # if the circleAction is to spawn a circle/star, gotta que it up.
            if circleAction[0] == 'C':
                circleWaiting = True
            # change the general speed for circles/stars
            elif circleAction[0] == 'CS':
                if circleAction[0] == 'CS':
                    pBox.cSpeed = circleAction[1]
            elif circleAction[0][0] == 'W':
                if circleAction[0] == 'W':
                    circleWaitStart = datetime.datetime.now()
                    circleWaiting = True
                    circleWaitMade = datetime.datetime.now() # time started waiting
                elif circleAction[0] == 'WC':
                    pBox.cWait = circleAction[1]
            elif circleAction[0] == 'S':
                pygame.mixer.music.stop()
                playing_campaign = False
        if circleWaiting:
            # All main actions have to wait before they can be performed,
            # so once an action is read, waiting becomes True, and we test to
            # see if the time passed is valid for the given wait time.
            if circleAction[0] == 'C':
                if waitCounterCirc >= pBox.cWait:
                    if circleAction[2] == '':
                        # if there is no given speed, then it's the global
                        # speed. . .
                        tempSpeed = pBox.cSpeed
                    else:
                        tempSpeed = circleAction[2]
                    tempColor = circleAction[1]
                    debug(c.DEBUG, ("{0}'s speed: {1}".format(tempColor, tempSpeed)))
                    tempCirc = Circle(stock.campaign['Circle'], 
                                      c.CENTER, 
                                      tempSpeed, 
                                      tempColor, 
                                      pBox.layer)
                    tempCirc.add(circSprites, allSprites)
                    circMade = datetime.datetime.now() #for debugging
                    pBox.layer += 1 #determines which get drawn on top
                    circleWaiting = False 
                    waitCounterCirc = 0
            elif circleAction[0] == 'W':
                change = datetime.datetime.now() - circleWaitStart
                # if the action is to JUST wait x amount of time
                if change.total_seconds() >= circleAction[1] / c.FPS:
                    circleWaiting = False
                    totalWaitTime = datetime.datetime.now() - circleWaitMade 
                    debug(c.DEBUG, ("Wait Time: ", totalWaitTime.total_seconds()))
                    waitCounterCirc = 0









        if not starWaiting:
            if not finishedStarActions:
                try:
                    starAction = starList.next()
                except:
                    finishedStarActions = True
            if starAction[0] == 'F':
                starWaiting = True
            # change the general speed for circles/stars
            elif starAction[0] == 'FS':
                    pBox.fSpeed = starAction[1]
            elif starAction[0][0] == 'W':
                if starAction[0] == 'W':
                    starWaitStart = datetime.datetime.now()
                    starWaiting = True
                    starWaitMade = datetime.datetime.now() # for debug purposes
                elif starAction[0] == 'WF':
                    pBox.fWait = starAction[1]
            elif starAction[0] == 'S':
                pygame.mixer.music.stop()
                playing_campaign = False
        if starWaiting:
            if starAction[0] == 'F':
                if waitCounterStar >= pBox.fWait:
                    if starAction[2] == '':
                        tempSpeed = pBox.fSpeed
                    else:
                        tempSpeed = starAction[2]
                    tempAngle = starAction[1]
                    images = (stock.campaign['Star Lit'],stock.campaign['Star Unlit'])
                    tempStar = Star(images, c.CENTER, tempSpeed, tempAngle)
                    tempStar.add(starSprites, allSprites)
                    # no longer waiting, bring on the next starAction!
                    starWaiting = False
                    waitCounterStar = 0
            elif starAction[0] == 'W':
                change = datetime.datetime.now() - starWaitStart
                # if the starAction is to JUST wait x amount of time
                if change.total_seconds() >= starAction[1] / c.FPS:
                    starWaiting = False
                    totalWaitTime = datetime.datetime.now() - starWaitMade 
                    debug(c.DEBUG, ("Wait Time: ", totalWaitTime.total_seconds()))
                    waitCounterStar = 0
                    # we must also set the wait for the next starAction to 0,
                    # or else the wait would be Wx + Wcircle/star.


        
        
        
        
        

        
        
        
        
        
        
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                playing_campaign = False
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                if c.DEBUG:
                    # quit game
                    playing_campaign = False
                    pygame.mixer.music.stop()
                else:
                    # have to time how long pause takes, for the wait.
                    pauseStartTime = datetime.datetime.now()
                    pause_selection = pause(c, stock, c.DISPLAYSURFACE)
                    pauseEndTime = datetime.datetime.now()
                    pauseTotalTime = (pauseEndTime - pauseStartTime)
                    starWaitStart += pauseTotalTime
                    circleWaitStart += pauseTotalTime
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == controls[0]:
                r = 255
                toggle_color_r = True
                total_input += 1
                ring.glowColor((r, g, b))
            elif event.type == KEYUP and event.key == controls[0]:
                r = 0
                toggle_color_r = False
                total_input += -1
                ring.glowColor((r, g, b))
            elif event.type == KEYDOWN and event.key == controls[1]:
                g = 255
                toggle_color_g = True
                total_input += 1
                ring.glowColor((r, g, b))
            elif event.type == KEYUP and event.key == controls[1]:
                g = 0
                toggle_color_g = False
                total_input += -1
                ring.glowColor((r, g, b))
            elif event.type == KEYDOWN and event.key == controls[2]:
                b = 255
                toggle_color_b = True
                total_input += 1
                ring.glowColor((r, g, b))
            elif event.type == KEYUP and event.key == controls[2]:
                b = 0
                toggle_color_b = False
                total_input += -1
                ring.glowColor((r, g, b))
            # Ring Spinning
            elif event.type == KEYDOWN and event.key == controls[5]:
                leftHold = True
                if upHold:
                    ring.spin('upleft')
                elif downHold:
                    ring.spin('downleft')
                else:
                    ring.spin('left')
            elif event.type == KEYUP and event.key == controls[5]:
                leftHold = False
            elif event.type == KEYDOWN and event.key == controls[6]:
                rightHold = True
                if upHold:
                    ring.spin('upright')
                elif downHold:
                    ring.spin('downright')
                else:
                    ring.spin('right')
            elif event.type == KEYUP and event.key == controls[6]:
                rightHold = False
            elif event.type == KEYDOWN and event.key == controls[3]:
                upHold = True
                if leftHold:
                    ring.spin('upleft')
                elif rightHold:
                    ring.spin('upright')
                else:
                    ring.spin('up')
            elif event.type == KEYUP and event.key == controls[3]:
                upHold = False
            elif event.type == KEYDOWN and event.key == controls[4]:
                downHold = True
                if leftHold:
                    ring.spin('downleft')
                elif rightHold:
                    ring.spin('downright')
                else:
                    ring.spin('down')
            elif event.type == KEYUP and event.key == controls[4]:
                downHold = False

            #====================================
            # --non-game-play events//--
            #====================================
            # if O is pressed, toggle context display -------TO BE REMOVED SOON
            elif event.type == KEYDOWN and event.key == K_o:
                if display_sprites == True:
                    display_sprites = False
                else:
                    display_sprites = True
            # if P is pressed, pause game.
            elif event.type == KEYUP and event.key == controls[7]:
                # have to time how long pause takes, for the wait.
                pauseStartTime = datetime.datetime.now()
                pause_selection = pause(c, stock, pygame.display.get_surface())
                pauseEndTime = datetime.datetime.now()
                pauseTotalTime = (pauseEndTime - pauseStartTime)
                starWaitStart += pauseTotalTime
                circleWaitStart += pauseTotalTime
            
            """LOGGING of inputs"""
            if event.type == KEYDOWN or event.type == KEYUP:
                debug(c.DEBUG, (pygame.event.event_name(event.type), event.dict))

        if pause_selection == 3:
            pygame.mixer.music.stop()
            playing_campaign = False
            return
        
        """CATCH CIRCLES MATCHING COLORS"""
        # catch matching circles!!
        for circle in circSprites.sprites():
            if circle.catchable:
                # catchable becomes true when the circle comes in contact 
                # with the ring.
                debug(c.DEBUG, (circle.color, (r, g, b)))
                circle.add(caughtSprite)
                circle.remove(circSprites)
                circle.catch()
                totalCircTime = datetime.datetime.now() - circMade

        """REPEATED POINTS HOLDING COLORS CAUGHT"""
        # every .1 seconds should add or remove points based on accuracy
        if not (caughtSprite.sprite is None):
            for circle in caughtSprite.sprites():
                if circle.color == (r, g, b) and not(circle.dieing):
                    debug(c.DEBUG, ("CIRCTIME: ", totalCircTime.total_seconds()))
                    #if the circle is more than 1 color, than we give bonus
                    if circle.color[0]+circle.color[1]+circle.color[2] >255:
                        scoreboard.addScore(40)
                    else:
                        scoreboard.addScore(20)
                    circle.remove(caughtSprite)
                    circle.add(dieingSprites)
                else:
                    circle.remove(caughtSprite)
                    circle.add(dieingSprites)
                    scoreboard.addScore(-10)


        # a circle begins in circSprites, then hits the ring, gets caught, and
        # goes into "caughtSprite" group. From there, it tries to match with
        # the user's input, then dies and goes into the "dieingCircs" group.
        # the purpose of the last group is just to have it animate the fading
        # or "dieing" sequence before disappearing.
        for circle in dieingSprites.sprites():
            circle.death()



        """DELETE FREE STARS SHOOTING"""
        for star in starSprites.sprites():
            
            if star.travDist >= (264-star.speed) and not(star.shooting):
                # this tests the stars' distance, once it's close enough. . .
                if not((ringSprite.sprite.angle)%360 == (star.angleDeg)%360):
                    debug(c.DEBUG, "Star Died at:")
                    debug(c.DEBUG, ("Ring Angle: ", ringSprite.sprite.angle) )
                    debug(c.DEBUG, ("Star Angle: ", star.angleDeg))
                    star.kill()
                    scoreboard.addScore(-30)
                else:
                    debug(c.DEBUG, "Star Made it at:")
                    debug(c.DEBUG, ("Ring Angle: ", ringSprite.sprite.angle) )
                    debug(c.DEBUG, ("Star Angle: ", star.angleDeg))
            if star.shooting:
#                 debug(c.DEBUG, 'I AM SHOOTING1!')
                # if the star has gone off the screen in the x or y direction
                # kill it and add points!!
                if star.pos[0] > c.DISPLAY_W or star.pos[0] < 0:
                    star.kill()
#                     debug(c.DEBUG, 'KILLED A STAR')
                    scoreboard.addScore(50)
                elif star.pos[1] > c.DISPLAY_H or star.pos[1] < 0:
                    star.kill()
#                     debug(c.DEBUG, 'KILLED A STAR')
                    scoreboard.addScore(50)
#         debug(c.DEBUG, ('Stars #: {0}'.format(len(starSprites.sprites())))

        """DISPLAY SPRITE TOGGLE"""
        allSprites.update()
        if display_sprites == True:
            dieingSprites.draw(c.DISPLAYSURFACE)
            caughtSprite.draw(c.DISPLAYSURFACE)
            circSprites.draw(c.DISPLAYSURFACE)
            starSprites.draw(c.DISPLAYSURFACE)
            ringSprite.draw(c.DISPLAYSURFACE)
            if toggle_color_r:
                c.DISPLAYSURFACE.blit(r_letter, r_letter_rect)
            if toggle_color_g:
                c.DISPLAYSURFACE.blit(g_letter, g_letter_rect)
            if toggle_color_b:
                c.DISPLAYSURFACE.blit(b_letter, b_letter_rect)
            c.DISPLAYSURFACE.blit(box_img, box_rectR)
            c.DISPLAYSURFACE.blit(box_img, box_rectG)
            c.DISPLAYSURFACE.blit(box_img, box_rectB)
            scoreSprite.draw(c.DISPLAYSURFACE)
            c.DISPLAYSURFACE.blit(versionID, (0,0))

        """DELAY"""
        c.FPSCLOCK.tick_busy_loop(c.FPS)

        """UPDATE"""
        pygame.display.flip()  # update()


    return

if __name__ == "__main__":
    from stock import Stock
    from store import Store
    
    
    c = Constants()
    stock = Stock(c)
    store = Store(c)
    background = load_image(c, 'starBG.png')
    background_rect = background.get_rect()

    # CUTTING the background to fit the DISPLAYSURFACE
    background = background.subsurface((0,0), (c.DISPLAY_W , c.DISPLAY_H))
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    
    campaign(c, background, stock, store)


