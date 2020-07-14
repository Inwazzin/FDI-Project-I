from imports import *
from game_objects.atom_container import *
from engine import *


class Atom(object):
    def __init__(self,
                 radius: int = 50,
                 color: pg.Color = pg.Color(255, 255, 255, 255),
                 pos: Tuple[float, float] = (0.0, 0.0),
                 velocity: Tuple[float, float] = (2.0, 2.0),
                 local_angle: int = 0,
                 tolerance: float = -1,
                 mass: int = 1):

        # Colors
        self.color: pg.Color = color
        self.current_color: pg.Color = self.color

        # Scalars
        self.radius: float = radius
        self.mass: int = mass
        self.local_angle: float = local_angle
        self.tolerance: float = self.radius / 10 if tolerance == -1 else tolerance * self.radius
        print("Debug Create Atom:", radius, color, pos, velocity, local_angle, mass, self.tolerance)

        # Vectors
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.velocity: pg.Vector2 = pg.Vector2(velocity)

    def update(self, global_angle, dt):
        pass

    def update_movement(self, dt: float):
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    # update_collision_velocities
    # tutaj chyba nie trzeba tlumaczyc za wiele
    def update_collision_atom(self, other):
        if self.__is_collision_atom(other):
            print('!!!COLLISION!!!')
            vector: pg.Vector2 = self.__find_collision_pos_vector(other)
            cos1: float = self.__get_cosine(vector)  # cos dla self
            cos2: float = other.__get_cosine(vector)  # cos dla other
            print(cos1, cos2)

            # Obliczenia
            self_vel_y: pg.Vector2 = self.velocity * cos1
            self_vel_x: pg.Vector2 = self.velocity * mh.sqrt(1 - cos1 ** 2)
            other_vel_y: pg.Vector2 = other.velocity * cos2
            other_vel_x: pg.Vector2 = other.velocity * mh.sqrt(1 - cos2 ** 2)
            # Podstawienie Wyników
            self.velocity: pg.Vector2 = self_vel_y + other_vel_x
            other.velocity = other_vel_y + self_vel_x
            # update

    # wariant - znak wielka litera, czy od North, South, etc...
    def update_collision_wall(self, container):
        type_: chr
        for wall in list(self.__find_collision_walls(container)):
            if wall in 'NS':
                self.velocity.y *= -1
            elif wall in 'WE':
                self.velocity.x *= -1

    # ZDERZENIA
    # dla pary kulek sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def __is_collision_atom(self, other):
        return self.pos.distance_to(other.pos) <= 2 * self.radius + self.tolerance
        # return 2 * self.radius < self.pos.distance_to(other.pos) <= 2 * self.radius + self.tolerance

    # dla pary kulka, kontener sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def __find_collision_walls(self, container: AtomContainer) -> str:
        if self.pos.x + self.radius > container.border_right:
            yield 'E'
        elif self.pos.x - self.radius < container.border_left:
            yield 'W'

        if self.pos.y + self.radius > container.border_down:
            yield 'S'
        elif self.pos.y - self.radius < container.border_up:
            yield 'N'

    # a ja bede biadloc po polsku - Maciek
    # dwie kulki - zwraca wektor miedzy nimi
    def __find_collision_pos_vector(self, other) -> pg.Vector2:
        return other.pos - self.pos

    # kulka i wektor miedzy kulkami -> kat miedzy predkoscia a wektorem
    def __get_cosine(self, other: pg.Vector2) -> float:
        return self.velocity.dot(other) / (self.velocity.length() * other.length())

    def render(self, screen: pg.Surface):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.current_color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.current_color)
