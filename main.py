import curses
import time
import sys
import math
from curses import wrapper
from shuffle_string import *
from state_machine import *
from iterated_choice import *

ALPHABET = "0123456789ABCDEF"
PASSWORD = "DEADFEED"
MIN_ENTROPY = 32

arg = sys.argv[1]

key_logger = []

stdscr = None

def init():
	global stdscr
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(True)

def terminate():
	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()

def gk():
	c = stdscr.getkey()
	key_logger.append((c,time.time_ns()))
	return c

def main_iterated_choice(stdscr):
	init()
	stdscr.clear()
	stdscr.refresh()
	psswd = ""
	option = ""
	cl = get_choice_length(MIN_ENTROPY,PASSWORD)
	co = get_choice_object(PASSWORD,cl,ALPHABET)
	while(True):
		stdscr.erase()
		stdscr.addstr(get_disp_string_IC(co)+"\n"+psswd+"\n<-"+option)
		c = gk()
		if c == "\n":
			if option in co:
				psswd+=co[option]
			if option=="":
				if psswd==PASSWORD:
					stdscr.erase()
					stdscr.addstr("Success")
					break
			option=""
			co=get_choice_object(PASSWORD,cl,ALPHABET)
		else:
			if c.isdigit():
				option+=c
			if c == 'KEY_BACKSPACE':
				if len(option)!=0:
					option = option[:len(option)-1]
	c = gk()
			



def main_state_machine(stdscr):
	init()
	stdscr.clear()
	stdscr.refresh()
	grid, N = get_grid(ALPHABET)
	psswd = ""
	i = 0
	j = 0
	while(True):
		stdscr.erase()
		stdscr.addstr(get_disp_string_SM(grid,i,j)+"\n\n"+psswd)
		c = gk()
		if c=='w':
			i-=1
		if c=='s':
			i+=1
		if c=='a':
			j-=1
		if c=='d':
			j+=1
		if c=='\n':
			psswd+=grid[i][j]
			grid, N = get_grid(ALPHABET)
		def norm(c):
			if c < 0:
				return 0
			if c>=N:
				return N-1
			return c
		i = norm(i)
		j = norm(j)
		if psswd==PASSWORD:
			stdscr.erase()
			stdscr.addstr("Success")
			break
	gk()

	



def main_shuffle_string(stdscr):
	init()
	stdscr.clear()
	stdscr.refresh()
	b = get_shuffle_basis(PASSWORD,MIN_ENTROPY,ALPHABET)
	disp_string = get_disp_string(b, random_string(ALPHABET,len(b)))
	stdscr.addstr(disp_string)
	input_string = ""
	pss_string = ""

	id = 0
	while(True):
		c = gk()
		if id>=len(b):
			break
		if b[id]:
			pss_string+=c
		if b[id] or not b[id] and c==disp_string[id]:
			input_string+=c
			stdscr.erase()
			stdscr.addstr(disp_string+"\n"+input_string+"\n"+pss_string)
			id+=1

	if pss_string == PASSWORD:
		stdscr.erase()
		stdscr.addstr("Success")
	else:
		stdscr.erase()
		stdscr.addstr("Fail")
	gk()




try:
	if arg == "1":
		wrapper(main_shuffle_string)
	if arg == "2":
		wrapper(main_iterated_choice)
	if arg == "3":
		wrapper(main_state_machine)
except KeyboardInterrupt:
	print(key_logger)
	pass


