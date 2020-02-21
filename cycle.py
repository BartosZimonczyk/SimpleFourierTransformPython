import pygame
import math
import intervals as I
from copy import deepcopy
import random


class Cycle:
    def __init__(self, r, x, y, interval, phase):
        self.phase, self.r, self.x_center, self.y_center = phase, math.floor(math.fabs(r)), math.floor(x), math.floor(y)
        self.color = (random.randint(30, 50), random.randint(30, 50), random.randint(30, 50))
        self.interval = interval
        self.angle = 0
        self.x = self.r * math.cos(phase) + self.x_center
        self.y = self.r * math.sin(phase) + self.y_center

    def update_point(self):
        self.x = math.floor(self.r * math.cos(self.angle * self.interval + self.phase)) + self.x_center
        self.y = math.floor(self.r * math.sin(self.angle * self.interval + self.phase)) + self.y_center

