from pygame import gfxdraw
import matplotlib.pyplot as plt
from typing import *
import pygame as pg
import numpy as np
import math as mh
import itertools as it
import random
import pygame_widgets as pw
import game
import sys

def get_cosine(vec1: pg.Vector2, vec2: pg.Vector2) -> float:
    return vec1.dot(vec2) / (vec1.length() * vec2.length())
def get_norm(vec1: pg.Vector2):
    vec1.normalize()
