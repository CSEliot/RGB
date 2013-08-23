import sys, os
from debug import debug

def log(c):
    #===========================================================================
    # DEF: changes print output to be directed to a log file and test
    # if full-screen works.
    # OUT: original sys.stdout or new sys.stdout
    #         rep
    # Input: the original stdout, log file
    #
    #===========================================================================
    saveDir = os.path.join(c.DATA_DIR, 'logs/log-{0}.txt'.format(c.DATE))
    # --TESTING the full-screen function//--
    #     for i in range(2):  # @UnusedVariable
    #         try:
    #             # toggle_fullscreen returns a 1/0 based on if it worked
    #             attempt_fullscreen = pygame.display.toggle_fullscreen()
    #             scn_tst = "About the full-screen, there were no errors boss!"
    #         except Exception as e:
    #             attempt_fullscreen = "Fullscreen Failed"
    #             scn_tst = "Full-screen error({0}): {1}".format(e.errno, e.strerror)
    # --LOGGING
    # if the original location to print out to is the same as current.
    # meaning, if it is still printing to the screen.
    if c.OG_STDOUT == sys.stdout:
        # create a file to print to.
        logFile = open(saveDir, 'a')
        # set the sys.stdout equal to the file we're writing to.
        sys.stdout = logFile
        debug(c.DEBUG, "LOGGING TO FILE BEGINNING--")
        debug(c.DEBUG, c.DATE)
        debug(c.DEBUG, "Display Info: {0}, {1}".format(c.whichDisplay, c.screenError))


    else:
        debug(c.DEBUG, "LOGGING TO FILE ENDING--")
        sys.stdout = c.OG_STDOUT
        return

