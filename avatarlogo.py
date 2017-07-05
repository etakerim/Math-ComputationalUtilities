"""
Questions:
    1. Must you commit before branch merge
    2. Handle many arguments to member function better
    3. Similar function shared by two classes rose, lissajous
    4. Changes of unexpected manner and git
"""
import math
from PIL import Image, ImageDraw
from vector import Vector2D

WHITE_RGB = (255, 255, 255)

class MathLogo:

    def __init__(self, img, filename):
        self.img = img
        self.filename = filename
    
    def __enter__(self):
        self.canvas = ImageDraw.Draw(self.img)
        return self.canvas

    def __exit__(self, *args):
        self.img.save(
                self.filename, 
                self.filename.rpartition('.')[-1].upper()
                )


class Rose():

    def __init__(self, canvas, pos, r, leafcnt, color=WHITE_RGB):
        self.canvas = canvas
        self.pos = pos
        self.r = r
        self.leaves = leafcnt
        self.rgb = color

    def __rose_calc(self, degrees):
        rad = math.radians(degrees)
        faktor = math.cos(self.leaves * rad)        
        x = self.r * faktor * math.cos(rad) + self.pos[0]
        y = self.r * faktor * math.sin(rad) + self.pos[1]
        return x, y

    def draw(self):
        prevx, prevy = self.__rose_calc(-1)
        
        for angle in range(360):
            x, y = self.__rose_calc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


class Lissajous():

    def __init__(self, canvas, 
        pos, a_amp, b_amp, a, b, delta,
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
        prevx, prevy = self.__lissajous_calc(-1)

        for angle in range(362):
            x, y = self.__lissajous_calc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


class KochFractal():

    def __init__(self, x, y, length):
        self.a = Vector2D(x, y)
        self.b = Vector2D(x + length, y)

    def curve(self):
        pass

if __name__ == '__main__':
    IMG_SIZE = (1000, 500)

    with MathLogo(Image.new('RGB', IMG_SIZE), 'image.png') as ico:
        #center = (500 / 2, 500 / 2)
        rose = Rose(ico, (250, 250), r=200, leafcnt=4)
        rose.draw()
        lissaj = Lissajous(ico, (750, 250), 100, 100, 5, 4, 180)
        lissaj.draw()

    
    
#def koch_snowflake(self):
#canvas.line((0, 0) + img.size, fill=255)
