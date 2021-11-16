import Terminal as term
import Befunge as bf

def halt():
	global handler,running
	handler.stop()
	term.ctrlc()
	term.unraw()

term.raw()
term.noctrlc()

handler=term.KeyHandler({
	"ctrl x":term.Action(halt),
	"default":term.Action(print)
})

handler.handle()