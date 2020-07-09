from imports import *

class Engine(object):
    def __init__(self,
                 R: int,
                 V: float,
                 d: float,
                 eta_h: float = 20,
                 eta_l: float = 20):

        # Mechanics
        # R - Radius    | H - Container Height = EtaH*R | L - Container Width = EtaL*R
        # 12>= R >= 1
        # 50 >= EtaH - Height Coe >= 20 | 50 >= EtaL - Width Coe >= 20
        # tak na oko wyszło, potem wychodzi za ekran, może być mniejsza w imię sliderów,
        # jak tam czytałem on proponuje tylko do 100, czyli można mniej, hence te eta_h <= 50
        # a większej rozdziałki nie chcę robić, bo lapka mi smali xD

        # 1 <= N <= (MiH * MiL) // 4
        # m = 1

        # Collision : 2R < |pos_i - pos_j| <= 2R + d
        # 0 <= d <= R/10
        # Maciej stuff
        # Time :
        # Ania stuff

        # init physic engine variables
        self.R: int = R                 # Radius of the atoms Experimental range := 12 >= R >= 1
        self.V: float = V               # Max Speed of the atoms
        self.eta_h: float = eta_h       # Container Height coefficient Experimental range := 50>=eta_h>=20
        self.eta_l: float = eta_l       # Container Width coefficient (Height should == Width)
        self.tolerance: float = d       # Atom Collision Tolerance coefficient
        self.global_angle: int = 0
        self.clock: pg.time.Clock = pg.time.Clock()

    def delta_time(self):
        pass
