import pymzn
from itertools import *
import time 
import sys
from ascon import *
from input_division_property import *

class autometic_search:
	def __init__(self, cipher_name, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.mzn'
		self.__model_data = cipher_name + '.dzn'
		self.__result = cipher_name
		File_model = open(self.__model_file, "w")
		File_model.close()
		self.__block_size = block_size
		self.__ns = number_of_sbox
	
	def generate_In(self, C):
		d = 'round_0_X = array2d(0..4, 0..63, [|'
		temp1 = [ ]
		temp2 = [ ]
		for row in range(0,5):
			temp = [ ]
			for col in range(0,self.__ns):
					temp.append('true')
			temp2.append(temp)
		for c in C:
			row = c[0]
			col = c[1]
			temp2[row][col] = 'false'
		for row in range(0,5):
			temp1.append(', '.join(temp2[row]))
		d = d + '| '.join(temp1) + '|] );'				
		return (d)			
	def generate_Out(self, R, C):
		d = 'round_%d_X = array2d(0..4, 0..63, [|'%(R)
		temp1 = [ ]
		for row in range(0,5):
			temp = [ ]
			for col in range(0,self.__ns):
				if(row == C[0] and col == C[1]):
					temp.append('true')
				else:
					temp.append('false')
			temp1.append(', '.join(temp))
		d = d + '| '.join(temp1) + '|] );'
		return (d)
		
	def get_balanced_bits(self,Round,C):
		ascon = CIPHER_MODEL(self.__block_size, Round, self.__ns)
		model = '\n'.join(ascon.get_full_constraints() )
		temp_model = model + 'solve satisfy;'
		
		#print(temp_model)
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		
		time_start = time.time()
		input_property = self.generate_In(C) 
		result =[]
		for out_row in range(0,5):
			for j in range(0,self.__ns):	
				B = []
				B.append(out_row)
				B.append(j)
				#print(B)
				input_data = input_property +'\n'+ self.generate_Out(Round, B)
				R = pymzn.minizinc(temp_model, data = input_data, solver=pymzn.Chuffed(solver_id='chuffed'), parallel ='4')
				if(str(R) == 'UNSATISFIABLE'):
				    result.append(B)
				    print ("Input=> ", C, " Output=> ",B, "***Balanced***")
				else:
					print ("Input=> ", " Output=> ",B, "***Unknown***")
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (result)
def get_col(t):
	C = []
	for i in range(0,5):
		temp = []
		temp.append(i)
		temp.append(t)
		C.append(temp)
	return (C)	
if __name__ == '__main__':
	cipher_name = "Ascon"
	sbox = [0x4,0xb,0x1f,0x14,0x1a,0x15,0x9,0x2,0x1b,0x5,0x8,0x12,\
				0x1d,0x3,0x6,0x1c,0x1e,0x13,0x7,0xe,0x0,0xd,0x11,0x18,0x10,\
				0xc,0x1,0x19,0x16,0xa,0xf,0x17]
	n = len(sys.argv)
	block_size = int(sys.argv[1])
	number_of_sbox = 64
	A = autometic_search(cipher_name, block_size, number_of_sbox)
	number_of_rounds = int(sys.argv[2])
	
	"""
	C = [ ]
	for i in range(3,64):
		C = C + get_col(i)
	C = C + [[1,2],[2,2],[3,2]]
	"""
	C = input_property #given in the file name input_division_property.py
	print (C, len(C))
	res = A.get_balanced_bits(number_of_rounds,C)
	print (res)
	print ("Number of balanced bits with input ", C, " = ",len(res))
