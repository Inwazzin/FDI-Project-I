from game_objects.atom_container import AtomContainer
from game_objects.atom import Atom
from resources.color_palette import Palette
from game_objects.button import InputButton
from engine import Engine
from imports import *
from menu import Menu


class Game(object):
    def __init__(self, R, V, eta_h, eta_l, N):
        # Simulation Variables
        self.N: int = int(N)
        self.V: float = float(V)
        self.is_running: bool = True
        self.phys: Engine = Engine(int(R), self.V, 0.1, int(eta_h), int(eta_l))  # R, V, d, eta_h, eta_l
        self.offset_pos: pg.Vector2 = pg.Vector2(40, 40)

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

        # Game Init
        pg.init()
        self.__init_game_object()
        self.phys.update_time()
        self.__game_loop()

    def __init_buttons(self):
        self.buttons['CHARTS'] = InputButton(pg.Rect(700, 540, 100, 40), roundness=0.4,
                                             font_size=30, font_color=self.colors.neutral, str_='Wykresy')

        self.buttons['RESTART'] = InputButton(pg.Rect(700, 590, 100, 40), roundness=0.4,
                                              font_size=30, font_color=self.colors.neutral, str_='Restart')

        self.buttons['EXIT'] = InputButton(pg.Rect(700, 640, 100, 40), roundness=0.4,
                                           font_size=30, font_color=self.colors.neutral, str_='Wyjdź')

    def __init_game_object(self):
        N: int = int(self.phys.eta_l / 4)
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, self.colors.neutral)
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)
        print(f"should create {N} atoms")

        # Should create N = min(eta_l,eta_h)/4 atoms inside the container boundaries
        # For now it is makeshift

        spawn_limit_inferior = pg.Vector2(self.offset_pos.x + self.phys.R, self.offset_pos.y + self.phys.R)
        spawn_limit_superior = pg.Vector2(self.atom_container.border_down - self.phys.R,
                                          self.atom_container.border_right - self.phys.R)
        x = spawn_limit_inferior.x + self.phys.R
        y = spawn_limit_inferior.y + self.phys.R
        for i in range(N):
            v_x = random.random() * self.V
            v_y = random.random() * self.V
            x += self.phys.R * 2.25
            if x + 1.1 * self.phys.R >= spawn_limit_superior.x:
                x = spawn_limit_inferior.x + self.phys.R
                y += self.phys.R * 2.25
            new_atom = Atom(self.phys.R,
                            self.colors.blue,
                            (x, y),
                            (v_x, v_y),
                            0,
                            self.phys.tolerance)
            self.atoms.append(new_atom)

    def __game_loop(self):
        while self.is_running:
            self.__handle_events()

            self.__update()
            self.__render()

    def __handle_events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
                self.is_running = False

        for button in self.buttons.values():
            button.handle_events(events)

        if self.buttons['EXIT'].is_clicked:
            pg.display.quit()

        if self.buttons['RESTART'].is_clicked:
            pg.display.quit()
            Menu()

    def __update_collision(self):
        atom: Atom
        for atom in self.atoms:
            atom.update_collision_wall(self.atom_container)

        a1: Atom
        a2: Atom
        for (a1, a2) in it.combinations(self.atoms, r=2):
            a1.update_collision_atom(a2)

    def __update(self):
        # Time Update
        self.phys.update_time()

        # Collision Update
        self.__update_collision()
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)

        for atom in self.atoms:
            atom.update(self.phys.discrete_dt)
            atom.update_movement(self.phys.discrete_dt)

    def __render(self):
        self.screen.fill(self.colors.background)

        for atom in self.atoms:
            atom.render(self.screen)

        for button in self.buttons.values():
            button.render(self.screen)
        self.atom_container.render(self.screen)
        pg.display.update()
