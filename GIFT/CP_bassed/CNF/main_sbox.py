from sbox import *

if __name__ == '__main__':
	sbox_list = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
	sbox_object = Sbox(sbox_list)
	ANF  = sbox_object.ANF_bit_product_function()
	T = sbox_object.get_trails()
	print(T)
	C_T = sbox_object.get_C_trails()
	print (C_T)
	for i in range(4):
		print (ANF[1 << i])
	
	print (sbox_object.get_trails())
	variables_X = []
	variables_Y = []
	for i in range(4):
		variables_X.append('%s_%d_%d_%d'%('X', 0, 1, i))
		variables_Y.append('%s_%d_%d_%d'%('Y', 0, 1, i))
	SOP = sbox_object.sop
	print (SOP)
	s = sbox_object.get_sbox_constraints(variables_X, variables_Y)
	print (s)
	
	POS = sbox_object.pos
	print (POS)
	s = sbox_object.get_sbox_constraints1(variables_X, variables_Y)
	print (s)
	"""
	sbox_object = Sbox(sbox_list)
	T = sbox_object.get_trails()
	print (T)
	SOP = sbox_object.get_SOP()
	round_number = 0
	after_sbox = 0
	for r in range(3):
		variables_X = []
		variables_Y = []
		for i in range(4):
			variables_X.append('%s_%d_%d'%('X',r, i))
			variables_Y.append('%s_%d_%d'%('Y',r, i))
		fun = [ ] 
		print ("len of SOP: ", len(SOP))
		for minterm in SOP:
			temp = [ ]
			for i in range(4):
				if(minterm[i] == '1'):
					temp.append (variables_X[i])
				elif(minterm[i] == '0'):
					temp.append ('('+'not '+variables_X[i]+')')
			for i in range(4,8):
				if(minterm[i] == '1'):
					temp.append (variables_Y[i-4])
				elif(minterm[i] == '0'):
					temp.append ('('+'not '+variables_Y[i-4]+')')
			
		"""
		
    		
    			
