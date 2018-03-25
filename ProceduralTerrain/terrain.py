import sys
import pygame
import random
import math
from PIL import Image, ImageDraw
import collections

Point = collections.namedtuple('Point', ['x', 'y'])


class Terrain:
    def __init__(self, detail):
        self.max = 2 ** detail
        self.size = self.max + 1
        self.map = [0] * (self.size ** 2)

    def look(self, x, y):
        if x < 0 or x > self.max or y < 0 or y > self.max:
            return -1
        else:
            return self.map[x + self.size * y]

    def put(self, x, y, value):
        self.map[x + self.size * y] = value

    def average(self, values):
        total = 0
        cnt = 0
        for i in values:
            if i != -1:
               total += i
               cnt += 1
        return total / cnt

    def square(self, x, y, size, offset):
        ave = self.average([self.look(x - size, y - size),
                            self.look(x + size, y - size),
                            self.look(x + size, y + size),
                            self.look(x - size, y + size)
                          ])
        self.put(x, y, ave + offset)

    def diamond(self, x, y, size, offset):
        ave = self.average([self.look(x, y - size),
                            self.look(x + size, y),
                            self.look(x, y + size),
                            self.look(x - size, y)
                          ])
        self.put(x, y, ave + offset)

    def divide(self, size, roughness):
        half = size // 2
        scale = roughness * size

        if half < 1:
            return

        for y in range(half, self.max, size):
            for x in range(half, self.max, size):
                self.square(x, y, half, 0.5) # random.random() * scale * 2 - scale)

        for y in range(0, self.max + 1, half):
            for x in range((y + half) % size, self.max + 1, size):
                self.diamond(x, y, half, 0.5) # random.random() * scale * 2 - scale)

        self.divide(size // 2, roughness)

    def generate(self, roughness):
        self.put(0, 0, self.max)
        self.put(self.max, 0, self.max / 2)
        self.put(self.max, self.max, 0)
        self.put(0, self.max, self.max / 2)

        self.divide(self.max, roughness)

    def draw(self, ctx, width, height):
        self.ctx = ctx
        water_val = self.size * 0.3
        self.width = width
        self.height = height

        for y in range(self.size):
            for x in range(self.size):
                val = self.look(x, y)
                top = self.project(x, y, val)
                bottom = self.project(x + 1, y, 0)
                water = self.project(x, y, water_val)
                style = self.brightness(x, y, self.look(x + 1, y) - val)

                self.rect(top, bottom, style)
                self.rect(water, bottom, (50, 150, 250, 65))

    def rect(self, a, b, style):
        if b.y < a.y:
            return
        # area = [math.ceil(x) for x in [a.x, a.y, b.x - a.x, b.y - a.y]]
        # pygame.draw.rect(self.ctx, style, area)
        area = [math.ceil(x) for x in [a.x, a.y, b.x, b.y]]
        self.ctx.rectangle(area, fill=style)

    def brightness(self, x, y, slope):
        if y == self.max or x == self.max:
            return (0, 0, 0, 255)
        else:
            b = int(slope * 40) + 128
            if b < 0:
                b = 0
            elif b > 255:
                b = 255
            return (b, b, b, 255)

    def iso(self, x, y):
        return Point(x=0.5 * (self.size + x - y), y=0.5 * (x + y))

    def project(self, flat_x, flat_y, flat_z):
        point = self.iso(flat_x, flat_y)
        x0 = self.width * 0.5
        y0 = self.height * 0.2
        z = self.size * 0.5 - flat_z + point.y * 0.75
        x = (point.x - self.size * 0.5) * 6
        y = (self.size - point.y) * 0.005 + 1

        return Point(x=x0 + x / y, y=y0 + z / y)

obr_sirka = 1280
obr_vyska = 1024
obr = pygame.display.set_mode([obr_sirka, obr_vyska])
pygame.display.set_caption('Terrain generation')

terrain = Terrain(9)
terrain.generate(0.7)
# terrain.draw(obr, obr_sirka, obr_vyska)

pilimg = Image.new('RGBA', (obr_sirka, obr_vyska))
terrain.draw(ImageDraw.Draw(pilimg), obr_sirka, obr_vyska)
pilimg.save('test.png')

t = pygame.image.load('test.png').convert_alpha()
obr.blit(t, (0, 0))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
