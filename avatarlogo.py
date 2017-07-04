import math
from PIL import Image, ImageDraw

class MathLogo:

    def __init__(self, size):
        self.img = Image.new('RGB', size)
        self.canvas = ImageDraw.Draw(img)


    def save(self, filename):
        self.img.save(filename, filename.rpartition('.').upper())


    def __rose_calc(self, k ,degrees):
        rad = math.degrees(degrees)
        x = math.cos(k * rad) * math.cos(rad)
        y = math.cos(k * rad) * math.sin(rad)
        return x, y


    def rose(self, x, y, r, leafcnt, rgb=(255, 255, 255)):
        prevx, prevy = self.__rose_calc(0)
        
        for angle in range(360):
            x, y = self.__rose_calc(angle)
            self.canvas.line((prevx, prevy), (x, y), fill=rgb)
            prevx, prevy = x, y


    def koch_snowflake(self):
        pass

# canvas.line((0, 0) + img.size, fill=255)
