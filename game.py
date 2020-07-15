from game_objects.atom_container import AtomContainer
from game_objects.atom import Atom
from engine import Engine
from imports import *

class Game(object):
    def __init__(self):
        # Simulation Variables
        self.is_running: bool = True
        self.phys: Engine = Engine(30, 2.0, 0.1, 20, 20)  # R, V, d, eta_h, eta_l
        self.offset_pos: pg.Vector2 = pg.Vector2(40, 40)

        # Game Colors
        self.color_blue: pg.Color = pg.Color(25, 126, 205)
        self.color_red: pg.Color = pg.Color(205, 126, 25)
        self.color_neutral: pg.Color = pg.Color(207, 207, 196)
        self.color_background: pg.Color = pg.Color(41, 41, 37)

        # Screen Init
        self.display_width: int = 800
        self.display_height: int = 700
        self.project_name: str = "FDI - Project I"
        self.screen = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption(self.project_name)

        # Init Dummy Game Variables
        self.atoms: List[Atom] = []
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, pg.Color(0, 0, 0))
        # Game Init

        pg.init()
        self.__init_game_object()
        self.phys.update_time()

        self.__game_loop()

    def __init_game_object(self):
        N: int = int((self.phys.eta_l*self.phys.eta_h)/4)
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, self.color_neutral)
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)
        print(f"should create {N} atoms")
        while N:
            N -= 1

        # Should create N = (eta_l*eta_h)/4 atoms inside the container boundaries
        # For now it is makeshift

        # Test Atom-Wall Collision
        # new_atom = Atom(self.phys.R, self.color_red, (50, 50), (20, 20), 0, 1)
        # self.atoms.append(new_atom)

        # # Test Atom-Atom Collision Random
        # new_atom = Atom(self.phys.R, self.color_blue, (150, 150), (-20, -15), 0, self.phys.tolerance)
        # self.atoms.append(new_atom)
        # new_atom = Atom(self.phys.R, self.color_neutral, (420, 220), (20, 0), 0, self.phys.tolerance)
        # self.atoms.append(new_atom)

        # Test Atom-Atom Collision X-Axis
        #  new_atom = Atom(self.phys.R, self.color_blue, (80, 240), (-20, 0), 0, self.phys.tolerance)
        #  self.atoms.append(new_atom)
        #  new_atom = Atom(self.phys.R, self.color_neutral, (420, 220), (20, 0), 0, self.phys.tolerance)
        #  self.atoms.append(new_atom)
        spawn_limit_inferior = pg.Vector2(self.offset_pos.x + self.phys.R, self.offset_pos.y + self.phys.R)
        spawn_limit_superior = \
            spawn_limit_inferior \
            + pg.Vector2(self.atom_container.border_down - self.phys.R, self.atom_container.border_right - self.phys.R)
        print(spawn_limit_superior, spawn_limit_inferior)
        # # Test Atom-Atom Collision Y-Axis
        new_atom = Atom(self.phys.R,
                        self.color_blue,
                        (40+self.phys.R, 40+self.phys.R),
                        (3, 3),
                        0,
                        self.phys.tolerance)
        self.atoms.append(new_atom)

        # new_atom = Atom(self.phys.R,
        #                 self.color_neutral,
        #                 (640-self.phys.R, 640-self.phys.R),
        #                 (-3, -3),
        #                 0,
        #                 self.phys.tolerance)
        # self.atoms.append(new_atom)

        # # Test Atom-Atom Collision Y-Axis
        # new_atom = Atom(self.phys.R,
        #                 self.color_blue,
        #                 (640-self.phys.R, 40+self.phys.R),
        #                 (-3, 3),
        #                 0,
        #                 self.phys.tolerance)
        # self.atoms.append(new_atom)

        new_atom = Atom(self.phys.R,
                        self.color_neutral,
                        (40+self.phys.R, 640-self.phys.R),
                        (3, -3),
                        0,
                        self.phys.tolerance)
        self.atoms.append(new_atom)

    def __game_loop(self):
        while self.is_running:
            self.__handle_events()

            self.__update()
            self.__render()

    def __handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

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

        # Debug Prints
        # print("Discrete time: ", self.phys.dt, self.phys.discrete_dt)
        # print(self.atom_container.border_up,
        #      self.atom_container.border_down,
        #      self.atom_container.border_left,
        #      self.atom_container.border_right)
        # print(self.atom_container.H)

        # Collision Update
        self.__update_collision()
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)

        for atom in self.atoms:
            atom.update(self.phys.discrete_dt)
            atom.update_movement(self.phys.discrete_dt)

    def __render(self):
        self.screen.fill(self.color_background)
        for atom in self.atoms:
            atom.render(self.screen)

        self.atom_container.render(self.screen)
        pg.display.update()
