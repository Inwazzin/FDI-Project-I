from imports import *

class Palette(object):
    def __init__(self):
        # Color Palette
        self.blue: pg.Color = pg.Color(25, 126, 205)
        self.red: pg.Color = pg.Color(205, 126, 25)
        self.neutral: pg.Color = pg.Color(207, 207, 196)
        self.background: pg.Color = pg.Color(41, 41, 37)

        # Button Palette
        self.button_active = pg.Color(120,20,40)
        self.button_passive = pg.Color(80,80,50)
