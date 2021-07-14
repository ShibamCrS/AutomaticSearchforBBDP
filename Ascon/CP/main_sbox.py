from sbox import *
def tobin(i):
	return bin(i)[2:].zfill(5)
def num_to_poly(L):
	P_list = []
	for l in L:
		#print (l)
		if (l == 0):
			P_list.append("1")
		else:
			l_vec = tobin(l)
			#print (l_vec)
			temp = ""
			for i in range(len(l_vec)):
				if(l_vec[i] == '1'):
					temp = temp + "x%d"%(i)
			P_list.append(temp)
	return (" + ".join(P_list))
def len_T(D):
	l = 0
	for k in D.keys():
		l = l + len(D[k])
	return l
if __name__ == '__main__':
	sbox_list = [0x4,0xb,0x1f,0x14,0x1a,0x15,0x9,0x2,0x1b,0x5,0x8,0x12,\
				0x1d,0x3,0x6,0x1c,0x1e,0x13,0x7,0xe,0x0,0xd,0x11,0x18,0x10,\
				0xc,0x1,0x19,0x16,0xa,0xf,0x17]
	print ("Sbox=>",sbox_list)
	sbox_object = Sbox(sbox_list)
	ANF  = sbox_object.ANF_bit_product_function()
	T = sbox_object.get_trails()
	print("num of valid division trails=",len_T(T))
	C_T = sbox_object.get_C_trails()
	
	print("\n************ANF of the SBox****************")
	for i in range(5):
		print (ANF[1 << i],"=>", num_to_poly(ANF[1 << i]))
	print ("*****************Division Trails ***********\n", sbox_object.get_trails())
	variables_X = []
	variables_Y = []
	for i in range(5):
		variables_X.append('%s_%d_%d_%d'%('X', 0, 1, i))
		variables_Y.append('%s_%d_%d_%d'%('Y', 0, 1, i))
	POS = sbox_object.pos
	#print (POS)
	s = sbox_object.get_sbox_constraints(variables_X, variables_Y)
	print ("*****************CNF***********************")
	print (s)
