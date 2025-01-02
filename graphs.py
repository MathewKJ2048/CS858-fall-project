from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from shuffle_string import *
import numpy as np
import random
import math

ALPHABET = "0123456789ABCDEF"
PASSWORD = "DEADFEED"
MIN_ENTROPY = 32

# two plots - average number of transitions per character for N
# vary alphabet size and entropy - length is a dependent, so is N, so is total time

def rc(N):
	return random.randint(0,N-1), random.randint(0,N-1)

def get_val_atomic(N,length):
	i, j = rc(N)
	sum = 0
	for lo in range(length):
		ni, nj = rc(N)
		sum+=abs(ni-i)+abs(nj-j)
		i, j = ni, nj
	return sum

def count(basis):
	st = [""]
	for i in range(len(basis)):
		if not basis[i]:
			st.append("")
		else:
			st[len(st)-1] = st[len(st)-1]+"*"
	answer = [0]*len(basis)
	for s in st:
		answer[len(s)]+=1
	answer[0]=0
	return answer

def add(a1,a2):
	a = [0]*len(a1)
	for i in range(len(a1)):
		a[i]=a1[i]+a2[i]
	return a

	
def graph_SS_1():
	# use default values
	# generate multiple instances
	# in each instance, count number of consecutive sizes
	basis = get_shuffle_basis(PASSWORD,MIN_ENTROPY,ALPHABET)
	T = 100000
	answer = [0]*len(basis)
	for i in range(T):
		answer = add(answer,count(get_shuffle_basis(PASSWORD,MIN_ENTROPY,ALPHABET)))
	X_data = [i for i in range(len(answer))]
	plt.xlabel("size of consecutive password segments")
	plt.ylabel("percentage of segments")
	plt.title("distribution of segment sizes (password length=8, sample size="+str(len(answer)))
	sum=0
	for a in answer:
		sum+=a
	plt.plot(X_data,[d/sum for d in answer])
	plt.savefig("./SS1.png")

def graph_SS_1_5():
	lb = len(get_shuffle_basis(PASSWORD,MIN_ENTROPY,ALPHABET))
	# X is 
	# Y is password length -  8, 12, 16, 20, 24, 28
	X_d = [i for i in range(lb)]
	Y_d = [i for i in range(2,31,2)]
	X_data=[]
	Y_data=[]
	Z_data=[]
	for y in Y_d:
		X_data+=X_d
		Y_data+=[y]*len(X_d)
		pswd = random_string(ALPHABET, y)
		basis = get_shuffle_basis(pswd,MIN_ENTROPY,ALPHABET)
		T=1000
		answer = [0]*len(basis)
		for i in range(T):
			answer = add(answer,count(get_shuffle_basis(pswd,MIN_ENTROPY,ALPHABET)))
		print(answer)
		sum=0
		for a in answer:
			sum+=a
		Z_data+=[d/sum for d in answer]

	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.scatter3D(X_data, Y_data, Z_data);
	ax.set_xlabel("Size of consecutive password segments")
	ax.set_ylabel("password length")
	ax.set_zlabel("frequency")
	#
	plt.title("distribution of segment sizes, sample size="+str(lb))
	plt.savefig("./SS1_5.png")


def graph_SM_1():
	xpoints = [i for i in range(1,101)]
	ypoints = [get_val_atomic(math.ceil(math.sqrt(x)),10000)/10000 for x in xpoints]
	plt.xlabel("|Σ|")
	plt.ylabel("average number of transitions per character")
	plt.plot(xpoints, ypoints)
	# #
	plt.savefig("./SM1.png")

def graph_SM_2():
	xpoints = [i for i in range(1,11)]
	ypoints = [get_val_atomic(x,10000)/10000 for x in xpoints]
	plt.xlabel("N")
	plt.ylabel("average number of transitions per character")
	plt.plot(xpoints, ypoints)
	#
	plt.savefig("./SM2.png")

def graph_SM_3():
	# entropy = length*lb(alphabetsize)
	x_points = [128*i for i in range(1,8)]
	y_points = [i for i in range(2,129)]
	def z(x,y): # y is alphabetsize, x is entropy
		l = x/math.log2(y)
		N = math.ceil(math.sqrt(y))
		return l*get_val_atomic(N,1000)/1000

	X_data = []
	Y_data = []
	Z_data = []
	for y in y_points:
		Y_data+=[y]*len(x_points)
		X_data+=x_points
	for i in range(len(X_data)):
		Z_data.append(z(X_data[i],Y_data[i]))


	fig = plt.figure()
	ax = plt.axes(projection='3d')
	ax.scatter3D(X_data, Y_data, Z_data);
	ax.set_xlabel("Entropy")
	ax.set_ylabel("|Σ|")
	ax.set_zlabel("average number of transitions")
	#
	plt.title("variation of the number of state transitions")
	plt.savefig("./SM3.png")


def string_contains(sup,sub):
	p=0
	q=0
	while p<len(sup) and q<len(sub):
		if sub[q]==sup[p]:
			q+=1
		p+=1
	return q==len(sub)


def common_ncsub(sa, sb, all_ncsub=False):
	mem = {}
	def get_key(s1, s2):
		return s1+"-"+s2
	def lookup(s1,s2):
		k1 = get_key(s1,s2)
		k2 = get_key(s2,s1)
		if k1 in mem:
			return mem[k1]
		if k2 in mem:
			return mem[k2]
		return []
	def split_str(s1):
		return s1[0:-1], s1[len(s1)-1]
	def prefix(s2,x):
		i = s2.rfind(x)
		return s2[0:i]
	def append_to_list(li, x):
		l = []
		for t in li:
			l.append(t+x)
		return l
	def ec(s1, s2):
		ml = lookup(s1,s2)
		if len(ml)!=0:
			return ml
		k = get_key(s1,s2)
		answer = [""]
		if not (len(s1)==0 or len(s2)==0):
			s_, x = split_str(s1)
			answer_without_x = ec(s_,s2)
			if x not in s2:
				answer = answer_without_x
			else: # x in s2
				ps2 = prefix(s2,x)
				answer_with_x = append_to_list(ec(s_, ps2),x)
				if all_ncsub:
					answer = answer_with_x+answer_without_x
				else:
					if len(answer_with_x[0])>len(answer_without_x[0]):
						answer = answer_with_x
					elif len(answer_with_x[0])<len(answer_without_x[0]):
						answer = answer_without_x
					else:
						answer = answer_with_x+answer_without_x
		d = {}
		for a in answer:
			d[a]=""
		answer = list(d.keys())
		mem[k] = answer
		return answer
	return ec(sa, sb)




def get_cs(pwd):
	basis = get_shuffle_basis(pwd,MIN_ENTROPY,ALPHABET)
	rs = random_string(ALPHABET,len(basis)-len(pwd))
	return get_complete_string(basis,rs,pwd)

def convergence_list(n):
	oiew = random_string(ALPHABET,len(PASSWORD))
	possible = common_ncsub(get_cs(oiew),get_cs(oiew),all_ncsub=True)
	answer = []
	for i in range(n):
		answer.append(len(possible))
		cs = get_cs(oiew)
		nlist = []
		for k in possible:
			if string_contains(cs,k) and not k in nlist:
				nlist.append(k)
		possible = nlist
	return answer

def graph_SS_2(): # convergence using all
	N = 100
	n = 10
	avg = [0]*n
	for i in range(N):
		print(i)
		avg = add(avg,convergence_list(n))
	avg = [a/N for a in avg]
	X_data = [i+2 for i in range(n)]
	plt.xlabel("number of samples")
	plt.ylabel("average number of possible passwords")
	plt.yscale("log")
	plt.plot(X_data,avg)
	plt.title("password prediction from multiple samples")
	#
	plt.savefig("./SS2.png")



def graph_SS_3(): # freqiuecy
	# assume n instances captured
	# k instances of 'a'abs
	# X = k/(n*lb)
	# E[X] = 1/|sigma| if `a` occurs 0 times
	cto = {
	}
	for p in ALPHABET:
		cto[p]=0
	N = 100
	lb = len(get_shuffle_basis(PASSWORD,MIN_ENTROPY,ALPHABET))
	X_data = [i for i in range(1,N+1)]
	Y_data = []
	for i in range(N):
		cs = get_cs(PASSWORD)
		for ch in cs:
			cto[ch]+=1
		cto_ = {}
		for cpc in cto:
			cto_[cpc] = cto[cpc]/(X_data[i]*lb)
		Y_data.append(cto_)
	transform_data = {}
	for p in PASSWORD:
		transform_data[p]=[]
	transform_data["0"]=[]
	for ch in transform_data:
		transform_data[ch] = [Y_data[x-1][ch] for x in X_data]
	plt.xlabel("number of samples")
	plt.ylabel("frequency of occurance")
	for ch in transform_data:
		plt.plot(X_data,transform_data[ch],label=ch)
	plt.legend()
	#
	plt.title("frequency analysis of samples")
	plt.savefig("./SS3.png")
	
def double_common(g):
	pswd = random_string(ALPHABET,g)
	cs1 = get_cs(pswd)
	cs2 = get_cs(pswd)
	return len(common_ncsub(cs1,cs2,all_ncsub=False)[0])


def graph_SS_4():
	for p in range(4,32,8):
		lcs = len(get_cs(PASSWORD))
		dist = [0]*lcs
		N=100
		for i in range(N):
			dist[double_common(p)]+=1
		plt.xlabel("length of common non-contiguous substring")
		plt.ylabel("frequency (per "+str(N)+")")
		X_data = [i for i in range(lcs)]
		Y_data = [dist[x] for x in X_data]
		plt.plot(X_data,Y_data,label="password length:"+str(p))
	plt.legend()
	plt.title("distribution of the length of longest non-contiguous substring from 2 samples")
	#
	plt.savefig("./SS4.png")



# graph_SS_4()
# graph_SS_3()
# graph_SS_2()
# graph_SM_1()
# graph_SM_2()
# graph_SM_3()
# graph_SS_1()
# graph_SS_1_5()

print(common_ncsub("ACXAA","AAAX"))






