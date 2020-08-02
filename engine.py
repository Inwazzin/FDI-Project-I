from imports import *


class Engine(object):
    def __init__(self,
                 R: int,
                 V: float = 2,
                 d: float = 0.1,
                 eta_h: float = 20,
                 eta_l: float = 20):
        """
        :param int R: Radius of a atom
        :param float V: Max speed of a atom
        :param float d: Collision Tolerance of atoms
        :param float eta_h: Atom container height coefficient
        :param float eta_l: Atom container width coefficient
        """

        # Init Const Variables
        self.R: int = R
        self.V: float = V
        self.eta_h: float = eta_h
        self.eta_l: float = eta_l
        self.tolerance: float = d
        self.refresh_rate: int = 60     # Standard refresh rate ; FPS
        # R := range 12 >= R >= 1
        # Eta_h, Eta_l := range 50>= Eta >=20
        # tolerance := range R/10 >= tolerance >= 0

        # Mechanics
        # N := 1 <= N <= (MiH * MiL) // 4
        # Collision : 2R < |atom.pos - other.pos| <= 2R + d

        # Time Variables
        self.clock: pg.time.Clock = pg.time.Clock()             # Clock
        self.dt_coefficient: float = 1 / (self.eta_h * self.V)  # Time Coefficient used to define discrete time
        self.dt: float = 0                                      # Real Time between frames
        self.discrete_dt: int = 0                               # Time difference used in the simulation

    def __update_dt(self):
        """Calculates the time difference between frames"""
        self.dt = self.clock.tick(self.refresh_rate)

    def update_time(self):
        """Calculates the time difference used in the simulation"""
        self.__update_dt()
        self.discrete_dt = self.dt_coefficient * self.dt
