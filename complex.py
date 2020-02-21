import math


class Complex:
    def __init__(self, a, b):
        self.re = a
        self.im = b

    def __mul__(self, other):
        return Complex(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)

    def __add__(self, other):
        return Complex(self.re + other.re, self.im + other.im)

    def angle(self):
        return math.atan2(self.im, self.re)

    def length(self):
        return math.sqrt(self.re**2 + self.im**2)
