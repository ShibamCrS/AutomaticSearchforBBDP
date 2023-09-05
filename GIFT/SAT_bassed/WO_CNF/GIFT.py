from AssertSbox import *
class CIPHER_MODEL(object):
	def __init__(self, sbox_name, sbox_list, block_size, number_of_rounds, number_of_sbox):
		self.__sbox = AssertSbox(sbox_name, sbox_list, number_of_rounds, number_of_sbox)
		self.__sbox_size = self.__sbox.sbox_size
		self.__block_size = block_size
		self.__rounds = number_of_rounds
		self.__constraints = [ ]
		self.__number_of_sbox = number_of_sbox
		#variables_X0 [sbox] variables_X1 [Linear part] variables_X1' [sbox] variables_X2 ...
		self.__variables_X = self.get_variables_X()
		self.__a = self.__sbox.get_conditions()
		self.__constraints = self.__constraints + self.__a
		self.gen_constraints()

	def get_variables_X(self):
		X = [[0 for x in range(self.__block_size)] for z in range(self.__rounds+1)]
		for r in range(self.__rounds+1):
			for i in range(self.__block_size):
				temp = 'X_%d_%d' %(r,i)
				X[r][i] = temp
				temp1 = '%s:BITVECTOR(1);' %temp
				self.__constraints.append(temp1)
		return X
	def LinearLayer(self,input_variables):
		array = ["" for i in range(0,64)]
		for i in range(0,64):
			array[((i >> 4) << 2) + (((3*((i & 0xf)>>2) + (i & 3)) & 3) << 4) + (i & 3)] = input_variables[i]
		return array

	def gen_constraints(self):
		if self.__rounds == 1:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					in_vec.append(self.__variables_X[0][(self.__sbox_size*p)+i])
					out_vec.append(self.__variables_X[1][(self.__sbox_size*p)+i])
				temp = self.__sbox.get_constraints(in_vec,out_vec,0,p)
				self.__constraints.append(temp)
		else:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					in_vec.append(self.__variables_X[0][(self.__sbox_size*p)+i])
					out_vec.append(self.__variables_X[1][(self.__sbox_size*p)+i])
				temp = self.__sbox.get_constraints(in_vec,out_vec,0,p)
				self.__constraints.append(temp)
			for r in range(1, self.__rounds):
				shuffeled_variables = self.LinearLayer(self.__variables_X[r])
				for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					for i in range(self.__sbox_size):
						in_vec.append(shuffeled_variables[(self.__sbox_size*p)+i])
						out_vec.append(self.__variables_X[r+1][(self.__sbox_size*p)+i])
					temp = self.__sbox.get_constraints(in_vec,out_vec,r,p)
					self.__constraints.append(temp)
	def get_full_constraints(self):
		return self.__constraints

if __name__ == "__main__":
	sbox = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
	Present = CIPHER_MODEL('SBOX', sbox, 64, 9, 16)
	print ('\n'.join(Present.get_full_constraints() ) )	
