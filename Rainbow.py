import sys
from PIL import Image

def rgb2hex(r, g, b):
	return '{:02x}{:02x}{:02x}'.format(r,g,b)

if len(sys.argv) > 1:
	imgPath = sys.argv[1]
else: 
	sys.exit(1)

img = Image.open(imgPath)


for r, g, b in list(img.getdata()):
	print rgb2hex(r, g, b)
