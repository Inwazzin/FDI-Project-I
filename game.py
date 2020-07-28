from game_objects.atom_container import AtomContainer
from game_objects.atom import Atom
from engine import Engine
from imports import *

class Game(object):
    def __init__(self, R,N,  eta_h, eta_l, V):
        # Simulation Variables
        self.N = N
        self.V = V
        self.is_running: bool = True
        self.phys: Engine = Engine(R, V, 0.1, eta_h, eta_l)  # R, V, d, eta_h, eta_l
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
        #button

        self.button = pw.Button(
            self.screen, 595, 655, 200, 40, text='Zakończ symulację',
            font=pg.font.Font('PatrickHandSC-Regular.ttf', 20),
            textColour = (255,255,255),
            fontSize=20, margin=15,
            inactiveColour=(238, 32, 77),
            pressedColour=(0, 0, 0), radius=5,
            onClick=lambda: (
            print("Click!"), pg.display.quit(), sys.exit())) #Tutaj trzeba dodać obsługę wyświetlenia okna z wykonanymi pomiarami

        # Game Init

        pg.init()
        self.__init_game_object()
        self.phys.update_time()

        self.__game_loop()

    def __init_game_object(self):
        N = self.N
        self.atom_container: AtomContainer = AtomContainer(self.offset_pos, self.color_neutral)
        self.atom_container.update(self.phys.eta_h, self.phys.eta_l, self.phys.R)
        print(f"should create {N} atoms")

        # Should create N = (eta_l*eta_h)/4 atoms inside the container boundaries
        # For now it is makeshift


        spawn_limit_inferior = pg.Vector2(self.offset_pos.x + self.phys.R, self.offset_pos.y + self.phys.R)
        spawn_limit_superior = pg.Vector2(self.atom_container.border_down - self.phys.R, self.atom_container.border_right - self.phys.R)
        x = spawn_limit_inferior.x + self.phys.R
        y = spawn_limit_inferior.y + self.phys.R
        for i in range(N):
            v_x = random.random() * self.V
            v_y = random.random() * self.V
            x += self.phys.R * 2.25
            if x + 1.1*self.phys.R >= spawn_limit_superior.x:
                x = spawn_limit_inferior.x + self.phys.R
                y += self.phys.R * 2.25
            new_atom = Atom(self.phys.R,
                        self.color_blue,
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
            self.button.listen(events)
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
        self.button.draw()
        for atom in self.atoms:
            atom.render(self.screen)

        self.atom_container.render(self.screen)
        pg.display.update()
