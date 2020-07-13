from game_objects.atom_container import AtomContainer
from game_objects.atom import Atom
from engine import Engine
from imports import *

class Game(object):
    def __init__(self):
        # Engine Variables
        self.is_running: bool = True
        self.phys = Engine(12, 2.0, 0.001, 50, 50)    # R, V, d, eta_h, eta_l

        # Game Colors
        # Tutaj są tuple zamiast pg.Color z powodu ograniczeń silnika
        self.color_blue = (25, 126, 205)
        self.color_red = (205, 126, 25)
        self.color_neutral = (207, 207, 196)
        self.color_background = (41, 41, 37)

        # Screen Init
        self.display_width: int = 800
        self.display_height: int = 700
        self.project_name: str = "FDI - Project I"
        pg.display.set_caption(self.project_name)
        self.screen = pg.display.set_mode((self.display_width, self.display_height))

        # Init Dummy Game Variables
        self.atoms: List[Atom] = []
        self.atom_container: AtomContainer = AtomContainer((0, 0), (0, 0, 0))
        # Game Init
        pg.init()
        self.init_game_object()
        self.game_loop()

    def init_game_object(self):
        # Should create N = (eta_l*eta_h)/4 atoms inside the container boundaries
        # For now it is makeshift
        new_atom = Atom(self.phys.R, self.color_blue, (100, 100), (20, 20), 0, 1)
        self.atoms.append(new_atom)
        new_atom = Atom(self.phys.R, self.color_red, (200, 100), (20, 20), 0, 1)
        self.atoms.append(new_atom)
        new_atom = Atom(self.phys.R, self.color_neutral, (300, 100), (5, 7), 0, 1)
        self.atoms.append(new_atom)
        self.atom_container = AtomContainer((30, 30), self.color_neutral)

    def game_loop(self):
        while self.is_running:
            self.__handle_events()

            self.__update()
            self.__render()

    def __handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

    def __update(self):
        # Update czasu
        self.phys.update_dt()
        self.phys.update_time()
        print("Discrete time: ", self.phys.dt, self.phys.discrete_dt)

        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)
        for atom in self.atoms:
            #  atom.update(self.phys.global_angle, self.phys.dt)
            atom.update_movement(self.phys.discrete_dt)

        self.__update_collision()

    def __update_collision(self):
        for i in range(len(self.atoms)):
            self.atoms[i].update_collision(self.atoms[:i]+self.atoms[i+1:], self.atom_container)

    def __render(self):
        self.screen.fill(self.color_background)
        for atom in self.atoms:
            atom.render(self.screen)

        self.atom_container.render(self.screen)
        pg.display.update()
