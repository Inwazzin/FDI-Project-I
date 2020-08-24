from imports import *

class AtomContainer(object):
    def __init__(self,
                 offset: pg.Vector2,
                 color: pg.Color):
        #print("Debug Create Container:", offset, color)
        # Init Private Const Container Variables
        self.__color = color

        # Private Const Width of the wall
        self.__width: int = 10
        self.__offset_initial = offset - pg.Vector2(self.__width, self.__width)
        # offset from the border of the screen

        # Init Dummy Public Variables
        self.H: int = 0                     # Height Inside the container
        self.L: int = 0                     # Useless Width Inside the container

        self.x: int = 0
        self.y: int = 0
        self.border_up: int = 0             # Upper border
        self.border_down: int = 0           # Lower border
        self.border_left: int = 0           # Left border
        self.border_right: int = 0          # Right border

        # Init Dummy Private Container Walls
        self.__height: int = 0              # Private Height of the wall
        self.__walls: list = []             # Wall list

    def __update_borders(self, eta_h, radius):
        self.H: int = int(eta_h*radius)
        self.L: int = self.H

        self.__height: int = self.H+self.__width
        self.border_up: int = self.__offset_initial.y + self.__width
        self.border_down: int = self.__offset_initial.y + self.__height
        self.border_left: int = self.__offset_initial.x + self.__width
        self.border_right: int = self.__offset_initial.x + self.__height

    def __update_wall(self):
        wall_up = (
            (int(self.__offset_initial.x), int(self.__offset_initial.y)),
            (self.__height, self.__width))
        wall_down = (
            (int(self.__offset_initial.x+self.__width), int(self.__offset_initial.y)+self.__height),
            (self.__height, self.__width))
        wall_left = (
            (int(self.__offset_initial.x), int(self.__offset_initial.y)+self.__width),
            (self.__width, self.__height))
        wall_right = (
            (int(self.__offset_initial.x)+self.__height, int(self.__offset_initial.y)),
            (self.__width, self.__height))
        self.__walls: list = [wall_up, wall_down, wall_left, wall_right]

    def update(self, eta_h: float, eta_l: float, radius: int):
        # eta_l is useless due to exercises' constraints
        self.__update_borders(eta_h, radius)
        self.__update_wall()

    def render(self, screen: pg.Surface):
        for wall in self.__walls:
            gfxdraw.box(screen, wall, self.__color)
