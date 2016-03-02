import sys
from PIL import Image

def rgb2hex(r, g, b):
	return '{:02x}{:02x}{:02x}'.format(r,g,b)

def 

if len(sys.argv) > 1:
	imgPath = sys.argv[1]
else: 
	sys.exit(1)

img = Image.open(imgPath)

statements = []

for r, g, b in list(img.getdata()):
	statements.append(rgb2hex(r, g, b))

mem = bytearray(256)

for statement in statements:
	ins = statement[0]
	addr = statement[1:2]
	switch = statement[3]
	val = statement[4:5]	
