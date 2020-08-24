from game_objects.text_object import TextObject
from game_objects.button import InputButton
from resources.color_palette import Palette
from simulation import Simulation
from imports import *

# Limity można se zmieniać w imię wygody lel‍
LIMIT_R = 15
LIMIT_V = 50.0
LIMIT_ETA_L = 40
LIMIT_ETA_H = 40
LIMIT_N = (LIMIT_ETA_L*LIMIT_ETA_H)//16

class Menu(object):
    def __init__(self):
        pg.init()
        # Screen init - from game.py
        self.is_running: bool = True

        # Screen Init
        self.display_width: int = 800
        self.display_height: int = 700
        self.project_name: str = "FDI - Project I - Menu Alfa Version 1.0"
        self.screen = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption(self.project_name)
        icon = pg.image.load('particle.png')
        pg.display.set_icon(icon)

        # Menu Variables
        self.font_header_height: int = 36
        self.font_normal_height: int = 30
        self.colors: Palette = Palette()

        self.__N_limit: int = 0
        self.texts: Dict[str, TextObject] = {}
        self.input_buttons: Dict[str, InputButton] = {}
        self.buttons: Dict[str, InputButton] = {}
        self.numbers: Tuple[int, ...] = (pg.K_0, pg.K_1, pg.K_2,
                                         pg.K_3, pg.K_4, pg.K_5,
                                         pg.K_6, pg.K_7, pg.K_8,
                                         pg.K_9, pg.K_PERIOD,
                                         pg.K_KP0, pg.K_KP1, pg.K_KP2,
                                         pg.K_KP3, pg.K_KP4, pg.K_KP5,
                                         pg.K_KP6, pg.K_KP7, pg.K_KP8,
                                         pg.K_KP9, pg.K_KP_PERIOD)

        self.__init_texts()
        self.__init_buttons()
        self.__main_loop()

    def __init_texts(self):
        self.texts['WARNING_TEXT'] = TextObject((400, 60),
                                                'Wymiary Zbiornika:',
                                                size=self.font_normal_height,
                                                color=self.colors.neutral)

        self.texts['WARNING_SIZE'] = TextObject((400, 100),
                                                f'{LIMIT_ETA_H * LIMIT_R} x {LIMIT_ETA_H * LIMIT_R}',
                                                size=self.font_normal_height,
                                                color=self.colors.neutral)

        self.texts['MENU_HEADER'] = TextObject((400, 20),
                                               'Symulacja cząsteczek gazu doskonałego',
                                               size=self.font_header_height,
                                               style=freetype.STYLE_STRONG,
                                               color=self.colors.neutral)

        self.texts['MENU_SUBSCRIPT'] = TextObject((400, 150),
                                                  'Aby rozpocząć symulację, należy podać następujące atrybuty:',
                                                  size=self.font_normal_height,
                                                  color=self.colors.neutral)

        self.texts['MENU_R'] = TextObject((300, 250),
                                          'R (promień atomu):',
                                          size=self.font_normal_height,
                                          color=self.colors.neutral)

        self.texts['MENU_V'] = TextObject((300, 325),
                                          'V (prędkość maksymalna atomu):',
                                          size=self.font_normal_height,
                                          color=self.colors.neutral)

        self.texts['MENU_N'] = TextObject((300, 550),
                                          'N (ilość atomów):',
                                          size=self.font_normal_height,
                                          color=self.colors.neutral)

        self.texts['MENU_ETA_H'] = TextObject((300, 400),
                                              u'ηH (wsp. wielkości):',
                                              size=self.font_normal_height,
                                              color=self.colors.neutral)

        self.texts['MENU_ETA_L'] = TextObject((300, 475),
                                              u'ηL (wsp. szerokości):',
                                              size=self.font_normal_height,
                                              color=self.colors.neutral)

    def __init_buttons(self):
        self.buttons['START'] = InputButton(pg.Rect(250, 600, 300, 80), roundness=0.4,
                                            font_size=40, font_color=self.colors.neutral, str_='Uruchom Symulację')

        self.buttons['EXIT'] = InputButton(pg.Rect(580, 600, 100, 80), roundness=0.4,
                                           font_size=40, font_color=self.colors.neutral, str_='Wyjdź')

        # R V H L N 24 10.0 100 100 0
        self.input_buttons['DATA_R'] = InputButton(pg.Rect(500, 225, 200, 50), self.colors.neutral,
                                                   self.font_normal_height, 0, self.numbers, LIMIT_R, 0.4)
        self.input_buttons['DATA_V'] = InputButton(pg.Rect(500, 300, 200, 50), self.colors.neutral,
                                                   self.font_normal_height, 0, self.numbers, LIMIT_V, 0.4)
        self.input_buttons['DATA_ETA_H'] = InputButton(pg.Rect(500, 375, 200, 50), self.colors.neutral,
                                                       self.font_normal_height, 0, self.numbers, LIMIT_ETA_H, 0.4)
        self.input_buttons['DATA_ETA_L'] = InputButton(pg.Rect(500, 450, 200, 50), self.colors.neutral,
                                                       self.font_normal_height, 0, self.numbers, LIMIT_ETA_L, 0.4)
        self.input_buttons['DATA_N'] = InputButton(pg.Rect(500, 525, 200, 50), self.colors.neutral,
                                                   self.font_normal_height, 0, self.numbers, LIMIT_N, 0.4)

    def __main_loop(self):
        while self.is_running:
            self.update()
            self.handle_events()
            self.render()

    def update(self):
        self.__update_atom_container_size()
        self.__update_n_limit()

    def __update_atom_container_size(self):
        radius = self.input_buttons['DATA_R'].get_data()
        eta_h = self.input_buttons['DATA_ETA_H'].get_data()
        eta_l = self.input_buttons['DATA_ETA_L'].get_data()

        if radius and eta_l and eta_h:
            size_x = int(radius) * int(eta_l)
            size_y = int(radius) * int(eta_h)
            if size_x > self.display_width or size_y > self.display_height:
                self.texts['WARNING_TEXT'].set_color(self.colors.red)
                self.texts['WARNING_SIZE'].set_color(self.colors.red)
                self.texts['WARNING_TEXT'].set_style(freetype.STYLE_STRONG)
                self.texts['WARNING_SIZE'].set_style(freetype.STYLE_STRONG)
            else:
                self.texts['WARNING_TEXT'].set_color(self.colors.neutral)
                self.texts['WARNING_SIZE'].set_color(self.colors.neutral)
                self.texts['WARNING_TEXT'].set_style(freetype.STYLE_DEFAULT)
                self.texts['WARNING_SIZE'].set_style(freetype.STYLE_DEFAULT)
        else:
            size_x = 0
            size_y = 0
        self.texts['WARNING_SIZE'].set_str(f'{size_x} x {size_y}')

    def __update_n_limit(self):
        eta_h = self.input_buttons['DATA_ETA_H'].get_data()
        eta_l = self.input_buttons['DATA_ETA_L'].get_data()
        self.__N_limit = int(eta_h) * int(eta_l)//16 if eta_h and eta_l else 0

        self.input_buttons['DATA_N'].set_number_limit(self.__N_limit)

        if (n := self.input_buttons['DATA_N'].get_data()) and int(n) > self.__N_limit:
            self.input_buttons['DATA_N'].set_str(str(self.__N_limit))

    def handle_events(self):
        events = pg.event.get()
        self.__handle_buttons(events)
        for event in events:
            # Quit events
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                self.is_running = False

        if self.buttons['EXIT'].is_clicked:
            pg.display.quit()
            exit()

        if self.buttons['START'].is_clicked:
            Simulation(*self.__get_data_from_inputs())
            self.__reset()

    def __handle_buttons(self, events):
        for button in self.input_buttons.values():
            button.handle_events(events)
        for button in self.buttons.values():
            button.handle_events(events)

    def render(self):
        self.screen.fill(self.colors.background)
        self.__render_texts(self.screen)
        self.__render_buttons(self.screen)

        pg.display.flip()

    def __render_texts(self, screen: pg.Surface):
        for text in self.texts.values():
            text.render(screen)

    def __render_buttons(self, screen: pg.Surface):
        for button in self.input_buttons.values():
            button.render(screen)
        for button in self.buttons.values():
            button.render(screen)

    def __get_data_from_inputs(self):
        return [button.get_data() for button in self.input_buttons.values()]

    def __reset(self):
        for button in self.buttons.values():
            button.reset()

        for button in self.input_buttons.values():
            button.reset()
