from PIL import Image, ImageDraw

img = Image.new('RGB', (640, 480))

canvas = ImageDraw.Draw(img)
canvas.line((0, 0) + img.size, fill=255)
img.save('avatar.png', 'PNG')
