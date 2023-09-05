import pymzn
from itertools import *
import time 
from Present import *
class autometic_search:
	def __init__(self, cipher_name, sbox_list, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.mzn'
		self.__model_data = cipher_name + '.dzn'
		File_model = open(self.__model_file, "w")
		File_model.close()
		self.__sbox_object = Sbox(sbox_list)
		self.__block_size = block_size
		self.__ns = number_of_sbox
	
	def generate_Out_j(self,j):
		Out_j = [ ]
		for t in range(self.__block_size):
			if (t != j):
				Out_j.append('false')
			else:
				Out_j.append('true')
		return (Out_j)
	def restart(self):
		S = ':: restart_geometric(2,100)'
		S = S +'\n'
		return (S)
	def search_strategy(self,r):
		a = [ ]
		S = ':: seq_search(['+'\n'
		for i in range(1,r):
			a.append('\t\t\tbool_search(round_%d_X, first_fail, indomain_random)'%(i))
		S = S + ',\n'.join(a) + '])'
		S = S + '\n'
		return (S)	
	def get_balanced_bits(self, r, set_of_constant_bits):
		Present = CIPHER_MODEL(self.__sbox_object, self.__block_size, r, self.__ns)
		model = '\n'.join(Present.get_full_constraints() )
		
		C = set_of_constant_bits
		In = [ ]
		for i in range(self.__block_size):
			if i not in C:
				In.append('true')
			else:
				In.append('false')
		d = 'round_0_X = array1d(0..63, [' + ', '.join(In) + ']);' 
		balanced_bits = [ ]
		time_start = time.time()
		#temp_model = model + self.search_strategy(r)
		temp_model = model + 'solve satisfy;'
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		print (temp_model)
		for j in range(self.__block_size-1,-1,-1):
			Out_j = self.generate_Out_j(j)
			d_j = d + '\n'+ 'round_%d_X = array1d(0..63, ['%(r) + ', '.join(Out_j) + ']);'
			print (d_j)
			File_data = open(self.__model_data, "w")
			File_data.write(d_j)
			File_data.close()
			R = pymzn.minizinc(temp_model, data = d_j, solver = pymzn.Chuffed(solver_id='chuffed'))
			print (R)
			if(str(R) == 'UNSATISFIABLE'):
				print ("Balance %d"%(j))
				balanced_bits.append(j)
				
			else:
				print ("Unknown %d"%(j))
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (balanced_bits)
if __name__ == '__main__':
	sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
	cipher_name = "Present"
	block_size = 64
	number_of_sbox = 16
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	C = [60, 61, 62, 63]
	B = A.get_balanced_bits(9,C)
	print(B)
		
