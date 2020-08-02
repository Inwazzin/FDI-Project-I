from imports import *
from resources.font import Font


class TextObject(object):
    def __init__(self,
                 pos: Tuple[int, int],
                 str_: str,
                 size: int,
                 style: int = 0,
                 color: pg.Color = pg.Color(0, 0, 0, 0),
                 is_centered: bool = True,
                 is_emoji: bool = False):
        font = Font()
        self.__font = font.emoji if is_emoji else font.font
        self.__str = str_
        self.__size = size
        self.__style = style
        self.__color: pg.Color = pg.Color(*color)
        self.__color.a = 255

        self.pos: pg.Vector2 = pg.Vector2(pos)

        self.__offset: pg.Vector2 = pg.Vector2(0, 0)
        self.__str_size: pg.Rect = pg.Rect(0, 0, 0, 0)
        self.__is_centered = is_centered
        self.shape: Optional[pg.Surface] = None

        self.__update_shape()

    def __update_shape(self):
        offset: pg.Rect
        self.shape, self.__str_size = self.__font.render(text=self.__str,
                                                         fgcolor=self.__color,
                                                         style=self.__style,
                                                         rotation=0,
                                                         size=self.__size)

        self.__offset.x = self.pos.x - self.__str_size.w // 2 * self.__is_centered
        self.__offset.y = self.pos.y - self.__str_size.h // 2

    def render(self, screen: pg.Surface):
        screen.blit(self.shape, self.__offset)

    def set_str(self, str_: str):
        if str_ != self.__str:
            self.__str = str_
            self.__update_shape()

    def set_size(self, size: int):
        if size != self.__size:
            self.__size = size
            self.__update_shape()

    def set_style(self, style):
        if style != self.__style:
            self.__style = style
            self.__update_shape()

    def set_color(self, color: pg.Color):
        if color != self.__color:
            self.__color = color

    def get_offset(self):
        return self.__offset

    def get_str_width(self):
        return self.__str_size.w

    def __repr__(self):
        return f'TextObject({self.__str} @{self.pos})'
