from CNF import *
from Linear_layer import *
class CIPHER_MODEL(object):
	def __init__(self, block_size, number_of_rounds, number_of_sbox):
		self.__linear_layer = Linear_layer()
		self.__block_size = block_size
		self.__sbox_size = 5
		self.__number_of_sbox = number_of_sbox
		self.__rounds = number_of_rounds
		
		self.__nrow = self.__sbox_size	
		self.__ncol = number_of_sbox
		
		self.__variables = []
		self.__declare = [ ]
		self.__constraints = [ ]
		
		self.gen_variables_X()
		self.gen_variables_Y()
		self.gen_aux_variables("U")
		self.gen_aux_variables("V")
		self.gen_aux_variables("W")
		
		self.gen_constraints()
		
	def gen_variables_X(self):
		for r in range(self.__rounds+1):
			temp = 'array[0..%d,0..%d] of var bool : round_%d_X;'%(
				self.__nrow-1,self.__ncol-1,r)
			self.__variables.append(temp)
	def gen_variables_Y(self):
		for r in range(self.__rounds):
			temp = 'array[0..%d,0..%d] of var bool : round_%d_Y;'%(
				self.__nrow-1,self.__ncol-1,r)
			self.__variables.append(temp)
	def gen_aux_variables(self,x):
		for r in range(self.__rounds):
			temp = 'array[0..%d,0..%d] of var bool : round_%d_%s;'%(
				self.__nrow-1,self.__ncol-1,r,x)
			self.__variables.append(temp)
			
	def gen_constraints(self):
		sbox_main = sbox_CNF1 +"\n" + sbox_CNF2
		self.__declare.append(sbox_main)
		F_main = F_CNF1 + "\n" + F_CNF2
		self.__declare.append(F_main)
		for r in range(0, self.__rounds):
			for p in range(self.__number_of_sbox):
				in_vec = []
				out_vec = []
				temp = 'constraint sbox('
				for i in range(self.__sbox_size):
					in_vec.append ( 'round_%d_X[%d,%d]'%(r, i, p))
					out_vec.append ('round_%d_Y[%d,%d]'%(r, i, p))
				temp = temp + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
				self.__constraints.append(temp)
			lin_layer_number = r
			temp = self.__linear_layer.gen_constraints_linear_layer(lin_layer_number)
			self.__constraints.append(temp)
					
	def get_full_constraints(self):
		l = ['\n']
		return self.__variables + self.__declare + self.__constraints + l

if __name__ == "__main__":
	sbox_list = [0x4,0xb,0x1f,0x14,0x1a,0x15,0x9,0x2,0x1b,0x5,0x8,0x12,\
				0x1d,0x3,0x6,0x1c,0x1e,0x13,0x7,0xe,0x0,0xd,0x11,0x18,0x10,\
				0xc,0x1,0x19,0x16,0xa,0xf,0x17]
	#sbox_object = Sbox(sbox_list)
	#print (sbox_object.sbox)
	number_of_rounds = 2
	#Other_F_object = FUN(3)
	Ascon = CIPHER_MODEL(320, number_of_rounds, 64)
	print ('\n'.join(Ascon.get_full_constraints() ) )	
