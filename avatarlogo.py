import math
from PIL import Image, ImageDraw


class MathLogo:

    def __init__(self, img):
        #self.img = Image.new('RGB', size)/open
        self.img = img
        self.canvas = ImageDraw.Draw(img)

    def save(self, filename):
        self.img.save(filename, filename.rpartition('.')[-1].upper())


class Rose(MathLogo):

    def __init__(self, img, x, y, r, leafcnt, color=(255, 255, 255)):
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

    def rose(self):
        prevx, prevy = self.__rose_calc(0)
        
        for angle in range(360):
            x, y = self.__rose_calc(angle)
            self.canvas.line((prevx, prevy, x, y), fill=self.rgb)
            prevx, prevy = x, y


if __name__ == '__main__':

    ico = Image.new('RGB', (500, 500))
    drawing = Rose(ico, ico.size[0] / 2, ico.size[1] / 2, 200, 4)
    drawing.rose()
    drawing.save('icon.png')

#def koch_snowflake(self):
#canvas.line((0, 0) + img.size, fill=255)
