import math
from PIL import Image, ImageDraw

class MathLogo:

    def __init__(self, size):
        self.img = Image.new('RGB', size)
        self.canvas = ImageDraw.Draw(img)

    def save(self, filename):
        self.img.save(filename, filename.rpartition('.').upper())
        
    def __rose_calc(self, degrees):
        pass

    def rose(self, x, y, r, leafcnt):
        pass

    def koch_snowflake(self):
        pass

# canvas.line((0, 0) + img.size, fill=255)
