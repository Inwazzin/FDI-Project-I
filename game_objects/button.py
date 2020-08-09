from game_objects.rounded_rectangle import RoundedRect
from game_objects.text_object import TextObject
from resources.color_palette import Palette
from imports import *


class Tile(object):
    def __init__(self,
                 emoji="",
                 rect: pg.Rect = pg.Rect(0, 0, 0, 0),
                 font_color: pg.Color = pg.Color(0, 0, 0, 0),
                 font_size: int = 24,
                 roundness: float = 0.5):
        # Tile Parameters
        self.is_clicked: bool = False
        self.is_right_clicked: bool = False

        # Rounded Rect Parameters
        self.pos = rect
        self.colors: Palette = Palette()
        self.font_color = font_color
        self.rect: RoundedRect = RoundedRect(rect, self.colors.button_passive, roundness)
        self.rect.set_alpha(255)

        # Text Parameters
        self.emoji: TextObject = TextObject((self.pos.x + self.pos.w // 2,
                                             self.pos.y + self.pos.h // 2),
                                            emoji,
                                            font_size,
                                            color=self.font_color,
                                            is_emoji=True)

    def handle_events(self, events: List[pg.event.EventType]):
        self.is_clicked = False
        self.is_right_clicked = False

        # Idle
        if not self._is_mouse_in_borders(*pg.mouse.get_pos()):
            self.rect.set_color(self.colors.button_passive)
        else:
            if any(event.type == pg.MOUSEBUTTONUP and event.button == 1 for event in events):
                self.is_clicked = True
            elif any(event.type == pg.MOUSEBUTTONUP and event.button == 3 for event in events):
                self.is_right_clicked = True
            else:
                self.rect.set_color(self.colors.button_active)

    def render(self, screen: pg.Surface):
        self.rect.render(screen)
        if self.emoji: self.emoji.render(screen)

    def set_emoji(self, emoji):
        self.emoji.set_str(emoji)

    def set_idle_color(self, color: pg.Color):
        self.colors.button_rect_idle = color

    def reset(self):
        self.is_clicked = False

    def _is_mouse_in_borders(self, pos_x, pos_y) -> bool:
        return (self.rect.border_right >= pos_x >= self.rect.border_left
                and self.rect.border_down >= pos_y >= self.rect.border_up)

    def __repr__(self):
        return f'Tile({self.emoji} @{self.rect})'


class Button(Tile):
    """Nawet nie patrz, moje dziecko do zabawy"""
    # RECT BOX | TEXT
    # / --- --- --- \
    # |     TXT     |
    # \ --- --- --- /
    # IDLE | HOVER | CLICK == >= <= /= ===
    def __init__(self,
                 str_: str = "",
                 rect: pg.Rect = pg.Rect(0, 0, 0, 0),
                 font_color: pg.Color = pg.Color(0, 0, 0, 0),
                 font_size: int = 24,
                 text_style=0,
                 roundness: float = 0.5,
                 emoji="",
                 emoji_align=0):

        # Button Parameters
        super().__init__(emoji, rect, font_color, font_size, roundness)
        self._key_time_max: float = 1.5
        self._key_time: float = self._key_time_max

        # Text
        self.text: TextObject = TextObject((self.pos.x + self.pos.w // 2,
                                            self.pos.y + self.pos.h // 2),
                                           str_,
                                           font_size,
                                           text_style)

        self.emoji: Optional[TextObject] = (False
                                            if not emoji
                                            else TextObject((self.pos.x + int(emoji_align * self.pos.w),
                                                             self.pos.y + self.pos.h // 2),
                                                            emoji,
                                                            font_size,
                                                            color=self.font_color,
                                                            is_emoji=True))

    def handle_events(self, events: List[pg.event.EventType]):
        if self.__is_key_time():
            super().handle_events(events)
        else:
            self.rect.set_color(self.colors.button_active)

    def update(self, dt: float):
        self._update_key_time(dt)

    def _update_key_time(self, dt):
        if self._key_time < self._key_time_max:
            self._key_time += dt

    def render(self, screen: pg.Surface):
        super().render(screen)
        self.text.render(screen)

    def __is_key_time(self):
        if self._key_time >= self._key_time_max:
            if self.is_clicked or self.is_right_clicked:
                self._key_time = 0
            return True
        return False

    def reset(self):
        super().reset()
        self._key_time = self._key_time_max

    def __repr__(self):
        return f'Button({self.text}+{self.emoji} @{self.rect})'


class InputButton(Button):
    """Simple Button containing click functionality"""
    def __init__(self,
                 rect: pg.Rect = pg.Rect(0, 0, 0, 0),
                 font_color: pg.Color = pg.Color(0, 0, 0, 0),
                 font_size: int = 24,
                 text_style=0,
                 supported_keys: Tuple[int, ...] = (),
                 number_limit: Optional[float] = None,
                 roundness: float = 0.5,
                 str_: str = ''):
        """
        :param rect: button frame itself (x, y, width, height)
        :param font_color: color of the font
        :param font_size: size of the font
        :param text_style: style of the font
        :param supported_keys: set containing all the allowed strokes
        :param number_limit: limit number which handles contained data within the button by limit's type
        :param roundness: roundness of the rect containing the button
        :param str_: Button Data or displayed text
        """
        # Button Parameters
        super().__init__('', rect, font_color, font_size, text_style, roundness, '')

        # Text
        self.__initial_str: str = str_
        self.__text_offset_width = font_size // 6
        self.__number_limit: Optional[float] = number_limit

        self.__data: str = str(self.__number_limit) if not self.__initial_str else self.__initial_str
        self.__width_limit: int = rect.w
        self.supported_keys: Tuple[int, ...] = supported_keys
        self.text: TextObject = TextObject((self.pos.x + self.__text_offset_width,
                                            self.pos.y + self.pos.h // 2),
                                           self.__data,
                                           font_size,
                                           text_style,
                                           color=self.font_color,
                                           is_centered=False)

    def handle_events(self, events: List[pg.event.Event]):
        """Handles Mouse and Keystrokes"""

        mouse_pos = pg.mouse.get_pos()
        for event in events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.is_clicked = self._is_mouse_in_borders(*mouse_pos)
                self.rect.set_color(self.colors.button_active if self.is_clicked else self.colors.button_passive)
            elif self.is_clicked and event.type == pg.KEYDOWN:
                if event.key in self.supported_keys and self.__is_new_data_valid(self.__data + event.unicode):
                    self.__data = self.__handle_data(event.unicode)

                elif event.key == pg.K_BACKSPACE:
                    self.__data = self.__data[:-1]
                self.__handle_width_limit()

    def __handle_width_limit(self):
        """Handles excessive length of a potential word by disallowing it"""
        self.text.set_str(self.__data)
        if self.text.get_str_width() + 2 * self.__text_offset_width > self.__width_limit:
            self.__data = self.__data[:-1]
        self.text.set_str(self.__data)

    def __handle_data(self, chr_: str):
        """Formats the potential word by its type specifier"""
        new_data = self.__data + chr_

        if (type_ := type(self.__number_limit)) is float:
            return new_data if float(new_data) <= self.__number_limit else str(self.__number_limit)
        elif type_ is int:
            return new_data if int(new_data) <= self.__number_limit else str(self.__number_limit)
        else:
            return new_data

    def __is_new_data_valid(self, new_data: str):
        """Checks whether the potential word is valid by its type specifier"""
        if (type_ := type(self.__number_limit)) is float:
            return bool(re.match(r'^(?!00)[0-9]*\.?[0-9]{0,4}$', new_data))
        elif type_ is int:
            return bool(re.match(r'^(?!00)[0-9]*$', new_data))
        else:
            return True

    def get_data(self):
        return self.__data

    def set_str(self, str_: str):
        if self.__data != str_:
            self.__data = str_
            self.text.set_str(self.__data)

    def set_color(self, color: pg.Color):
        self.text.set_color(color)

    def set_number_limit(self, number_limit):
        if self.__number_limit != number_limit:
            self.__number_limit = number_limit

    def reset(self):
        """Resets the button to default settings"""
        self.is_clicked = False
        self.rect.set_color(self.colors.button_passive)
        self.__data = self.__initial_str if self.__initial_str else str(self.__number_limit)
        self.text.set_str(self.__data)

    def __repr__(self):
        return f'InputButton({self.text}+{self.emoji} @{self.rect})'
