from sbox import *
class CIPHER_MODEL(object):
	def __init__(self, sbox_object, block_size, number_of_rounds, number_of_sbox):
		self.__sbox = sbox_object
		self.__block_size = block_size
		self.__P  = self.gen_permutation()
		#print (self.__P)
		self.__sbox_size = self.__sbox.size	
		self.__rounds = number_of_rounds
		self.__constraints = [ ]
		self.__number_of_sbox = number_of_sbox
		#variables_X0 [sbox] variables_Y0 [Linear part] variables_X1 ...
		self.__declare = [ ]
		self.gen_variables_X()
		self.gen_constraints()
			
	def gen_variables_X(self):
		for r in range(self.__rounds+1):
			for i in range(self.__block_size):
				temp = 'X_%d_%d : BITVECTOR(1);'%(r,i)
				self.__declare.append(temp)
	
	def gen_permutation(self):
		variable = [x for x in range(64)]
		array = [0 for i in range(0,64)]
		for i in range(0,64):
			array[((i >> 4) << 2) + (((3*((i & 0xf)>>2) + (i & 3)) & 3) << 4) + (i & 3)] = variable[i]
		return array
		
	def gen_constraints(self):	
		if self.__rounds == 1:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					in_vec.append  ('X_%d_%d'%(0, (self.__sbox_size*p)+i))
					out_vec.append ('X_%d_%d'%(1, (self.__sbox_size*p)+i))
				temp1 = self.__sbox.get_sbox_constraints_CNF(in_vec, out_vec)
				self.__constraints.append(temp1)
		else:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					in_vec.append  ('X_%d_%d'%(0, (self.__sbox_size*p)+i))
					out_vec.append ('X_%d_%d'%(1, (self.__sbox_size*p)+i))
				temp1 = self.__sbox.get_sbox_constraints_CNF(in_vec, out_vec)
				self.__constraints.append(temp1)
			for r in range(1, self.__rounds):
				for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					for i in range(self.__sbox_size):
						in_vec.append  ('X_%d_%d'%(r, self.__P[(self.__sbox_size*p)+i]))
						out_vec.append ('X_%d_%d'%(r+1, (self.__sbox_size*p)+i))
					temp1 = self.__sbox.get_sbox_constraints_CNF(in_vec, out_vec)
					self.__constraints.append(temp1)

	def get_full_constraints(self):
		l = ['\n'] 
		return self.__declare + self.__constraints + l


if __name__ == "__main__":
	sbox_list = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
	sbox_object = Sbox(sbox_list)
	GIFT = CIPHER_MODEL( sbox_object, 64, 9, 16)
	#print ('\n'.join(GIFT.get_full_constraints() ) )	
