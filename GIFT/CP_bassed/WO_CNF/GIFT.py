from sbox import *
class CIPHER_MODEL(object):
	def __init__(self, sbox_object, block_size, number_of_rounds, number_of_sbox):
		self.__sbox = sbox_object
		self.__block_size = block_size
		self.__P  = self.gen_permutation()
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
			temp = 'array[0..%d] of var bool : round_%d_X;'%(self.__block_size-1,r)
			self.__declare.append(temp)
	
	def gen_permutation(self):
		variable = [x for x in range(64)]
		array = [0 for i in range(0,64)]
		for i in range(0,64):
			array[((i >> 4) << 2) + (((3*((i & 0xf)>>2) + (i & 3)) & 3) << 4) + (i & 3)] = variable[i]
		return array
		
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
					in_vec.append ( 'round_%d_X[%d]'%(0,(self.__sbox_size*p)+i) )
					out_vec.append ( 'round_%d_X[%d]'%(1,(self.__sbox_size*p)+i) )
				temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
				self.__constraints.append(temp1)
		else:
			for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					temp1 = 'constraint sbox('
					for i in range(self.__sbox_size):
						in_vec.append ( 'round_%d_X[%d]'%(0,(self.__sbox_size*p)+i) )
						out_vec.append ( 'round_%d_X[%d]'%(1,(self.__sbox_size*p)+i) )
					temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
					self.__constraints.append(temp1)
			for r in range(1, self.__rounds):
				for p in range(self.__number_of_sbox):
					in_vec = []
					out_vec = []
					temp1 = 'constraint sbox('
					for i in range(self.__sbox_size):
						in_vec.append ( 'round_%d_X[%d]'%(r,self.__P[(self.__sbox_size*p)+i]) )
						out_vec.append ( 'round_%d_X[%d]'%(r+1,(self.__sbox_size*p)+i) )
					temp1 = temp1 + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
					self.__constraints.append(temp1)

	def get_full_constraints(self):
		l = ['\n'] 
		return self.__declare + self.__constraints + l

def MatrixPrint(M):
	for i in range(len(M)):
		print (M[i])
	print("\n")
if __name__ == "__main__":
	sbox_list = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
	sbox_object = Sbox(sbox_list)
	Present = CIPHER_MODEL( sbox_object, 64, 2, 16)
	print ('\n'.join(Present.get_full_constraints() ) )	
