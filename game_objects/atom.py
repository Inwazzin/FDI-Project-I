from imports import *
from game_objects.atom_container import *
from engine import *

class Atom(object):
    def __init__(self,
                 radius: int = 50,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 pos: Tuple[float, float] = (0.0, 0.0),
                 velocity: Tuple[float, float] = (0.0, 0.0),
                 local_angle: int = 0,
                 tolerance: float = -1,
                 mass: int = 1):
        print("Debug Create Atom:", radius, color, pos, velocity, local_angle, mass)

        self.color: pg.Color = pg.Color(*color)

        # Scalars
        self.radius: float = radius
        self.mass: int = mass
        self.local_angle: float = local_angle
        self.tolerance: float = self.radius/10 if tolerance == -1 else tolerance

        # Vectors
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.velocity: pg.Vector2 = pg.Vector2(velocity)

    def update(self, global_angle, dt):

        # Maciej(metody) i Ania(czas)
        pass

    # a ja bede biadloc po polsku - Maciek
    def get_collision_vector(self, other: pg.Vector2) -> pg.Vector2:  # dwie kulki - zwraca wektor miedzy nimi
        return pg.Vector2(other.pos.x - self.pos.x, other.pos.y - self.pos.y)

    def get_cosine(self, vector: pg.Vector2) -> float:  # kulka i wektor miedzy kulkami -> kat miedzy predkoscia a wektorem
        return (vector.x
                * self.velocity.x
                + vector.y
                * self.velocity.y) / (
                       mh.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)
                       + mh.sqrt(vector.x ** 2 + vector.y ** 2))

    # update_collision_velocities
    def update_collision_atom_velocities(self, other):  # tutaj chyba nie trzeba tlumaczyc za wiele
        vector: pg.Vector2 = self.get_collision_vector(other)
        cos1: float = self.get_cosine(vector)  # cos dla self
        cos2: float = other.get_cosine(vector)  # cos dla other

        # Obliczenia
        self_vel_y: pg.Vector2 = self.velocity * cos1
        self_vel_x: pg.Vector2 = self.velocity * mh.sqrt(1 - cos1 ** 2)
        other_vel_y: pg.Vector2 = other.velocity * cos2
        other_vel_x: pg.Vector2 = other.velocity * mh.sqrt(1 - cos2 ** 2)

        # Podstawienie Wyników
        self.velocity: pg.Vector2 = self_vel_y + other_vel_x
        other.velocity = other_vel_y + self_vel_x
        # update

    def update_collision_wall_velocities(self, collision_type: str):  # wariant - znak wielka litera, czy od North, South, etc...
        if collision_type in 'NS':
            self.velocity.y *= -1
        elif collision_type in 'WE':
            self.velocity.x *= -1
        else:
            raise Exception(f"ERROR::ATOM::NEW_VELOCITY Wrong Collision Type {collision_type} instead of NSWE")

    def render(self, screen: pg.Surface):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)

    #ZDERZENIA
    # dla pary kulek sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def is_collision_atom(self, other):
        return 2 * self.radius < self.get_collision_vector(other) <= 2 * self.radius + self.tolerance

    # dla pary kulka, kontener sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def check_collision_wall(self, container: AtomContainer) -> Tuple[bool, str]:
        if self.pos.x + self.radius - self.tolerance >= container.border_right:
            return True, 'E'
        elif self.pos.x - self.radius + self.tolerance <= container.border_left:
            return True, 'W'
        elif self.pos.y + self.radius - self.tolerance >= container.border_down:
            return True, 'S'
        elif self.pos.y - self.radius + self.tolerance <= container.border_up:
            return True, 'N'
        return False, ''
