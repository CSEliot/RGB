import sys, os, pygame # @UnusedImport
from pygame.compat import geterror # @UnusedImport
from debug import debug



def commander(c):
    # this function opens the commands.txt file and converts it into a list of
    # commands on how to play the level accompanying the song and put them into
    # a list. If a command is unrecognized, the game will close (for now).
    # It will take the commands and their parameters and organize them into a
    # 2D list
    # RETURNS: A list of lists
    # DEFAULT VALUES
    ringSize = 265
    bpm = 60
    cSpeed = 10
    sSpeed = 10
    cWait = 1
    sWait = 1
    saveDir = os.path.join(c.DATA_DIR, 'commands.txt')
    try:
        commandsFile = open(saveDir, 'r')
    except pygame.error:
        debug(c.DEBUG, ('Cannot open file: ', saveDir))
        raise SystemExit(str(geterror()))
    
    # list of commands
    commands = commandsFile.read()
    commands = commands.split()
    commandList = []
    for action in commands:
        # Option 1: set the BPM
        if action[0] == 'B':
            try:
                bpm = action.replace('BPM', '')
                bpm = float(bpm)
            except Exception:
                raise UserWarning, "Invalid BPM possible. See commands.txt"
                print UserWarning
                sys.exit(UserWarning)
            # calculate the global wait time.
            cWait = (60 / bpm)
            fWait = cWait
            # calculate the move speed of circle and star
            cSpeed = (ringSize / c.FPS) * (bpm / 60.0)
            fSpeed = cSpeed
            # the BPM list is formatted as such:'B', WC, WF, CSP, and FSP
            commandList.append(['B', cWait, fWait, cSpeed, fSpeed])
        elif action[0] == 'P':
            if action == 'Play:':
                commandList.append(['P'])
            else:
                raise UserWarning, "Invalid Play action given. See commands.txt"
                print UserWarning
                sys.exit(UserWarning)
        elif action[0] == 'C':
            color = ''
            # we test to see if the action is for changing speed, or making circ
            if action[1] == 'S':
                try:
                    cSpeed = action.replace('CSP', '')
                    cSpeed = float(cSpeed)
                except Exception:
                    raise UserWarning, "Invalid CSP given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['CS', cSpeed])
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
                    except Exception:
                        raise UserWarning, "Invalid CSpeed given. See commands.txt"
                        print UserWarning
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
                    raise UserWarning, "No colors found. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['C', (R, G, B), cSpeed])
        elif action[0] == 'F':
            if action.find(',') != -1:
                # if both an angle and speed is defined, we must split the
                # numbers by the comma.
                starTemp = action.replace('F', '')
                fAngle, fSpeed = starTemp.split(',')
                try:
                    fAngle = float(fAngle)
                    fSpeed = float(fSpeed)
                except Exception:
                    raise UserWarning, "Invalid  Fx/# given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['F', fAngle, fSpeed])
            else:
                fAngle = action.replace('F', '')
                try:
                    fAngle = float(fAngle)
                except Exception:
                    raise UserWarning, "Invalid  Fx given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['F', fAngle])
        elif action[0] == 'W':
            if action[1].isdigit():
                waitTime = action.replace('W', '')
                # an instance wait, for only that call.
                try:
                    waitTime = float(waitTime)
                except Exception:
                    raise UserWarning, "Invalid W# given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['W', waitTime])
            elif action[1] == 'G':
                # a global constant wait time between each action
                gWait = action.replace('W', '')
                gWait = gWait.replace('G', '')
                try:
                    gWait = float(gWait)
                except Exception:
                    raise UserWarning, "Invalid WG# given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['WG', gWait])
            elif action[1] == 'C':
                # a global constant wait time before each circle creation
                cWait = action.replace('W', '')
                cWait = cWait.replace('C', '')
                try:
                    cWait = float(cWait)
                except Exception:
                    raise UserWarning, "Invalid WC# given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['WC', cWait])
            elif action[1] == 'F':
                # a global constant wait time before each star creation
                fWait = action.replace('W', '')
                fWait = fWait.replace('F', '')
                try:
                    fWait = float(fWait)
                except Exception:
                    raise UserWarning, "Invalid WF# given. See commands.txt"
                    print UserWarning
                    sys.exit(UserWarning)
                commandList.append(['WG', fWait])
        elif action[0] == ':':
            if action == ':Stop':
                commandList.append(['S'])
            else:
                raise UserWarning, "Invalid Stop given. See commands.txt"
                print UserWarning
                sys.exit(UserWarning)
    debug(c.DEBUG, commandList)
    return commandList