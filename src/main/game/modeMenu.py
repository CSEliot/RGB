import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport
from numpy import *  # @UnusedWildImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
from loader import load_image, load_song
from time import sleep
from time import time
from constants import Constants
from debug import *  # @UnusedWildImport

def modeMenu(c, background):
    
    debug(c.DEBUG, "Entering: modeMenu")
    # the background is the current information from the screen. It's faster
    # than grabbing it from the constants file.
    background_rect = background.get_rect()


    # menu elements
    selected = 1  # tells which button is currently highlighted
    buttons = 3  # tells max # selected can reach
    newSelected = True  # tells if something new has been highlighted
    unselected = selected  # used to change unhighlighted button back
    campaignButton = 1  # represents placeholder for button
    creativeButton = 2  # represents placeholder for button
    backButton = 3
    entered = False  # tells if the user has chosen a button

    #Other Variables
    fpsList = []
    fpsWait = 2 #how many seconds till we report the game's FPS.
    frameCount = 0
    


    corners, __corners_rect = load_image(c, "menu/menuBox.png")
    campaign,__campaign_rect = load_image(c, 'menu/campaign.png')
    creative, __creative_rect = load_image(c, 'menu/creative.png')
    logo, __logo_rect = load_image(c, 'menu/logo.png')
    back, __back_rect = load_image(c, 'menu/return.png')  # @UnusedVariable

    # RESIZE TO FIT THE SCREEN.
    # RESIZING VVVVVVVVVVVVVVVVV
    campaignHeight = int(campaign.get_height() * .5)
    campaignWidth = int(campaign.get_width() * .5)
    campaign = pygame.transform.smoothscale(campaign, (campaignWidth, campaignHeight))
    campaign_rect = campaign.get_rect()
    logoHeight = int(logo.get_height() * .5)
    logoWidth = int(logo.get_width() * .5)
    logo = pygame.transform.smoothscale(logo, (logoWidth, logoHeight))
    logo_rect = logo.get_rect()
    creativeHeight = int(creative.get_height() * .5)
    creativeWidth = int(creative.get_width() * .5)
    creative = pygame.transform.smoothscale(creative, (creativeWidth, creativeHeight))
    creative_rect = creative.get_rect()
    backHeight = int(back.get_height() * .5)
    backWidth = int(back.get_width() * .5)
    back = pygame.transform.smoothscale(back, (backWidth, backHeight))  # @ReservedAssignment
    back_rect = back.get_rect()
    cornersHeight = int(corners.get_height() * .5)
    cornersWidth = int(corners.get_width() * .5)
    corners = pygame.transform.smoothscale(corners, (cornersWidth, cornersHeight))
    corners_rect = corners.get_rect()
    # RESIZING ^^^^^^^^^^^^^^^^^
    # menu locations, done both resizing or not.
    campaignPos = c.CENTER[0], c.CENTER[1] - 25  # adjusting by specific pixels
    campaign_rect.center = campaignPos
    logoPos = c.CENTER[0], c.CENTER[1] - 150  # adjusting by specific pixels
    logo_rect.center = logoPos
    creativePos = c.CENTER[0], c.CENTER[1] + 25  # adjusting by specific pixels
    creative_rect.center = creativePos
    backPos = c.CENTER[0], c.CENTER[1] + 75
    back_rect.center = backPos
    # and then the corners, seperate
    corners_rect.center = c.CENTER

    # set original images
    OGcreative = creative.copy()
    OGcampaign = campaign.copy()
    OGback = back.copy()
    OGBackground = background.copy()
    
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
            background = pygame.transform.rotozoom(OGBackground, c.BgAngle%360 , 1)
            background_rect = background.get_rect()
            background_rect.center = c.CENTER
        frameCount += 1
        
        
        """EVENT HANDLING INPUT"""
        # grab all the latest input
        latest_events = pygame.event.get()
        for event in latest_events:
            if event.type == QUIT:
                going = False
                entered = True
                selected = "QUIT"
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                entered = True
                selected = "QUIT"
                going = False
            # --game-play events//--
            elif event.type == KEYDOWN and event.key == K_DOWN:
                if selected < buttons:
                    # set the unselected as the previous selected one.
                    unselected = selected
                    selected += 1
                    newSelected = True
            elif event.type == KEYDOWN and event.key == K_UP:
                if selected > 1:
                    unselected = selected
                    selected -= 1
                    newSelected = True
            elif event.type == KEYDOWN and event.key == K_RETURN:
                entered = True

        if newSelected:
            # revert unselected button back
            newSelected = False
            if unselected == campaignButton:
                campaign = OGcampaign
                campaign_rect.center = campaignPos
            elif unselected == creativeButton:
                creative = OGcreative
                creative_rect.center = creativePos
            elif unselected == backButton:
                back = OGback
                back_rect.center = backPos
            # change image of newly selected
            if selected == campaignButton:
                campaign = pygame.transform.smoothscale(campaign, (campaign_rect.width + 7, \
                                                        campaign_rect.height + 5))
                pgext.color.setColor(campaign, (255, 255, 0))
                campaign_rect.center = campaignPos
            elif selected == creativeButton:
                creative = pygame.transform.smoothscale(creative, (creative_rect.width + 7, \
                                                        creative_rect.height + 5))
                pgext.color.setColor(creative, (0, 255, 255))
                creative_rect.center = creativePos
            elif selected == backButton:
                back = pygame.transform.smoothscale(back, (back_rect.width + 7, \
                                                        back_rect.height + 5))
                pgext.color.setColor(back, (255, 0, 255))
                back_rect.center = backPos






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
            


        # leave menu screen
        if entered:
            sleep(1)
            return selected
        c.DISPLAYSURFACE.fill((0,0,0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        c.DISPLAYSURFACE.blit(corners, corners_rect)
        c.DISPLAYSURFACE.blit(logo, logo_rect)
        c.DISPLAYSURFACE.blit(campaign, campaign_rect)
        c.DISPLAYSURFACE.blit(creative, creative_rect)
        c.DISPLAYSURFACE.blit(back, back_rect)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        c.FPSCLOCK.tick_busy_loop(c.FPS)
        pygame.display.flip()
        #         pygame.transform.set_smoothscale_backend(SSE)



if __name__ == "__main__":
    c = Constants()
    background, background_rect = load_image(c, 'starBG.png')
    mult = 1.6
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    modeMenu(c, background)
