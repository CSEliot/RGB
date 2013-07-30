import sys, os, pygame  # @UnusedImport
from pygame.compat import geterror  # @UnusedImport
from debug import debug



def commander(c, genList, circleList, starList):
    # this function opens the commands.txt file and converts it into a list of
    # commands on how to play the level accompanying the song and put them into
    # a list. If a command is unrecognized, the game will close (for now).
    # It will take the commands and their parameters and organize them into a
    # 2D list
    # RETURNS: A list of lists
    # DEFAULT VALUES
    
    try:
        genFile = open(genList, 'r')
    except pygame.error:
        debug(c.DEBUG, ('Cannot open file: ', genList))
        raise SystemExit(str(geterror()))
    
    
    try:
        circleFile = open(circleList, 'r')
    except pygame.error:
        debug(c.DEBUG, ('Cannot open file: ', circleList))
        raise SystemExit(str(geterror()))
    
    
    try:
        starFile = open(starList, 'r')
    except pygame.error:
        debug(c.DEBUG, ('Cannot open file: ', starList))
        raise SystemExit(str(geterror()))

    # list of general commands
    genCommands = genFile.read()
    genCommands = genCommands.split()
    genCommandList = []

    # list of circle commands
    circleCommands = circleFile.read()
    circleCommands = circleCommands.split()
    circleCommandList = []
    
    
    # list of star commands
    starCommands = starFile.read()
    starCommands = starCommands.split()
    starCommandList = []
    
    for action in genCommands:
        # the action[0] just checks the first letter in the action.
        # Option 1: set the BPM
        if action[0] == 'B':
            try:
                bpm = action.replace('BPM', '')
                bpm = float(bpm)
            except Exception:
                print "Invalid BPM possible. See commands.txt"
                sys.exit(UserWarning)
            # calculate the global wait times.
            # (how many frames until the next action is committed.)
            cWait = c.FPS / (bpm / 60.0)
            fWait = cWait
            # calculate the move speed of circle and star
            # this equation sets the speed as a fraction of the radius of the
            # ring, so that it takes X seconds to reach the ring.
            # the X seconds will either be user defined, or bpm/60
            # (how quickly an action is completed)
            cSpeed = (c.RING_SIZE / c.FPS) * (bpm / 60.0)
            fSpeed = (c.RING_RADIUS / c.FPS) * (bpm / 60.0)
            # the BPM list is formatted as such:'B', WC, WF, CSP, and FSP
            genCommandList.append(['B', cWait, fWait, cSpeed, fSpeed])
        #=======================================================================
        # elif action[0] == 'P':
        #     if action == 'Play:':
        #         commandList.append(['P'])
        #     else:
        #         print "Invalid Play action given. See commands.txt"
        #         sys.exit(UserWarning)
        #=======================================================================
        elif action[0] == 'J':
            if "JumpTo," in action:
                try:
                    startTime = float(action.replace('JumpTo,', ''))
                except Exception:
                    print "Invalid start time given. Must be in seconds. See commands.txt"
                    sys.exit(UserWarning)
                genCommandList.append(['J', startTime])
            else:
                print "Invalid start time given. Must be 'JumpTo,X'. See commands.txt"
                sys.exit(UserWarning)
        elif action[0] == 'W':
            if action[1] == 'G':
                # a global constant wait time between each action
                gWait = action.replace('W', '')
                gWait = gWait.replace('G', '')
                try:
                    gWait = c.FPS * float(gWait)
                except Exception:
                    print "Invalid WG# given. See commands.txt"
                    sys.exit(UserWarning)
                genCommandList.append(['WG', gWait])
            elif action[1] == 'C':
                # a global constant wait time before each circle creation
                cWait = action.replace('W', '')
                cWait = cWait.replace('C', '')
                try:
                    cWait = c.FPS * float(cWait)
                except Exception:
                    print "Invalid WC# given. See commands.txt"
                    sys.exit(UserWarning)
                genCommandList.append(['WC', cWait])
            elif action[1] == 'F':
                # a global constant wait time before each star creation
                fWait = action.replace('W', '')
                fWait = fWait.replace('F', '')
                try:
                    fWait = c.FPS * float(fWait)
                except Exception:
                    print "Invalid WF# given. See commands.txt"
                    sys.exit(UserWarning)
                genCommandList.append(['WF', fWait])
                
                
                
    for action in circleCommands:
        if action[0] == 'C':
            color = ''
            # we test to see if the action is for changing speed, or making circ
            if action[1] == 'S':
                try:
                    cSpeed = action.replace('CSP', '')
                    cSpeed = float(cSpeed)
                    cSpeed = (c.RING_SIZE / c.FPS) / cSpeed
                    debug(c.DEBUG, cSpeed)
                except Exception:
                    print "Invalid CSP given. See commands.txt"
                    sys.exit(UserWarning)
                circleCommandList.append(['CS', cSpeed])
            # if it does not begin with CS, that means it is for making a circle
            else:
                cSpeed = action.replace('C', '')
                cSpeed = cSpeed.replace(',', '')
                # now we iterate through the string, creating a color variable
                # and remove the letters, leaving speed with only numbers.
                # if no speed was given, then the len will be 0, so we can exit.
                while len(cSpeed) != 0 and cSpeed[0].isalpha():
                    debug(c.DEBUG, ('cSpeed2: ', cSpeed))
                    color = color + cSpeed[0]
                    cSpeed = cSpeed.replace(cSpeed[0], '')
                # if anything is left in the variable cSpeed, then it SHOULD be
                # the circle speed number
                if len(cSpeed) != 0:
                    try:
                        cSpeed = float(cSpeed)
                        cSpeed = (c.RING_SIZE / c.FPS) / cSpeed
                    except Exception:
                        print "Invalid CSpeed given. See commands.txt"
                        sys.exit(UserWarning)
                # grab the right colors!
                R, G, B = 0, 0, 0
                debug(c.DEBUG, ("COLOR: ", color))
                if color.find('R') != -1:
                    R = 255
                if color.find('G') != -1:
                    G = 255
                if color.find('B') != -1:
                    B = 255
                if (R, G, B) == (0, 0, 0):
                    print "No colors found. See commands.txt"
                    sys.exit(UserWarning)
                circleCommandList.append(['C', (R, G, B), cSpeed])
        elif action[0] == 'W':
            if action[1] == 'C':
                # a global constant wait time before each circle creation
                cWait = action.replace('W', '')
                cWait = cWait.replace('C', '')
                try:
                    cWait = c.FPS * float(cWait)
                except Exception:
                    print "Invalid WC# given. See commands.txt"
                    sys.exit(UserWarning)
                circleCommandList.append(['WC', cWait])
            elif action[1].isdigit():
                waitTime = action.replace('W', '')
                # an instance wait, for only that call.
                try:
                    # how many frames before the next action occurs
                    waitTime = c.FPS * float(waitTime)
                except Exception:
                    print "Invalid W# given. See commands.txt"
                    sys.exit(UserWarning)
                circleCommandList.append(['W', waitTime])
        elif action[0] == ':':
            if action == ':Stop':
                circleCommandList.append(['S'])
            else:
                print "Invalid Stop given. See commands.txt"
                sys.exit(UserWarning)
                
                
                
                
    for action in starCommands:
        if action[0] == 'F':
            # we test to see if the action is for changing speed, or making star
            if action[1] == 'S':
                try:
                    fSpeed = action.replace('FSP', '')
                    fSpeed = float(fSpeed)
                    fSpeed = (c.RING_RADIUS / c.FPS) / fSpeed
                except Exception:
                    print "Invalid FSP given. See commands.txt"
                    sys.exit(UserWarning)
                starCommandList.append(['FS', fSpeed])
            else:
                if action.find(',') != -1:
                    # if both an angle and speed is defined, we must split the
                    # numbers by the comma.
                    starTemp = action.replace('F', '')
                    fAngle, fSpeed = starTemp.split(',')
                    try:
                        fAngle = float(fAngle)
                        fSpeed = float(fSpeed)
                        fSpeed = (c.RING_RADIUS / c.FPS) / fSpeed
                    except Exception:
                        print "Invalid  Fx/# given. See commands.txt"
                        sys.exit(UserWarning)
                    starCommandList.append(['F', fAngle, fSpeed])
                else:
                    fAngle = action.replace('F', '')
                    try:
                        fAngle = float(fAngle)
                    except Exception:
                        print "Invalid  Fx given. See commands.txt"
                        sys.exit(UserWarning)
                    starCommandList.append(['F', fAngle, ''])
        elif action[0] == 'W':
            if action[1].isdigit():
                waitTime = action.replace('W', '')
                # an instance wait, for only that call.
                try:
                    # how many frames before the next action occurs
                    waitTime = c.FPS * float(waitTime)
                except Exception:
                    print "Invalid W# given. See commands.txt"
                    sys.exit(UserWarning)
                starCommandList.append(['W', waitTime])
            elif action[1] == 'F':
                # a global constant wait time before each star creation
                fWait = action.replace('W', '')
                fWait = fWait.replace('F', '')
                try:
                    fWait = c.FPS * float(fWait)
                except Exception:
                    print "Invalid WF# given. See commands.txt"
                    sys.exit(UserWarning)
                starCommandList.append(['WF', fWait])
            elif action[1].isdigit():
                waitTime = action.replace('W', '')
                # an instance wait, for only that call.
                try:
                    # how many frames before the next action occurs
                    waitTime = c.FPS * float(waitTime)
                except Exception:
                    print "Invalid W# given. See commands.txt"
                    sys.exit(UserWarning)
                starCommandList.append(['W', waitTime])
        elif action[0] == ':':
            if action == ':Stop':
                starCommandList.append(['S'])
            else:
                print "Invalid Stop given. See commands.txt"
                sys.exit(UserWarning)
                
                
                

    debug(c.DEBUG, (genCommandList, circleCommandList, starCommandList))
    return genCommandList, circleCommandList, starCommandList 
