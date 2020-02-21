import pygame
from cycle import Cycle
import math
import random
from complex import Complex


class Fourier:
    def __init__(self, points=None):
        self.H = 900
        self.W = 1500
        self.DISPLAY = None
        self.BACKGROUND = (0, 0, 0)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.points = points if points is not None else []
        self.intervals_y = sorted(self.dft([p[1] for p in self.points]), key=lambda x: x[0], reverse=True)
        self.intervals_x = sorted(self.dft([p[0] for p in self.points]), key=lambda x: x[0], reverse=True)
        self.complex_intervals = sorted(self.dft2(self.points), key=lambda x: x[0], reverse=True)
        self.cycles_x = []
        self.cycles_y = []
        self.complex_cycles = []
        self.time = 0
        self.dt = 2*math.pi/len(self.points) if len(self.points) != 0 else 1
        self.point_x = None
        self.point_y = None
        self.complex_point = None
        self.complex_drawing = []
        self.drawing = []

    @staticmethod
    def dft(points):
        X = []
        N = len(points)

        for k in range(N):
            re = 0
            im = 0
            for n in range(N):
                const = 2*math.pi*k*n/N
                re += points[n]*math.cos(const)
                im -= points[n]*math.sin(const)
            re = re / N
            im = im / N
            radius = math.sqrt(im**2 + re**2)
            phase = math.atan2(im, re)
            if radius > 1:
                X.append((radius, k, phase))
        return X

    @staticmethod
    def dft2(points):
        complex_list = [Complex(p[0], p[1]) for p in points]
        N = len(complex_list)
        X = []
        for k in range(N):
            x = Complex(0, 0)
            for n in range(N):
                t = 2 * math.pi * k * n / N
                c = Complex(math.cos(t), -math.sin(t))
                x += c * complex_list[n]
            x.re = x.re / N
            x.im = x.im / N
            radius = x.length()
            phase = x.angle()
            if radius > 1:
                X.append((radius, k, phase))
        return X

    def draw_circle(self, cycle):
        pygame.draw.line(self.DISPLAY, cycle.color, (cycle.x_center, cycle.y_center), (cycle.x, cycle.y))
        pygame.draw.circle(self.DISPLAY, cycle.color, (cycle.x_center, cycle.y_center), cycle.r, 1)

    def get_image(self):
        if not self.points == []:
            return

        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.W, self.H), 0)
        self.DISPLAY.fill(self.BACKGROUND)
        quit_draw = False
        draw = []
        while not quit_draw:
            self.DISPLAY.fill(self.BACKGROUND)
            mouse = pygame.mouse.get_pressed()
            if mouse == (1, 0, 0):
                x, y = pygame.mouse.get_pos()
                self.points.append((x - self.W / 2, y - self.H / 2))
                draw.append((x, y))
            if len(draw) > 1:
                pygame.draw.lines(self.DISPLAY, (255, 255, 255), False, draw, 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_draw = True

            pygame.display.flip()
            self.CLOCK.tick(self.FPS)
        self.complex_intervals = sorted(self.dft2(self.points), key=lambda x: x[0], reverse=True)
        self.dt = 2 * math.pi / len(self.points)

    def play1(self, waves=False):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.W, self.H), 0)
        self.DISPLAY.fill(self.BACKGROUND)
        quit_draw = False
        for n, cycle in enumerate(self.complex_intervals):
            if n == 0:
                self.complex_cycles.append(Cycle(cycle[0], self.W/2, self.H/2, cycle[1], cycle[2]))
            else:
                self.complex_cycles.append(
                    Cycle(cycle[0], self.complex_cycles[n - 1].x, self.complex_cycles[n - 1].y, cycle[1], cycle[2]))
        while not quit_draw:
            self.DISPLAY.fill(self.BACKGROUND)

            for n, cycle in enumerate(self.complex_cycles):
                self.draw_circle(cycle)
                cycle.angle = self.time
                cycle.update_point()
                if n < len(self.complex_cycles)-1:
                    self.complex_cycles[n+1].x_center = cycle.x
                    self.complex_cycles[n+1].y_center = cycle.y

            self.complex_point = [self.complex_cycles[-1].x, self.complex_cycles[-1].y]
            pygame.draw.circle(self.DISPLAY, (255, 0, 0), self.complex_point, 2)
            self.complex_drawing.append(self.complex_point)
            # przesuwanie
            if waves:
                for n in range(len(self.complex_drawing)):
                    self.complex_drawing[n] = (self.complex_drawing[n][0]+1, self.complex_drawing[n][1])
                self.complex_drawing = [point for point in self.complex_drawing if point[0] < 1520]
            else:
                if self.time > 2*math.pi:
                    self.complex_drawing = []
                    self.time = 0

            if len(self.complex_drawing) > 1:
                pygame.draw.lines(self.DISPLAY, (255, 255, 255), False, self.complex_drawing)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_draw = True
                    pygame.quit()
                    quit()

            pygame.display.flip()
            self.time += self.dt
            self.CLOCK.tick(self.FPS)

    def play(self):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((self.W, self.H), 0)
        self.DISPLAY.fill(self.BACKGROUND)
        quit_draw = False
        for n, cycle in enumerate(self.intervals_x):
            if n == 0:
                self.cycles_x.append(Cycle(cycle[0], 800, 100, cycle[1], cycle[2]))
            else:
                self.cycles_x.append(Cycle(cycle[0], self.cycles_x[n - 1].x, self.cycles_x[n - 1].y, cycle[1], cycle[2]))
        for n, cycle in enumerate(self.intervals_y):
            if n == 0:
                self.cycles_y.append(Cycle(cycle[0], 200, 600, cycle[1], cycle[2]))
            else:
                self.cycles_y.append(Cycle(cycle[0], self.cycles_y[n - 1].x, self.cycles_y[n - 1].y, cycle[1], cycle[2]))
        while not quit_draw:
            self.DISPLAY.fill(self.BACKGROUND)

            for n, cycle in enumerate(self.cycles_x):
                self.draw_circle(cycle)
                cycle.angle += self.time/60
                cycle.update_point()
                if n < len(self.cycles_x)-1:
                    self.cycles_x[n+1].x_center = cycle.x
                    self.cycles_x[n+1].y_center = cycle.y
            for n, cycle in enumerate(self.cycles_y):
                self.draw_circle(cycle)
                cycle.angle += self.time/60
                cycle.update_point()
                if n < len(self.cycles_y)-1:
                    self.cycles_y[n+1].x_center = cycle.x
                    self.cycles_y[n+1].y_center = cycle.y

            self.point_x = [self.cycles_x[-1].x, self.cycles_x[-1].y]
            self.point_y = [self.cycles_y[-1].x, self.cycles_y[-1].y]
            pygame.draw.circle(self.DISPLAY, (255, 0, 0), self.point_x, 2)
            pygame.draw.circle(self.DISPLAY, (255, 0, 0), self.point_y, 2)

            self.drawing.append([self.point_x[0], self.point_y[1]])
            pygame.draw.line(self.DISPLAY, (255, 255, 255), self.point_x, self.drawing[-1])
            pygame.draw.line(self.DISPLAY, (255, 255, 255), self.point_y, self.drawing[-1])
            if self.time > 2*math.pi:
                self.drawing = []
            if len(self.drawing) > 1:
                pygame.draw.lines(self.DISPLAY, (255, 255, 255), False, self.drawing)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_draw = True
                    pygame.quit()
                    quit()

            pygame.display.flip()

            self.CLOCK.tick(self.FPS)


if __name__ == '__main__':
    w = Fourier()
    w.get_image()
    print(w.points)
    w.play1()
