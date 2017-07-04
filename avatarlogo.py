"""
Questions:
    1. Must you commit before branch merge
    2. Handle many arguments to member function better
    3. Similar function shared by two classes rose, lissajous
"""
import math
from PIL import Image, ImageDraw

WHITE_RGB = (255, 255, 255)

class MathLogo:

    def __init__(self, img):
        #self.img = Image.new('RGB', size)/open
        self.img = img
        self.canvas = ImageDraw.Draw(img)

    def save(self, filename):
        self.img.save(filename, filename.rpartition('.')[-1].upper())


class Rose(MathLogo):

    def __init__(self, img, x, y, r, leafcnt, color=WHITE_RGB):
        super().__init__(img)
        self.x = x
        self.y = y
        self.r = r
        self.leaves = leafcnt
        self.rgb = color

    def __rose_calc(self, degrees):
        rad = math.radians(degrees)
        faktor = math.cos(self.leaves * rad)        
        x = self.r * faktor * math.cos(rad) + self.x
        y = self.r * faktor * math.sin(rad) + self.y
        return x, y

    def draw(self):
        prevx, prevy = self.__rose_calc(0)
        
        for angle in range(360):
            x, y = self.__rose_calc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


class Lissajous(MathLogo):

    def __init__(self, img, x, y, a, b, color=WHITE_RGB):
        super().__init__(img)
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.rgb = color

    def draw(self):
        prevx, prevy = self.__lissajous_calc(0)

        for angle in range(360):
            x, y = self.__lissajous_calc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


if __name__ == '__main__':
    ico = Image.new('RGB', (500, 500))
    drawing = Rose(ico, ico.size[0] / 2, ico.size[1] / 2, 200, 4)
    drawing.rose()
    drawing.save('icon.png')

#def koch_snowflake(self):
#canvas.line((0, 0) + img.size, fill=255)
