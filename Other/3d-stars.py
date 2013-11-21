""" 3d-stars.py -- Korruptor Jan 2001, test code for Seal Basher (v1.0)

This is an example of a 3D star field, another staple demo effect... I don't think
it's very elegant, neat or optimized, but it shows how 3D starfields are made.

Interesting things to do: 
    add rotation, 
    do it for all axis,
    do progressive erasure so the 'closer' the star is to the screen the larger the trail behind it,
    make close stars fater,
    do it with sprites instead of pixel fills...
    etc."""
    
import pygame, pygame.transform
from random import *
from pygame.surfarray import *
from pygame.locals import *
from numpy import *

# ------------------------------------------------------------------------------------
# Glob decs

# Screen resolution...
RES 	= array((1100,700))

# We use this to provide the upper and lower bands of the initial x,y randomisation
# and then as a modifier to shift negative x,y values back into our screen display range 
RANGE_X   = RES[0]/2
RANGE_Y   = RES[1]/2

# An array of star positions Z,X,Y -- [In|De]crease length for different star numbers...
STARS      = zeros((300,3))
COORDS     = zeros((300,2))

# Initialise an array for storing RGB tuples
COLOUR_MAP = [[]] * 256

# Constants...
global MAXSTARS
global MAXZ  
global NUMSTARS 

# ------------------------------------------------------------------------------------
def main():
    "Inisalises display, precalculates the cosine values, and controls the update loop"
    
    # Change this and the length of the STARS array for more stars...
    MAXSTARS = 150
    # The number of live stars...
    NUMSTARS = 0 
    
    # Initialise pygame, and grab an 8bit display.
    pygame.init()
    screen_surface = pygame.display.set_mode(RES, 0, 8)

    # setup the screen palette...
    for i in range(256):
        COLOUR_MAP[i] = (255-i,255-i,255-i)
    #COLOUR_MAP[255] = (0,0,0)
    #print COLOUR_MAP
    # Slap the palette onto our display
    screen_surface.set_palette(COLOUR_MAP)


    # Create an initial star set...
    NUMSTARS = create_stars(NUMSTARS,MAXSTARS)
    FPSCLOCK = pygame.time.Clock()

    # Fruity loops...
    while 1:
    
        # Have we received an event to close the window?
        for e in pygame.event.get():
            if e.type in (QUIT,KEYDOWN,MOUSEBUTTONDOWN):
                return

        # Right, check for dead stars and make some new ones...
        NUMSTARS = create_stars(NUMSTARS, MAXSTARS)
        # Then update our star positions...
        NUMSTARS = update_stars(NUMSTARS, MAXSTARS,screen_surface)
        # Show the results to our audience...

        pygame.display.update()
        screen_surface.fill((0,0,0))
        FPSCLOCK.tick_busy_loop(30)
        print FPSCLOCK.getFps()
        pygame.display.flip()
# ------------------------------------------------------------------------------------
def update_stars(nstars,mstars,screen):
    "Erase old stars, and update the new ones before drawing them again..."

    # Loop through each star...
    for i in range(0,mstars):

        # Check the z-value for the star. If it's 0 we know we've found a dead star...
        if(STARS[i][0] == 0):
            # Ignore this and check the next star...
            nstars - 1
            continue
        else:
            # Ooo, we gotta live one. Erase it...
            screen.fill((0,0,0), (COORDS[i][0], COORDS[i][1], 1, 1))            
        
            # Calculate the new x/y coords for the star (This bitta maths nicked from Vulture/OUTLAW)...
            COORDS[i][0] = ((256 * STARS[i][1]) / STARS[i][0]) + RANGE_X
            COORDS[i][1] = ((256 * STARS[i][2]) / STARS[i][0]) + RANGE_Y
                    
            # Bounds check the values for x and y... Kill the star if it's offscreen...
            if((COORDS[i][0] > (RES[0])) or (COORDS[i][1] > (RES[1]))):
                STARS[i][0] = 0
                STARS[i][1] = 0
                STARS[i][2] = 0
                # Decrement the number of live stars so the next call to create_stars will make a new one...
                nstars -= 1
                continue
            i = int(i)
            # Draw the star's new position to the screen using the colour specified in the colour_map...
            screen.fill(COLOUR_MAP[STARS[i][0]], (COORDS[i][0], COORDS[i][1], 1, 1))            

            # Decrement the z value for the star... (Increment to zoom out)
            # Not checking for the z value == 1 caused a bastard bud I've been hunting all night :)
            if (STARS[i][0] < 4):
                STARS[i][0] -= 1
                nstars -= 1
            else:
                STARS[i][0] -= 1
                
    return nstars
# ------------------------------------------------------------------------------------
def create_stars(nstars, mstars):
    "Check for empty array slots and create a new star in there..."

    # If we've got enough stars already...
    if(nstars >= mstars):
        # Don't do anything...
        return nstars
    else:
        # Find the dead star...
        for i in range(0,mstars):
            if(STARS[i][0] < 1):
                # Create a new star in it's place...
                STARS[i][0] = 255
                STARS[i][1] = randrange(negative(RANGE_X),RANGE_X,1)
                STARS[i][2] = randrange(negative(RANGE_Y),RANGE_Y,1)
                # Increment that number of live stars...
                nstars += 1
    return nstars
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------

# Ahead warp fact 1 Mr Sulu...
if __name__ == '__main__': main()

# End of sauce. Pass the chips...


