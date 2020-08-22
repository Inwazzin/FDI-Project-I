from game_objects.atom_container import AtomContainer
from game_objects.text_object import TextObject
from resources.color_palette import Palette
from game_objects.button import InputButton
from game_objects.atom import Atom, data
from engine import Engine
from imports import *
import matplotlib.backends.backend_agg as agg
import pylab

M = 5000
t = 0

delta_N = []
lam = []
n = []

class Simulation(object):
    """
    Contains all the simulation components
    """
    def __init__(self, R, V, eta_h, eta_l, N):

        # Simulation Variables
        self.is_running: bool = True
        self.is_paused: bool = True
        self.display_plots: bool = False

        self.N: int = int(N)
        self.V: float = float(V)
        self.offset_pos: pg.Vector2 = pg.Vector2(40, 40)
        self.phys: Engine = Engine(int(R), self.V, 0.1, int(eta_h), int(eta_l))  # R, V, d, eta_h, eta_l

        # Game Colors
        self.colors: Palette = Palette()

        # Screen Init
        self.display_width: int = 800
        self.display_height: int = 700
        self.project_name: str = "FDI - Project I"
        self.screen = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption(self.project_name)

        # Init Dummy Game Variables
        self.atoms: List[Atom] = []
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, pg.Color(0, 0, 0))

        # Init Buttons
        self.buttons: Dict[str, InputButton] = {}
        self.__init_buttons()

        self.plots_buttons: Dict[str, InputButton] = {}
        self.__init_plots_buttons()

        # Init Texts
        self.texts: Dict[str, TextObject] = {}
        self.__init_text()

        # Game Init
        pg.init()
        self.__init_simulation_object()
        self.__simulation_loop()

    def __init_text(self):
        """Initializes texts"""
        self.texts['PAUSE'] = TextObject((750, 390), 'Pauza', size=40, color=self.colors.red)

    def __init_buttons(self):
        """Initializes buttons"""
        self.buttons['CHARTS'] = InputButton(pg.Rect(700, 490, 100, 40), roundness=0.4,
                                             font_size=30, font_color=self.colors.neutral, str_='Wykresy')

        self.buttons['PAUSE'] = InputButton(pg.Rect(700, 540, 100, 40), roundness=0.4,
                                            font_size=30, font_color=self.colors.neutral, str_='Start')

        self.buttons['RESTART'] = InputButton(pg.Rect(700, 590, 100, 40), roundness=0.4,
                                              font_size=30, font_color=self.colors.neutral, str_='Restart')

        self.buttons['EXIT'] = InputButton(pg.Rect(700, 640, 100, 40), roundness=0.4,
                                           font_size=30, font_color=self.colors.neutral, str_='Wyjdź')

    def __init_plots_buttons(self):   # przyciski do zmiany wykresów
        self.plots_buttons['1'] = InputButton(pg.Rect(700, 100, 100, 40), roundness=0.4,
                                             font_size=25, font_color=self.colors.neutral, str_='M = 300')

        self.plots_buttons['2'] = InputButton(pg.Rect(700, 150, 100, 40), roundness=0.4,
                                            font_size=25, font_color=self.colors.neutral, str_='M = 500')

        self.plots_buttons['3'] = InputButton(pg.Rect(700, 200, 100, 40), roundness=0.4,
                                              font_size=25, font_color=self.colors.neutral, str_='M = 1000')

        self.plots_buttons['4'] = InputButton(pg.Rect(700, 250, 100, 40), roundness=0.4,
                                           font_size=25, font_color=self.colors.neutral, str_='M = 3000')

        self.plots_buttons['5'] = InputButton(pg.Rect(700, 300, 100, 40), roundness=0.4,
                                        font_size=25, font_color=self.colors.neutral, str_='M = 5000')


    def __init_simulation_object(self):
        """Initializes simulation objects like atoms and containers"""

        N: int = self.N
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, self.colors.neutral)
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)
        print(f"should create {N} atoms")

        spawn_limit_inferior = pg.Vector2(self.atom_container.border_left, self.atom_container.border_up)
        spawn_limit_superior = pg.Vector2(self.atom_container.border_right, self.atom_container.border_down)

        if N > 0:
            x = spawn_limit_inferior.x + self.phys.R
            y = spawn_limit_superior.y - self.phys.R
            v_x = random.random() * self.V
            v_y = -random.random() * self.V

            new_atom = Atom(self.phys.R,
                            self.colors.red,
                            (x, y),
                            (v_x, v_y),
                            self.phys.tolerance)
            new_atom.prev = pg.Vector2(new_atom.pos)
            self.atoms.append(new_atom)
            N -= 1

        while N:
            v_x = random.random() * self.V * (1 if random.randint(0, 1) else -1)
            v_y = random.random() * self.V * (1 if random.randint(0, 1) else -1)
            x = random.randrange(spawn_limit_inferior.x + self.phys.R, spawn_limit_superior.x - self.phys.R)
            y = random.randrange(spawn_limit_inferior.y + self.phys.R, spawn_limit_superior.y - self.phys.R)
            pos = pg.Vector2(x, y)

            if not any(map(
                    lambda a: a.pos.distance_to(pos) <= 2 * self.phys.R * (1 + self.phys.tolerance), self.atoms)):
                new_atom = Atom(self.phys.R,
                                self.colors.blue,
                                (x, y),
                                (v_x, v_y),
                                self.phys.tolerance)
                self.atoms.append(new_atom)
                N -= 1

    def __simulation_loop(self):
        """Simulation loop"""
        while self.is_running:
            self.__handle_events()

            self.__update()
            self.__render()

    def __handle_events(self):
        """Handles simulation event handling"""
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                self.is_running = False
                self.display_plots = False
        self.__handle_buttons(events)

    def __handle_buttons(self, events):
        """Handles button interactions"""

        for button in self.buttons.values():
            button.handle_events(events)

        for button in self.plots_buttons.values():
            button.handle_events(events)

        if self.buttons['CHARTS'].is_clicked:
            self.screen.fill(self.colors.background)
            self.display_plots = True
            self.buttons['CHARTS'].is_clicked = False

            M300 = pg.image.load("M300.png")
            M500 = pg.image.load("M500.png")
            M1000 = pg.image.load("M1000.png")
            M3000 = pg.image.load("M3000.png")
            M5000 = pg.image.load("M5000.png")

            image = M300

            while self.display_plots:
                self.buttons['RESTART'].render(self.screen)
                self.buttons['EXIT'].render(self.screen)
                self.__render_plots_buttons()

                self.screen.blit(image, (0,0))
                self.__handle_events()

                if self.plots_buttons['1'].is_clicked:
                    image = M300
                    self.plots_buttons['1'].is_clicked = False

                if self.plots_buttons['2'].is_clicked:
                    image = M500
                    self.plots_buttons['2'].is_clicked = False

                if self.plots_buttons['3'].is_clicked:
                    image = M1000
                    self.plots_buttons['3'].is_clicked = False

                if self.plots_buttons['4'].is_clicked:
                    image = M3000
                    self.plots_buttons['4'].is_clicked = False

                if self.plots_buttons['5'].is_clicked:
                    image = M5000
                    self.plots_buttons['5'].is_clicked = False

                pg.display.flip()


        if self.buttons['PAUSE'].is_clicked:
            # Laziest workaround you can do lol
            self.is_paused = not self.is_paused
            self.buttons['PAUSE'].set_str('Start' if self.is_paused else 'Stop')
            self.buttons['PAUSE'].is_clicked = False

        if self.buttons['RESTART'].is_clicked:
            data.clear()
            self.is_running = False
            self.display_plots = False

        if self.buttons['EXIT'].is_clicked:
            pg.display.quit()
            exit()


    def __update_collision(self):
        """Updates Collision between simulation objects"""
        for atom in self.atoms:
            atom.update_collision_wall(self.atom_container)

        a1: Atom
        a2: Atom
        for (a1, a2) in it.combinations(self.atoms, r=2):
            a1.update_collision_atom(a2)

    def __update(self):
        """Handles simulation value updates"""
        # Time Update
        self.phys.update_time()

        ############################################################
        ############################################################
        '''
        global M, t
        if M == 0:
            if data:
                delta_N.append(len(data))
                lam.append(sum(data) / len(data))
            else:
                delta_N.append(0)
                lam.append(0)
            n.append(len(data) / t)
            data.clear()
            t, M = 0, 5000
            self.is_running = False
        else:
            t += self.phys.dt_coefficient
            M -= 1

        if len(n) == 10:
            print(lam)
            print(n)
            print(delta_N)
        '''
        ############################################################
        ############################################################

        # Collision Update
        if not self.is_paused:
            self.__update_collision()
            self.__update_atoms()

    def __update_atoms(self):
        """Updates Atom values"""
        for atom in self.atoms:
            atom.update(self.phys.discrete_dt)

    def __render(self):
        """Handles simulation rendering"""
        self.screen.fill(self.colors.background)

        self.__render_atoms()
        self.__render_texts()
        self.__render_buttons()
        self.atom_container.render(self.screen)

        pg.display.flip()

    def __render_atoms(self):
        """Renders Atoms"""
        for atom in self.atoms:
            atom.render(self.screen)

    def __render_buttons(self):
        """Renders Buttons"""
        for button in self.buttons.values():
            button.render(self.screen)

    def __render_plots_buttons(self):
        for button in self.plots_buttons.values():
            button.render(self.screen)

    def __render_texts(self):
        """Renders Texts"""
        for text in self.texts.values():
            if text is self.texts['PAUSE']:
                if self.is_paused:
                    text.render(self.screen)
            else:
                text.render(self.screen)