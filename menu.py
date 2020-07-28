from imports import *


class Menu(object):
    def click(self):
        print("ON!")
    def __init__(self):
        pg.init()

        # Screen init - from game.py
        self.display_width: int = 800
        self.display_height: int = 700
        self.project_name: str = "FDI - Project I - Menu Alfa Version 1.0"
        self.screen = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption(self.project_name)

        self.button = pw.Button(
            self.screen, 250, 600, 300, 80, text='Uruchom symulację', font = pg.font.Font('PatrickHandSC-Regular.ttf',40),
            fontSize=40, margin=15,
            inactiveColour=(255, 255, 255),
            pressedColour=(0,0, 0), radius=5,
            onClick = lambda: (print("Click!"),pg.display.quit(), game.Game(int(self.user_text[0]),int(self.user_text[1]),
                                                                            int(self.user_text[2]),int(self.user_text[3]),
                                                                            float(self.user_text[4])), sys.exit()))
        # Extra - icon init :3
        icon = pg.image.load('particle.png')
        pg.display.set_icon(icon)

        # New menu variables
        # Font
        self.font_header = pg.font.Font('PatrickHandSC-Regular.ttf', 36)
        self.font_basic = pg.font.Font('PatrickHandSC-Regular.ttf', 30)
        self.white = (255, 255, 255)

        # User input (rectangles)
        self.num_of_rect: int = 5
        self.user_text: list = [''] * self.num_of_rect
        # USER ATTRIBUTES (so far...)
        # 1 - R
        # 2 - N
        # 3 - eta_H
        # 4 - eta_L
        # 5 - Vmax

        self.input_rect: list = []
        self.rect_width: int = 100
        self.rect_height: int = 32
        self.color_rect_active = pg.Color('lightskyblue3')                      # Active rect
        self.color_rect_passive = pg.Color('gray15')                            # Passive rect
        self.color_rect: list = [self.color_rect_passive] * self.num_of_rect    # Default color of the rect
        self.active_rect: list = [False] * self.num_of_rect                     # Default - rect not active

        # Temporary solution for available chars in rect
        # Because what if input is (for example): 5.0.0.3...
        self.numbers: list = [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_PERIOD]

        self.init_menu()

    # Drawing strings
    def draw_text(self, text, font, color, x, y):
        txt_object = font.render(text, True, color)
        txt_rect = txt_object.get_rect(center=(x, y))
        self.screen.blit(txt_object, txt_rect)

    # Drawing rectangles for inputs
    def draw_rect(self, x, y, i):
        self.input_rect.append(pg.Rect(x, y, self.rect_width, self.rect_height))
        pg.draw.rect(self.screen, self.color_rect[i], self.input_rect[i])

        # Color - if active or not
        if self.active_rect[i]:
            self.color_rect[i] = self.color_rect_active
        else:
            self.color_rect[i] = self.color_rect_passive

        # Draw text in rect
        text_surface = self.font_basic.render(self.user_text[i], True, self.white)
        self.screen.blit(text_surface, (self.input_rect[i].x + 5, self.input_rect[i].y - 7))

        # Get the width of rect - minimum 100 px
        self.input_rect[i].w = max(100, text_surface.get_width() + 10)

    # Menu initialisation
    def init_menu(self):
        while True:
            self.screen.fill((0, 0, 0))

            # draw_text inits
            self.draw_text('Symulacja cząsteczek gazu doskonałego', self.font_header, self.white, 400, 75)
            self.draw_text('Aby rozpocząć symulację, należy podać następujące atrybuty:', self.font_basic, self.white,
                           400, 150)

            self.draw_text('R (promień atomu): ', self.font_basic, self.white, 300, 250)
            self.draw_text('N (ilość atomów): ', self.font_basic, self.white, 300, 325)
            self.draw_text('ni_H: ', self.font_basic, self.white, 300, 400)
            self.draw_text('ni_L: ', self.font_basic, self.white, 300, 475)
            self.draw_text('V (prędkość maksymalna atomu): ', self.font_basic, self.white, 300, 550)
            self.button.draw()
            # Events
            events = pg.event.get()
            for event in events:
                # Quit events
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                self.button.listen(events)
                # Text input events
                for i in range(self.num_of_rect):
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # If we click on the rect - then ACTIVE
                        if self.input_rect[i].collidepoint(event.pos):
                            self.active_rect[i] = True
                        else:
                            self.active_rect[i] = False

                    # If BACKSPACE - delete last char / Or if NUMBER add into input
                    if event.type == pg.KEYDOWN:
                        if self.active_rect[i]:
                            if event.key == pg.K_BACKSPACE:
                                tmp = self.user_text[i]
                                self.user_text[i] = tmp[:-1]
                            # Add numbers (and period)
                            elif event.key in self.numbers:
                                self.user_text[i] += event.unicode

            # draw_rect inits
            self.draw_rect(500, 234, 0)
            self.draw_rect(500, 309, 1)
            self.draw_rect(500, 384, 2)
            self.draw_rect(500, 459, 3)
            self.draw_rect(500, 534, 4)

            pg.display.update()