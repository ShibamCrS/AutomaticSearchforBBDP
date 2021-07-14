from sbox import *

if __name__ == '__main__':
	sbox_list = [0x4,0xb,0x1f,0x14,0x1a,0x15,0x9,0x2,0x1b,0x5,0x8,0x12,\
				0x1d,0x3,0x6,0x1c,0x1e,0x13,0x7,0xe,0x0,0xd,0x11,0x18,0x10,\
				0xc,0x1,0x19,0x16,0xa,0xf,0x17]
	print (sbox_list)
	sbox_object = Sbox(sbox_list)
	ANF  = sbox_object.ANF_bit_product_function()
	T = sbox_object.get_trails()
	print(T)
	C_T = sbox_object.get_C_trails()
	print (C_T)
	for i in range(5):
		print (ANF[1 << i])
	print (sbox_object.get_trails())
	variables_X = []
	variables_Y = []
	for i in range(5):
		variables_X.append('%s_%d_%d_%d'%('X', 0, 1, i))
		variables_Y.append('%s_%d_%d_%d'%('Y', 0, 1, i))
	POS = sbox_object.pos
	print (POS)
	s = sbox_object.get_sbox_constraints_CNF(variables_X, variables_Y)
	print (s)
