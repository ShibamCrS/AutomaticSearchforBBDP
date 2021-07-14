import pymzn
from itertools import *
import time 
from KNOT import *
from permutation import *
import sys

def tobin(x,n=4) :
	xbin = []
	for i in range(n-1,-1,-1) :
		xbin.append((x >> i) & 1 )
	return xbin
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
		temp2 = [ ]
		for row in range(0,4):
			temp = [ ]
			for col in range(0,self.__ns):
					temp.append('false')
			temp2.append(temp)
		for c in C:
			row = c[0]
			col = c[1]
			temp2[row][col] = 'true'
		for row in range(0,4):
			temp1.append(', '.join(temp2[row]))
		d = d + '| '.join(temp1) + '|] );'				
		return (d)		
	
	def check_with_const_col(self,Round,L):
		KNOT= CIPHER_MODEL(self.__sbox_list, self.__block_size, Round, self.__ns)
		model = '\n'.join(KNOT.get_full_constraints() )
		temp_model = model + 'solve satisfy;' 
		
		
		#print(temp_model)
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		
		time_start = time.time()
		#B=[[i for i in range(self.__ns)] for j in range(4)]
		self.__permutation = Permutation(self.__block_size)
		self.__P  = self.__permutation.gen_permutation()
		states = self.__P
		print (states)
		
		balanced = dict()	
		for in_row in range(0,1):
			for i in range(0,self.__ns):
				C = []
				C1 = []
				C1.append(in_row)
				C1.append(i)
				C.append(C1)
				input_property = self.generate_In(C) 
				balanced[tuple(C1)] = dict()
				for col in range(0,self.__ns):
					print ("col = ",col)
					balanced[tuple(C1)][col] = []
					T = dict()
					for l in L:
						T[l] = []
						Flag = True
						l_vec = tobin(l)
						B = []
						for out_row in range(0,4):
							j = 3 - out_row
							if l_vec[j] == 1:
								B1 = []
								B1.append(out_row)
								B1.append(states[out_row][col])
								B.append(B1)
						print("l=>",l_vec,"B",B)
						input_data = input_property +'\n'+ self.generate_Out(Round, B)
						R = pymzn.minizinc(temp_model, data = input_data, solver=pymzn.Chuffed(solver_id='chuffed'), parallel ='4')
						
						if(str(R) == 'UNSATISFIABLE'):
							print ("Balance l=>",l,"l_vec=>",l_vec, C, "=>",B)
							C = input("continue?",)
							T[l].append(B)
						else:
							print ("Unknown ",l,"l_vec=>",l_vec, C, "=>",B)
							
					balanced[tuple(C1)][col].append(T)
				print (balanced[tuple(C1)])
		time_end = time.time()	
		print("Time used = " + str(time_end - time_start))		
		return (balanced)
if __name__ == '__main__':
	sbox = [0x4,0x0,0xA,0x7,0xB,0xE,0x1,0xD,0x9,0xF,0x6,0x8,0x5,0x2,0xC,0x3]
	cipher_name = "KNOT"
	
	n = len(sys.argv)
	block_size = int(sys.argv[1])
	number_of_sbox = block_size >> 2
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	number_of_rounds = int(sys.argv[2])
	for i in range(3,n):
		st = sys.argv[i]
		c_temp = [j for j in st.split(',')]
		Output_bit_combinations = [int(j) for j in c_temp]
	print (Output_bit_combinations)
	res = A.check_with_const_col(number_of_rounds, Output_bit_combinations) 
	print (res)
