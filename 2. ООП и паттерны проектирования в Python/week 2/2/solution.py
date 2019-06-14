import pygame
import random
import math


class Vec2d:
    """Class that describes the vector in 2D space"""

    def __init__(self, x=0, y=None):
        if y is None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return f'Vec2d({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, val):
        if isinstance(val, Vec2d):
            return self.x * val.x + self.y * val.y
        return Vec2d(self.x * val, self.y * val)

    def __neg__(self):
        return Vec2d(-self.x, -self.y)

    def __len__(self):
        return math.hypot(self.x, self.y)

    def int_pair(self):
        return int(self.x), int(self.y)


class Polyline:
    def __init__(self, screen_din=(800, 600)):
        self.points = []
        self.speeds = []
        self.screen_din = screen_din

    def clear(self):
        self.points = []
        self.speeds = []

    def speed_up(self):
        for i in range(len(self.speeds)):
            self.speeds[i] *= 1.1

    def slow_down(self):
        for i in range(len(self.speeds)):
            self.speeds[i] *= 0.9

    def add_point(self, point, speed):
        """Add coordinates"""
        self.points.append(point)
        self.speeds.append(speed)

    def dell_last_point(self):
        if self.points and self.speeds:
            self.points.pop()
            self.speeds.pop()

    def set_points(self):
        """Recalculation coordinates"""
        for p in range(len(self.points)):
            self.points[p] += self.speeds[p]
            if self.points[p].x > self.screen_din[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > self.screen_din[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def draw_points(self, gameDisplay, width=3, color=(255, 255, 255)):
        for p in self.points:
            pygame.draw.circle(gameDisplay, color, p.int_pair(), width)


class Knot(Polyline):
    def __init__(self, steps, screen_din=(800, 600)):
        super().__init__(screen_din)
        self.steps = steps

    def plus_step(self):
        self.steps += 1

    def minus_step(self):
        if self.steps > 1:
            self.steps -= 1

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot()

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    def get_point(self, points, alpha, deg=None):
        """Polyline smoothing"""
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.steps
        res = []
        for i in range(self.steps):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def draw_line(self, gameDisplay, width=3, color=(255, 255, 255)):
        points = self.get_knot()
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, points[p_n].int_pair(),
                             points[p_n + 1].int_pair(), width)


class MyGame:
    def __init__(self, screen_din=(800, 600), steps=20, hue=0):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(screen_din)
        pygame.display.set_caption("MyScreenSaver")

        self.screen_din = screen_din
        self.steps = steps
        self.pause = True
        self.color = pygame.Color(0)
        self.hue = hue
        self.storage = []

    def end_game(self):
        pygame.display.quit()
        pygame.quit()

    def restart_game(self):
        self.storage.clear()

    def make_it_faster(self):
        self.storage[-1][0].speed_up()
        self.storage[-1][1].speed_up()

    def make_it_slower(self):
        self.storage[-1][0].slow_down()
        self.storage[-1][1].slow_down()

    def new_point(self, pos):
        self.storage[-1][0].add_point(Vec2d(pos),
                                      Vec2d(random.random() * 2, random.random() * 2))
        self.storage[-1][1].add_point(Vec2d(pos),
                                      Vec2d(random.random() * 2, random.random() * 2))

    def draw_it(self):
        self.gameDisplay.fill((0, 0, 0))
        self.hue = (self.hue + 1) % 360
        self.color.hsla = (self.hue, 100, 50, 100)
        for pol in self.storage:
            pol[0].draw_points(self.gameDisplay)
            pol[1].draw_line(self.gameDisplay, 3, self.color)

    def is_pause(self):
        if not self.pause:
            for pol in self.storage:
                pol[0].set_points()
                pol[1].set_points()

    def dell_point(self):
        self.storage[-1][0].dell_last_point()
        self.storage[-1][1].dell_last_point()

    def add_new_line(self):
        self.storage.append((Polyline(self.screen_din), Knot(self.steps, self.screen_din)))

    def start_game(self):
        self.add_new_line()
        working = True
        show_help = False
        while working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        working = False
                    if event.key == pygame.K_r:
                        self.restart_game()
                        self.add_new_line()
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_n:
                        self.add_new_line()
                    if event.key == pygame.K_z:
                        self.dell_point()
                    if event.key == pygame.K_f:
                        self.make_it_faster()
                    if event.key == pygame.K_s:
                        self.make_it_slower()
                    if event.key == pygame.K_KP_PLUS:
                        self.storage[-1][1].plus_step()
                    if event.key == pygame.K_F1:
                        show_help = not show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.storage[-1][1].minus_step()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.new_point(event.pos)
            self.draw_it()
            self.is_pause()
            if show_help:
                self.draw_help()
            pygame.display.flip()
        self.end_game()

    def draw_help(self):
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["F", "Faster"],
            ["S", "Slower"],
            ["Z", "Delete last point"],
            ["N", "Create new line"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["", ""],
            [str(self.storage[-1][1].steps), "Current points"]
        ]

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


g = MyGame()
g.start_game()
