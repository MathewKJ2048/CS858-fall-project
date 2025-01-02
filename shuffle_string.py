import os
import random


def get_shuffle_basis(PASSWORD, entropy, alphabet):
	# repeatedly insert characters
	n = len(PASSWORD)
	basis = [True]*n
	m = entropy-n
	for i in range(m):
		cl = len(basis)
		# insert position is anywhere from 0 to cl
		id = random.randint(0,cl)
		new_basis = []
		for k in range(cl+1):
			if k==id:
				new_basis.append(False)
			if k<cl:
				new_basis.append(basis[k])
		basis = new_basis
	return basis


def random_string(alphabet,n):
	s = ""
	for i in range(n):
		s+=alphabet[random.randint(0,len(alphabet)-1)]
	return s

def get_disp_string(basis,random_string):
	empty = "☐"
	disp_string = ""
	pt=0
	for i in range(len(basis)):
		if basis[i]:
			disp_string+=empty
		else:
			disp_string+=random_string[pt]
			pt+=1
	return disp_string

def get_complete_string(basis,random_string,password):
	disp_string = ""
	pt=0
	pp=0
	for i in range(len(basis)):
		if basis[i]:
			disp_string+=password[pp]
			pp+=1
		else:
			disp_string+=random_string[pt]
			pt+=1
	return disp_string