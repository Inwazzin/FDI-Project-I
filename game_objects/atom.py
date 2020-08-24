from imports import *
from game_objects.atom_container import *
from engine import *

data = []
l = 0

def distance(atom: 'Atom'):
    global l
    l += math.sqrt(pow((atom.pos.x - atom.prev.x), 2) + pow((atom.pos.y - atom.prev.y), 2))
    atom.prev.x, atom.prev.y = atom.pos.x, atom.pos.y
    return l


class Atom(object):
    def __init__(self,
                 radius: int = 50,
                 color: pg.Color = pg.Color(255, 255, 255, 255),
                 pos: Tuple[float, float] = (0.0, 0.0),
                 velocity: Tuple[float, float] = (2.0, 2.0),
                 tolerance: float = 0.1,
                 mass: int = 1):

        # Shape
        self.shape: pg.Surface = pg.Surface((0, 0))

        # Colors
        self.color: pg.Color = color
        self.current_color: pg.Color = self.color

        # Scalars
        self.radius: float = radius
        self.mass: int = mass
        self.tolerance: float = tolerance

        print(self.tolerance)

        # Timers
        self.__collision_timer: float = 0

        # self.__max_collision_time_atom: float = 0
        # self.__collision_time_atom: float = 0.17
        # self.__max_collision_time_wall: float = 0.17
        # self.__collision_time_wall: float = 0.17

        # Vectors
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.velocity: pg.Vector2 = pg.Vector2(velocity)
        self.init_shape()

        # pozycja atomu przy ostatnim zderzeniu
        self.prev = pg.Vector2((0.0, 0.0))

        print("Debug Create Atom:", radius, color, pos, velocity, mass, self.tolerance)

    def update(self, dt: float):
        # self.__update_collision_timer(dt)
        self.__update_movement(dt)

    def __update_movement(self, dt: float):
        self.pos += self.velocity * dt

    def update_collision_atom(self, other: 'Atom'):
        global l, t
        if self.__is_collision_atom(other):
            if self.color == (205, 126, 25, 255):
                data.append(distance(self))
                l = 0
            # From Wikipedia Free Encyclopedia

            print('!!!COLLISION!!!')
            print(self.velocity, other.velocity)
            self.velocity, other.velocity = self.__find_new_velocity(other), other.__find_new_velocity(self)

            pos_dif = self.pos - other.pos
            angle = math.atan2(pos_dif.y, pos_dif.x) + 0.5 * math.pi

            overlap = 0.5 * (2 * self.radius * (1 + self.tolerance) - self.pos.distance_to(other.pos) + 1)

            self.pos.x += math.sin(angle) * overlap
            self.pos.y -= math.cos(angle) * overlap
            other.pos.x -= math.sin(angle) * overlap
            other.pos.y += math.cos(angle) * overlap

            print(overlap, self.velocity, other.velocity)

    # dla pary kulka, kontener sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    # wariant - znak wielka litera, czy od North, South, etc...
    def update_collision_wall(self, container):
        global l
        walls = list(self.__find_collision_walls(container))
        for wall in walls:
            if self.color == (205, 126, 25, 255):
                l += distance(self)
            if wall == 'N':
                self.velocity.y *= -1
                self.pos.y += self.radius / 8
            elif wall == 'S':
                self.velocity.y *= -1
                self.pos.y -= self.radius / 8
            elif wall == 'W':
                self.velocity.x *= -1
                self.pos.x += self.radius / 8
            elif wall == 'E':
                self.velocity.x *= -1
                self.pos.x -= self.radius / 8

    def __is_collision_atom(self, other):
        return self.pos.distance_to(other.pos) <= (2 + self.tolerance) * self.radius
        # return 2 * self.radius < self.pos.distance_to(other.pos) <= 2 * self.radius + self.tolerance

    def __find_new_velocity(self, other: 'Atom') -> pg.Vector2:
        # v1' = v1 - (((2*m2) / (m1+m2)) * ((<v1-v2, x1-x2>) / (||x1-x2||^2)) * (x1 - x2))
        pos_diff: pg.Vector2 = self.pos - other.pos
        return self.velocity - (self.velocity - other.velocity).dot(pos_diff) / pos_diff.length_squared() * pos_diff
        # This one has mass
        # return (self.velocity
        #         - (((2 * self.mass) / (self.mass + other.mass))
        #            * (((self.velocity - other.velocity).dot(pos_diff)) / pos_diff.length_squared())
        #            * pos_diff))

    def __find_collision_walls(self, container: AtomContainer) -> str:
        if self.pos.x + self.radius > container.border_right:
            yield 'E'
        elif self.pos.x - self.radius < container.border_left:
            yield 'W'

        if self.pos.y + self.radius > container.border_down:
            yield 'S'
        elif self.pos.y - self.radius < container.border_up:
            yield 'N'

    def render(self, screen: pg.Surface):
        screen.blit(self.shape, (self.pos.x - self.radius, self.pos.y - self.radius))

    def init_shape(self):
        circle = pg.Surface([self.radius * 30] * 2, pg.SRCALPHA)
        pg.draw.ellipse(circle, self.color, circle.get_rect(), 0)
        self.shape = pg.transform.smoothscale(circle, [self.radius * 2] * 2)
