"""errorbox, by Pete Shinners

Tries multiple python GUI libraries to display an error box
on the screen. No matter what is successful, the error will also
be sent to stdout. For GUI platforms, this can be a lot nicer than
opening a shell with errors dumped into it.

Call the "errorbox()" function with an error title and error message.

The different GUI libraries will leave the program in undefined
states, so this function will never return, but instead end the
program when the error has been dismissed. That makes this only
useful for errors, and not general message boxes.

Feel free to perhaps add some GUI handlers, as well as enhance
any that are here. They have all been tested on their appropriate
platforms.

There is even a decent pygame handler, if all else fails.

Use it to report things like missing modules (image, numeric, etc?).
Perhaps pygame raised an exception while initializing. This little
messagebox can sure be a lot nicer than a stack trace. ;]
"""

import sys
import os
import pygame, pygame.font
from pygame.locals import *


def errorbox(title, message):
    "attempt to error with a gui"
    global handlers
    __stdout(title, message)
    for e in handlers:
        try:
            e(title, message)
            break
        except (ImportError, NameError): pass
    raise SystemExit



def __wxpython(title, message):
    from wxPython.wx import *
    class LameApp(wxApp):  # @UndefinedVariable
        def OnInit(self): return 1
    app = LameApp()  # @UnusedVariable
    dlg = wxMessageDialog(None, message, title, wxOK|wxICON_EXCLAMATION)  # @UndefinedVariable
    dlg.ShowModal()
    dlg.Destroy()


def __gtk(title, message):
    import GtkExtra  # @UnresolvedImport
    GtkExtra.message_box(title, message, ['Ok'])
   

def __tkinter(title, message):
    import Tkinter, tkMessageBox
    Tkinter.Tk().wm_withdraw()
    tkMessageBox.showerror(title, message)


def __pygame(title, message):

    try:


        pygame.quit() #clean out anything running
        pygame.display.init()
        pygame.font.init()
        screen = pygame.display.set_mode((460, 140))
        pygame.display.set_caption(title)
        font = pygame.font.SysFont('arial', 18)
        foreg = 0, 0, 0
        backg = 200, 200, 200
        liteg = 255, 255, 255
        ok = font.render('Ok', 1, foreg)
        screen.fill(backg)
        okbox = ok.get_rect().inflate(20, 10)
        okbox.centerx = screen.get_rect().centerx
        okbox.bottom = screen.get_rect().bottom - 10
        screen.fill(liteg, okbox)
        screen.blit(ok, okbox.inflate(-20, -10))
        pos = [20, 20]
        for text in message.split('\n'):
            msg = font.render(text, 1, foreg)
            screen.blit(msg, pos)
            pos[1] += font.get_height()

        pygame.display.flip()
        while 1:
            e = pygame.event.wait()
            if e.type == QUIT or e.type == MOUSEBUTTONDOWN or \
                       (e.type == KEYDOWN and e.key in (K_ESCAPE, K_SPACE, K_RETURN)):
                break
        pygame.quit()
    except pygame.error:
        raise ImportError


def __stdout(title, message):
    text = 'ERROR: ' + title + '\n' + message
    print text

handlers = __gtk, __tkinter, __wxpython, __pygame


#test the error box
if __name__ == '__main__':
    errorbox("Testing", "This is only a test.\nHad this been " + \
          "a real emergency, you would be very afraid." )
