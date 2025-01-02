
import math
import random

def get_grid(ALPHABET):
	ALPHABET = "".join(random.sample(ALPHABET,len(ALPHABET)))
	N = math.ceil(math.sqrt(len(ALPHABET)))
	grid = []
	for i in range(N):
		row = []
		for j in range(N):
			row.append(None)
		grid.append(row)
	p=0
	for i in range(N):
		for j in range(N):
			if p<len(ALPHABET):
				grid[i][j] = ALPHABET[p]
			p+=1
	return grid, N

def get_disp_string_SM(grid,i,j):
	answer = ""
	for I in range(len(grid)):
		for J in range(len(grid[0])):
			if i==I and (j==J or J==j+1):
				answer+="|"
			else:
				answer+=" "
			if grid[I][J]:
				answer+=str(grid[I][J])
			else:
				answer+=str(" ")
		if i==I and j==len(grid[0])-1:
			answer+="|"
		answer+="\n"
	return answer