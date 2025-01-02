import random


def get_choice_length(entropy, PASSWORD):
	# entropy = pl*log2(cl)
	# cl = 2^(entropy/pl)
	return int(2**(entropy/len(PASSWORD)))
	
def get_choice_object(PASSWORD, choice_length, ALPHABET):
	ALP = "".join(random.sample(ALPHABET,choice_length))
	co = {}
	for i in range(len(ALP)):
		co[str(i)] = ALP[i]
	return co
	
def get_disp_string_IC(co):
	disp = ""
	for x in co:
		disp+=(co[x]+"<-"+x+" ")
	return disp


