import sys
from PIL import Image

mem = bytearray(256) #256 cell memory tape
statements = [] #statements in image
currStatement = 0 #current statement index
ioMode = "-a"

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
	for i in range(addr,addr2+1):
		if ioMode == "-d":
			print(mem[i], end="")
		elif ioMode == "-h":
			print(format(mem[i], "x"), end="")
		else:
			print(chr(mem[i]), end="")

#Takes input starting at addr and sets
#addr2 to the address of the cell at
#the end of the input stream
def vm_in(addr, addr2):
	inp = input()
	i = 0
	if ioMode == "-d" or ioMode == "-h":
		mem[addr] = int(inp)
	else:
		for c in inp:
			mem[addr+i] = ord(c)
			i+=1
	mem[addr2] = addr + i	

#Sets a label of val for lookback or
#lookahead instructions
#empty 
def vm_label(addr, val):
	return

#Checks if the value of a label statement
#is the same as val
def vm_evallabel(statement, val):
	if statement[0] == '5':
		lswitch = statement[3]
		lval = int(statement[4:6], 16)
		if lswitch == '1':
			lval = mem[lval]
		if lval == val:
			return True
	return False

#Searches backwards and resumes execution
#at the first label with value val (lazy)
def vm_lookback(addr, val):
	global currStatement	
	while currStatement > 0:
		currStatement -= 1
		if vm_evallabel(statements[currStatement], val):
			return

#Searches forwards and resumes execution
#at the first label with value val (lazy)
def vm_lookahead(addr, val):
	global currStatement
	while currStatement < len(statements):
		currStatement += 1
		if vm_evallabel(statements[currStatement], val):
			return

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
	'3': vm_in,
	'5': vm_label,
	'6': vm_lookback,
	'7': vm_lookahead,
	'a': vm_add,
	'b': vm_sub,
	'c': vm_mul,
	'd': vm_div,
	'e': vm_mod,
}

if len(sys.argv) <= 1:
	sys.exit()

for arg in sys.argv:
	if arg[0] == "-":
		ioMode = arg
	else:
		imgPath = arg

img = Image.open(imgPath)

for r, g, b in list(img.getdata()):
	statements.append(rgb2hex(r, g, b))

while currStatement < len(statements):
	statement = statements[currStatement]
	ins = statement[0]
	addr = int(statement[1:3], 16)	
	switch = statement[3]
	val = int(statement[4:6], 16)
	
	#if switch is 1, get value at address val
	#exclusion of ins '1' and '2' is a temporary
	#workaround pending update to the Rainbow spec
	if switch == '1' and ins != '2' and ins != '3':
		val = mem[val]
	
	if ins in insmap:
		insmap[ins](addr, val)

	currStatement+=1
