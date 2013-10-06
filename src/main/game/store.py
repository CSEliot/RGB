from loader import load_sound, load_song

class Store(object):
    '''
    Stores all the sound/music files.
    '''


    def __init__(self, c):
        # music is actually streamed, so we don't load it. . . so this is kinda
        # sorta mostly useless, for now.
        self.music = {"It's Melting": load_sound(c, "music/It's Melting.ogg"), 
                      "Spicy Chips": load_sound(c, "music/Spicy Chips.ogg"),
                      "The Power Supply": load_sound(c, "music/The Power Supply.ogg"),
                      "menu": load_sound(c, "music/menuV3.ogg"),
                      "menu2": load_sound(c, "music/Space1 by alaupas.ogg")
                      }
        
        self.sounds = {"Enter 1": load_sound(c, "enter 1.ogg"),
                       "Enter 2": load_sound(c, "enter 2.ogg"),
                       "Enter 3": load_sound(c, "enter 3.ogg"),
                       "scroll": load_sound(c, "scroll.ogg"),
                       "test": load_sound(c, "test.ogg")
                       }
        # set volume by a factor of current volume.
        self.sounds["Enter 1"].set_volume(self.sounds["Enter 1"].get_volume()/35.0)
        self.sounds["Enter 2"].set_volume(self.sounds["Enter 2"].get_volume()/35.0)
        self.sounds["Enter 3"].set_volume(self.sounds["Enter 3"].get_volume()/35.0)
        self.sounds["scroll"].set_volume(self.sounds["scroll"].get_volume()/30.0)
        
        