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
			temp = 'array[0..%d,0..%d] of var bool : round_%d_X;'%(
				self.__nrow-1,self.__row_size-1,r)
			self.__declare.append(temp)
			
	def gen_constraints(self):
		X = [ ]
		Y = [ ]
		for i in range(self.__sbox_size):
			X.append('x%d'%(i))
			Y.append('y%d'%(i))
		sbox_main = 'predicate sbox('
		temp = [ ]
		for i in range(self.__sbox_size):
			temp.append('var bool:%s'%(X[i]))
		for i in range(self.__sbox_size):
			temp.append('var bool:%s'%(Y[i]))
		sbox_main = 'predicate sbox(' + ', '.join(temp) + ' ) =\n'
		sbox_main = sbox_main +(
					self.__sbox.get_sbox_constraints(X,Y) 
					+ ';' + '\n')
		self.__declare.append(sbox_main)
		
		if self.__rounds == 1:
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				temp1 = 'constraint sbox('
				for i in range(self.__sbox_size):
					j = self.__sbox_size - 1 -i
					in_vec.append ( 'round_%d_X[%d,%d]'%(0, j, p))
					out_vec.append ('round_%d_X[%d,%d]'%(1, j, p))
				temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
				self.__constraints.append(temp1)
		else:
			for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					temp1 = 'constraint sbox('
					for i in range(self.__sbox_size):
						j = self.__sbox_size - 1 -i
						in_vec.append ( 'round_%d_X[%d,%d]'%(0, j, p))
						out_vec.append ('round_%d_X[%d,%d]'%(1, j, p))
					temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
					self.__constraints.append(temp1)
			for r in range(1, self.__rounds):
				for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					temp1 = 'constraint sbox('
					for i in range(self.__sbox_size):
						j = self.__sbox_size - 1 -i
						in_vec.append ( 'round_%d_X[%d,%d]'%(r, j, self.__P[j][p]))
						out_vec.append ('round_%d_X[%d,%d]'%(r+1, j, p))
					temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
					self.__constraints.append(temp1)

	def get_full_constraints(self):
		l = ['\n']
		return self.__declare + self.__constraints + l

if __name__ == "__main__":
	sbox_list = [6, 0, 11, 5, 9, 4, 2, 7, 14, 8, 15, 1, 12, 13, 3, 10]
	KNOT = CIPHER_MODEL( sbox_list, 32, 2, 8)
	print ('\n'.join(KNOT.get_full_constraints() ) )	
