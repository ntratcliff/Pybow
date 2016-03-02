import sys
from PIL import Image

mem = bytearray(256) #256 cell memory tape

def rgb2hex(r, g, b):
	return '{:02x}{:02x}{:02x}'.format(r,g,b)

#Exit the progam
def vm_exit(addr, val):
	print()
	sys.exit(0)

#Set cell at address addr to value val
def vm_set(addr, val):
	mem[addr] = val

#Sequentially prints the values of each
#cell from addr to addr2 inclusively
def vm_print(addr, addr2): 
	for i in range(addr,addr2):
		print(chr(mem[i]), end="")

#Takes input starting at addr and sets
#addr2 to the address of the cell at
#the end of the input stream
#def vm_in(addr, addr2):
	#TODO

#Sets a label of val for lookback or
#lookahead instructions
#def vm_label(addr, val):
	#TODO

#Searches backwards and resumes execution
#at the first label with value val (lazy)
#def vm_lookback(addr, val):
	#TODO

#Searches forwards and resumes execution
#at the first label with value val (lazy)
#def vm_lookahead(addr, val):
	#TODO

#Adds val to the value at addr
def vm_add(addr, val):
	mem[addr] = mem[addr] + val

#Subtracts val from the value at addr
def vm_sub(addr, val):
	mem[addr] = mem[addr] - val

#Multiplies the value at addr by val
def vm_mul(addr, val):
	mem[addr] = mem[addr] * val

#Divides the value at addr by val
def vm_div(addr, val):
	mem[addr] = mem[addr] / val

#Mods the value at addr by val
def vm_mod(addr, val):
	mem[addr] = mem[addr] % val

#instruction map
insmap = {
	'0': vm_exit,
	'1': vm_set,
	'2': vm_print,
#	'3': vm_in,
#	'5': vm_label,
#	'6': vm_lookback,
#	'7': vm_lookahead,
	'a': vm_add,
	'b': vm_sub,
	'c': vm_mul,
	'd': vm_div,
	'e': vm_mod,
}

if len(sys.argv) > 1:
	imgPath = sys.argv[1]
else: 
	sys.exit(1)

img = Image.open(imgPath)

statements = []

for r, g, b in list(img.getdata()):
	statements.append(rgb2hex(r, g, b))


for statement in statements:
	ins = statement[0]
	addr = int(statement[1:3], 16)
	switch = statement[3]
	val = int(statement[4:6], 16)

	#if switch is 1, get value at address val
	#exclusion of ins '1' and '2' is a temporary
	#workaround pending update to the Rainbow spec
	if switch == '1' and ins != '1' and ins != '2':
		val = mem[val]
	
	#execute instruction at ins
	if ins in insmap:
		insmap[ins](addr, val)
