import math
from PIL import Image, ImageDraw
from vector import Vector2D

WHITE_RGB = (255, 255, 255)
GREEN_RGB = (0,   255,   0)

class MathLogo:

    def __init__(self, img, filename):
        self.img = img
        self.filename = filename

    def __enter__(self):
        self.canvas = ImageDraw.Draw(self.img)
        return self.canvas

    def __exit__(self, *args):
        self.img.save(self.filename, 
                      self.filename.rpartition('.')[-1].upper())


class PeriodicMathFunc():
    def period_draw(self, mfunc):
        prevx, prevy = mfunc(-1)

        for angle in range(360):
            x, y = mfunc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


class Rose(PeriodicMathFunc):
    def __init__(self, canvas, pos, r, leafcnt, color=WHITE_RGB):
        self.canvas = canvas
        self.pos = pos
        self.r = r
        if leafcnt % 2 == 0:
            self.leaves = leafcnt / 2
        else:
            self.leaves = leafcnt
        self.rgb = color

    def __rose_calc(self, degrees):
        rad = math.radians(degrees)
        faktor = math.cos(self.leaves * rad)        
        x = self.r * faktor * math.cos(rad) + self.pos[0]
        y = self.r * faktor * math.sin(rad) + self.pos[1]
        return x, y

    def draw(self):
        self.period_draw(self.__rose_calc)


class Lissajous(PeriodicMathFunc):
    def __init__(self, canvas, 
                 pos, a_amp, b_amp, a=5, b=4, delta=math.pi,
                 color=WHITE_RGB):

        self.canvas = canvas
        self.pos = pos
        self.a_amp = a_amp
        self.b_amp = b_amp
        self.delta = math.radians(delta)
        self.a = a
        self.b = b
        self.rgb = color

    def __lissajous_calc(self, degrees):
        rad = math.radians(degrees)
        x = self.a_amp * math.sin(self.a * rad + self.delta) + self.pos[0]
        y = self.b_amp * math.sin(self.b * rad) + self.pos[1]
        return x, y

    def draw(self):
       self.period_draw(self.__lissajous_calc) 


class KochFractal():
    def __init__(self, canvas, color=WHITE_RGB):
        self.canvas = canvas
        self.rgb = color

    def curve(self, a, b):
        if abs(b - a) < 3:
            self.canvas.line(a.data + b.data, fill=self.rgb)
            return
        
        divpoints = [a]
        for faktor in range(1, 4):
            divpoints.append(a + faktor * ((b - a) / 3))
        
        self.curve(divpoints[0], divpoints[1]) 
        
        middlelen = divpoints[2] - divpoints[1]
        c = middlelen.rotate(math.radians(60))
        self.curve(divpoints[1], divpoints[1] + c)
        
        c = middlelen.rotate(math.radians(-60))
        self.curve(divpoints[2] - c, divpoints[2]) 
       
        self.curve(divpoints[2], divpoints[3])

    def snowflake(self, x, y, r):
        center = Vector2D(x, y)
        radius = Vector2D(r, 0)

        points = [
                  center + radius.rotate(math.radians(-45)),
                  center + radius.rotate(math.radians(90)),
                  center + radius.rotate(math.radians(-135))
                 ]

        self.curve(points[0], points[2]) 
        self.curve(points[1], points[0])
        self.curve(points[2], points[1])


class FractalTree():
    def __init__(self, canvas, factor, angle, areleaves=False, leafsize=5, 
                isgrowdown=False, color=WHITE_RGB, 
                leaffill=GREEN_RGB, leafoutline=GREEN_RGB):
        self.canvas = canvas
        self.factor = factor
        self.angle = angle
        self.isgrowdown = isgrowdown 
        self.leafsize = leafsize
        self.areleaves = areleaves
        self.rgb = color
        self.leaffill = leaffill
        self.leafoutline = leafoutline


    def __branch(self, a, b, l):
        if l == 0 or abs(b - a) < 2:
            if self.areleaves:
                self.canvas.ellipse(b.data + (b + Vector2D(self.leafsize, 
                                    self.leafsize)).data, fill=self.leaffill,
                                    outline=self.leafoutline)
            return

        dirangle = math.pi
        if self.isgrowdown:
            dirangle = 0

        c = (b - a) * self.factor
        b1 = b - c.rotate(self.angle + dirangle)
        b2 = b - c.rotate(-self.angle + dirangle)

        self.canvas.line(b.data + b1.data, self.rgb)
        self.__branch(b, b1, l - 1)
        self.canvas.line(b.data + b2.data, self.rgb)
        self.__branch(b, b2, l - 1)


    def tree(self, x, y, rootheight, depth):
        y2 = y - rootheight
        if self.isgrowdown:
            y2 = y + rootheight
        self.canvas.line((x, y, x, y - rootheight), self.rgb) 
        self.__branch(Vector2D(x, y), Vector2D(x, y - rootheight), depth)


if __name__ == '__main__':
    IMG_SIZE = (600, 500)

    with MathLogo(Image.new('RGB', IMG_SIZE), 'image.png') as ico:
        center = (IMG_SIZE[0] / 2, IMG_SIZE[1] / 2 + 10)
        treebase = (IMG_SIZE[0] / 2, IMG_SIZE[1] - (IMG_SIZE[1] / 3))
        
        KochFractal(ico).snowflake(*center, 220)
        FractalTree(ico, 0.60, math.radians(35), areleaves=True).tree(*treebase, 80, 20)
        Lissajous(ico, treebase, 30, 30).draw()
        Rose(ico, (180, treebase[1] - 20), 30, 8).draw()
        Rose(ico, (420, treebase[1] - 20), 30, 8).draw()
