hidecursor="\033[?25l"
showcursor="\033[?25h"

homecursor="\033[H"

savecursor="\033[s"
loadcursor="\033[u"

normalscreen="\033[?47l"
canvasscreen="\033[?47h"

cleartoeos="\033[0J"
cleartoeol="\033[0K"

movecursor="\033[{row};{column}H"

green="\033[32m"
yellow="\033[33m"
red="\033[31m"
blue="\033[34m"
cyan="\033[36m"
default="\033[39m" #reset text color

bold="\033[1m"

from sys import stdin,stdout
from os import get_terminal_size as termsize
from threading import Thread as thread
from subprocess import run as syscall
from threading import Lock as lock
from time import sleep as wait
from random import randint as random
from random import choice 
import termios, sys
import select
fd=stdin.fileno()

def sfprint(*stuff):
	if len(stuff)>1:
		stdout.write(" ".join(stuff))
	else:
		stdout.write(stuff[0])

def fprint(*stuff):
	if len(stuff)>1:
		stdout.write(" ".join(stuff))
	else:
		stdout.write(stuff[0])
	stdout.flush()

size=termsize()
rows=size.lines
columns=size.columns
maxx=columns-1
maxy=rows-1

read=stdin.read

rawBackup=None
def raw():
	global rawBackup
	if not rawBackup==None: return
	rawBackup=termios.tcgetattr(fd)
	raw=termios.tcgetattr(fd)
	raw[3]=raw[3] & ~(termios.ECHO | termios.ICANON)
	termios.tcsetattr(fd,termios.TCSADRAIN,raw)

def unraw():
	global rawBackup
	if rawBackup==None: return
	termios.tcsetattr(fd,termios.TCSADRAIN,rawBackup)
	rawBackup=None

ctrlcBackup=None
def noctrlc():
	global ctrlcBackup
	if not ctrlcBackup==None: return
	ctrlcBackup=termios.tcgetattr(fd)
	noctrlc=termios.tcgetattr(fd)
	noctrlc[3]=noctrlc[3] & ~termios.ISIG
	termios.tcsetattr(fd,termios.TCSADRAIN,noctrlc)

def ctrlc():
	global ctrlcBackup
	if ctrlcBackup==None: return
	termios.tcsetattr(fd,termios.TCSADRAIN,ctrlcBackup)
	ctrlcBackup=None

def canvas():
	fprint(savecursor+hidecursor+canvasscreen)

def clear():
	fprint(homecursor+cleartoeos)

def uncanvas():
	fprint(normalscreen+loadcursor+showcursor) #restore terminal

mappings={
	0:"ctrl 1",
	27:"ctrl 2",
	28:"ctrl 3",
	29:"ctrl 4",
	30:"ctrl 5",
	31:"ctrl 6",
	127:"ctrl 7",
	23:"ctrl w",
	5:"ctrl e",
	18:"ctrl r",
	20:"ctrl t",
	25:"ctrl y",
	21:"ctrl u",
	9:"ctrl i",
	16:"ctrl p",
	1:"ctrl a",
	4:"ctrl d",
	6:"ctrl f",
	7:"ctrl g",
	8:"ctrl h",
	11:"ctrl k",
	12:"ctrl l",
	26:"ctrl z",
	24:"ctrl x",
	3:"ctrl c",
	2:"ctrl b",
	14:"ctrl n"
}
def proccessTermChar(char):
	if ord(char) in mappings:
		return mappings[ord[char]]
	else: 
		return char

arrowChars={"A":"up","B":"down","C":"right","D":"left"}
arrowModifyers={"2":"shift","3":"option","4":"shift option"}
def isarrow(key):
	if key.startswith('\033['):
		key=key[2:]
		if len(key)==1: #maybe non-shifted key
			if key in arrowChars:
				return arrowChars[key]
		elif len(key)==4: #modified key
			if key.startswith("1;"):
				key=key[2:]
				if key[0] in arrowModifyers:
					modifyer=arrowModifyers[key[0]]
					key=key[1:]
					if key in arrowChars:
						return modifyer+" "+arrowChars[key]
	return False

def stdinempty():
	return not select.select([sys.stdin,],[],[],0.0)[0]

def readall():
	data=""
	while not stdinempty():
		data+=stdin.read(1)
	return data

class KeyHandler:
		def __init__(self,actions):
			self.actions=actions
			self.thread=None
			self.delay=0.05
			self.tasks=[]

		def _handle(self):
			while self.thread!=None:
				try:
					key=stdin.read(1)
					action=self.actions[key]
				except KeyError:
					try:
						action=self.actions["default"]
					except KeyError:
						continue
				self.tasks+=[[key,thread(target=action[0],args=action[1])]]
				self.tasks[-1][1].start()
				for task in reversed(range(len(self.tasks))):
					if not self.tasks[task][1].is_alive():
						self.tasks.pop(task)
				wait(self.delay)

		def handle(self):
			if self.thread==None:
				self.thread=thread(target=self._handle)
				self.thread.start()

		def stop(self):
			self.thread=None
			self.tasks=[]