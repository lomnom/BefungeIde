import Terminal as term
import Befunge as bf

term.raw()
term.noctrlc()
for key in term.keys():
	if key=="ctrl x":
		break
	else:
		print(key)
term.ctrlc()
term.unraw()