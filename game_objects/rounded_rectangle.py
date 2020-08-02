from imports import *

class RoundedRect(object):
    def __init__(self,
                 rect: pg.Rect,
                 color: pg.Color,
                 roundness: float = 0.5):
        self.__color: pg.Color = color
        self.__alpha: int = self.__color.a
        self.__color.a = 0

        self.rect: pg.Rect = pg.Rect(*rect)
        self.pos = self.rect.topleft
        self.__shape = pg.Surface((200, 300))
        self.__roundness: float = roundness

        self.border_up: int = rect.y
        self.border_down: int = rect.y + rect.h
        self.border_left: int = rect.x
        self.border_right: int = rect.x + rect.w
        self.__update_shape()

    def render(self, screen: pg.Surface):
        screen.blit(self.__shape, self.pos)

    def __update_shape(self):
        if self.__alpha == 0: return

        rectangle = pg.Surface(self.rect.size, pg.SRCALPHA)
        circle = pg.Surface([min(self.rect.size) * 3] * 2, pg.SRCALPHA)
        pg.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
        circle = pg.transform.smoothscale(circle, [int(min(self.rect.size) * self.__roundness)] * 2)
        self.rect.topleft = (0, 0)

        radius: pg.Rect
        radius = rectangle.blit(circle, (0, 0))

        radius.bottomright = self.rect.bottomright
        rectangle.blit(circle, radius)

        radius.topright = self.rect.topright
        rectangle.blit(circle, radius)

        radius.bottomleft = self.rect.bottomleft
        rectangle.blit(circle, radius)

        rectangle.fill((0, 0, 0), self.rect.inflate(-radius.w, 0))
        rectangle.fill((0, 0, 0), self.rect.inflate(0, -radius.h))
        rectangle.fill(self.__color, special_flags=pg.BLEND_RGBA_MAX)
        rectangle.fill((255, 255, 255, self.__alpha), special_flags=pg.BLEND_RGBA_MIN)
        self.__shape = rectangle

    def set_color(self, color: pg.Color):
        if self.__color != color:
            self.__color = color
            self.__color.a = 0
            self.__update_shape()

    def set_alpha(self, alpha: int):
        if self.__alpha != alpha:
            self.__alpha = alpha
            self.__update_shape()

    def set_rect(self, rect: pg.Rect):
        if self.rect != rect:
            self.rect = rect
            self.pos = self.rect.topleft
            self.__update_shape()

    def set_width(self, width: int):
        if self.rect.w != width:
            self.rect.w = width
            self.__update_shape()

    def get_width(self):
        return self.rect.w