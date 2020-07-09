from imports import *

class Atom(object):
    def __init__(self,
                 radius: int = 50,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 pos: Tuple[float, float] = (0.0, 0.0),
                 velocity: Tuple[float, float] = (0.0, 0.0),
                 local_angle: int = 0,
                 mass: int = 1):
        print("Debug Create Atom:", radius, color, pos, velocity, local_angle, mass)

        self.color: pg.Color = pg.Color(*color)

        # Scalars
        self.radius: float = radius
        self.mass: int = mass
        self.local_angle: float = local_angle

        # Vectors
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.velocity: pg.Vector2 = pg.Vector2(velocity)

    def update(self, global_angle):
        # Maciej(metody) i Ania(czas)
        pass

    def render(self, screen: pg.Surface):
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)
        gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.color)
