from imports import *

class Font(object):
    def __init__(self):
        """
        self.emoji - Font Supporting Emoji : Segoe UI Emoji\n
        self.font - Font For regular text : Patrick Hand SC
        """
        freetype.init()
        self.__path: str = 'resources/font'

        self.emoji: freetype.Font = freetype.Font(f'{self.__path}/seguiemj.ttf')

        self.font: freetype.Font = freetype.Font(f'{self.__path}/PatrickHandSC-Regular.ttf')
