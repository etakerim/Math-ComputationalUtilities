import math
from PIL import Image, ImageDraw

class MathLogo:

    def __init__(self, img):
        #self.img = Image.new('RGB', size)/open
        self.img = img
        self.canvas = ImageDraw.Draw(img)


    def save(self, filename):
        self.img.save(filename, filename.rpartition('.').upper())


class Rose(MathLogo):
    
    def __init__(self, x, y, r, leafcnt, color=(255, 255, 255)):
        super().__init__(img)
        self.x = x
        self.y = y
        self.r = r
        self.leaves = leafcnt
        self.rgb = color


    def __rose_calc(self, degrees):
        rad = math.degrees(degrees)
        x = math.cos(self.leaves * rad) * math.cos(rad)
        y = math.cos(self.leaves * rad) * math.sin(rad)
        return x, y


    def rose(self):
        prevx, prevy = self.__rose_calc(0)
        
        for angle in range(360):
            x, y = self.__rose_calc(angle)
            self.canvas.line((prevx, prevy), (x, y), fill=rgb)
            prevx, prevy = x, y


#def koch_snowflake(self):
#canvas.line((0, 0) + img.size, fill=255)
