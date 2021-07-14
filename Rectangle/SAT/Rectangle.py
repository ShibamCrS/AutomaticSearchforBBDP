from sbox import *
from permutation import *
class CIPHER_MODEL(object):
	def __init__(self, sbox_list, block_size, number_of_rounds, number_of_sbox):
		self.__sbox = Sbox(sbox_list)
		self.__sbox_size = self.__sbox.size	
		
		self.__block_size = block_size
		self.__permutation = Permutation(self.__block_size)
		self.__P  = self.__permutation.gen_permutation()
		#print (self.__P)
		
		self.__rounds = number_of_rounds
		self.__constraints = [ ]
		self.__number_of_sbox = number_of_sbox
		self.__declare = [ ]
		self.__row_size = block_size >> 2
		self.__nrow = int(self.__block_size/self.__row_size)
		self.gen_variables_X()
		self.gen_constraints()
			
	def gen_variables_X(self):
		for r in range(self.__rounds+1):
			for row in range(self.__nrow):
				for i in range(self.__row_size):
					temp = 'X_%d_%d_%d : BITVECTOR(1);'%(r,row,i)
					self.__declare.append(temp)
	def gen_constraints(self):
		if self.__rounds == 1:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					j = self.__sbox_size - 1 -i
					in_vec.append  ('X_%d_%d_%d'%(0, j, p))
					out_vec.append ('X_%d_%d_%d'%(1, j, p))	
				temp1 = self.__sbox.get_sbox_constraints(in_vec, out_vec)
				self.__constraints.append(temp1)
		else:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				for i in range(self.__sbox_size):
					j = self.__sbox_size - 1 -i
					in_vec.append  ('X_%d_%d_%d'%(0, j, p))
					out_vec.append ('X_%d_%d_%d'%(1, j, p))	
				temp1 = self.__sbox.get_sbox_constraints(in_vec, out_vec)
				self.__constraints.append(temp1)
			for r in range(1, self.__rounds):
				for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					for i in range(self.__sbox_size):
						j = self.__sbox_size - 1 -i
						in_vec.append ( 'X_%d_%d_%d'%(r, j, self.__P[j][p]))
						out_vec.append ('X_%d_%d_%d'%(r+1, j, p))
					temp1 = self.__sbox.get_sbox_constraints(in_vec, out_vec)
					self.__constraints.append(temp1)
	def get_full_constraints(self):
		l = ['\n']
		return self.__declare + self.__constraints + l

def MatrixPrint(M):
	for i in range(len(M)):
		print (M[i])
	print("\n")
if __name__ == "__main__":
	sbox_list = [0x6,0x5,0xC,0xA,0x1,0xE,0x7,0x9,0xB,0x0,0x3,0xD,0x8,0xF,0x4,0x2]
	Rectangle = CIPHER_MODEL( sbox_list, 64, 9, 16)
	print ('\n'.join(Rectangle.get_full_constraints() ) )	
