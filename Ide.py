import Terminal as term
import Befunge as bf

term.raw()
term.noctrlc()
while True:
	stuff=term.read(1)
	if stuff=='q':
		break
	elif stuff.isalnum():
		print(stuff+" ({})".format(ord(stuff)))
	else:
		print("({})".format(ord(stuff)))
term.ctrlc()
term.unraw()