import pymzn
from itertools import *
import time 
from Rectangle import *
import sys

class autometic_search:
	def __init__(self, cipher_name, sbox_list, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.mzn'
		self.__model_data = cipher_name + '.dzn'
		self.__result = cipher_name
		File_model = open(self.__model_file, "w")
		File_model.close()
		self.__sbox_list = sbox_list
		self.__block_size = block_size
		self.__ns = number_of_sbox
	
	def generate_In(self, C):
		d = 'round_0_X = array2d(0..3, 0..%d, [|'%(self.__ns - 1)
		temp1 = [ ]
		temp2 = [ ]
		for row in range(0,4):
			temp = [ ]
			for col in range(0,self.__ns):
					temp.append('true')
			temp2.append(temp)
		for c in C:
			row = c[0]
			col = c[1]
			temp2[row][col] = 'false'
		for row in range(0,4):
			temp1.append(', '.join(temp2[row]))
		d = d + '| '.join(temp1) + '|] );'				
		return (d)			
	def generate_Out(self, R, C):
		d = 'round_%d_X = array2d(0..3, 0..%d, [|'%(R,self.__ns - 1)
		temp1 = [ ]
		for row in range(0,4):
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
		Rectangle = CIPHER_MODEL(self.__sbox_list, self.__block_size, Round, self.__ns)
		model = '\n'.join(Rectangle.get_full_constraints() )
		temp_model = model + 'solve satisfy;' 
		
		
		#print(temp_model)
		
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		
		
		time_start = time.time()
		input_property = self.generate_In(C) 
		result =[]
		for out_row in range(0,4):
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
					print ("Input=> ", C, " Output=> ",B, "***Unknown***")
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (result)

if __name__ == '__main__':
	sbox = [0x6,0x5,0xC,0xA,0x1,0xE,0x7,0x9,0xB,0x0,0x3,0xD,0x8,0xF,0x4,0x2]
	cipher_name = "Rectangle"
	
	n = len(sys.argv)
	block_size = int(sys.argv[1])
	number_of_sbox = block_size >> 2
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	number_of_rounds = int(sys.argv[2])
	#C = [[0, 0], [1, 0], [2, 0], [3, 0]]
	C = [ ]
	for i in range(3,n):
		st = sys.argv[i]
		c_temp = [j for j in st.split(',')]
		c = [int(j) for j in c_temp]
		C.append(c)
	# = [[3,0]] #sys.argv[3]
	print (C)
	res = A.get_balanced_bits(number_of_rounds,C)
	print (res)
	print ("Number of balanced bits with input ", C, " = ",len(res))
