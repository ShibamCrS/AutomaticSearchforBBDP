import pymzn
from itertools import *
import time 
from GIFT import *
class autometic_search:
	def __init__(self, cipher_name, sbox_list, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.mzn'
		self.__model_data = cipher_name + '.dzn'
		self.__result = cipher_name
		File_model = open(self.__model_file, "w")
		File_model.close()
		self.__sbox_object = Sbox(sbox_list)
		self.__block_size = block_size
		self.__ns = number_of_sbox
	
	def generate_In(self, C):
		d = 'round_0_X = array1d(0..63, ['
		temp = [ ]
		for i in range(0,64):
			temp.append('true')
		for c in C:
			temp[c] = 'false'
		d = d + ','.join(temp) + '] );'				
		return (d)			
	def generate_Out(self, R, C):
		d = 'round_%d_X = array1d(0..63, ['%(R)
		temp = [ ]
		for i in range(0,64):
			temp.append('false')
		for c in C:
			temp[c] = 'true'
		d = d + ','.join(temp) + '] );'				
		return (d)	
	
	def get_balanced_bits(self, r):
		Present = CIPHER_MODEL(self.__sbox_object, self.__block_size, r, self.__ns)
		model = '\n'.join(Present.get_full_constraints() )
		temp_model = model + 'solve satisfy;' #self.restart()
		
		print(temp_model)
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		
		
		time_start = time.time()
		balanced_bits = []
		for i in range(0,64):
			C = []
			C.append(i)
			print(C)
			in_d = self.generate_In(C)
			S = []		
			for j in range(0,64):
				B = []
				B.append(j)
				print(B)
				d_j = in_d +'\n'+ self.generate_Out(r, B)
				print (d_j)
				R = pymzn.minizinc(temp_model, data = d_j, solver=pymzn.Chuffed(solver_id='chuffed'), parallel ='4')
				if(str(R) == 'UNSATISFIABLE'):
					print ("Balance ", C ,"->>", B)
					balanced_bits.append(j)
				else:
					print ("Unknown ", C ,"->>", B)
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (balanced_bits)
	def check_with_const_col(self,r,C):
		Present = CIPHER_MODEL(self.__sbox_object, self.__block_size, r, self.__ns)
		model = '\n'.join(Present.get_full_constraints() )
		temp_model = model + 'solve satisfy;' #self.restart()
		
		print(temp_model)
		File_model = open(self.__model_file, "w")
		File_model.write(temp_model)
		File_model.close()
		
		in_d = self.generate_In(C) 
	
		balanced_bits =[]
		time_start = time.time()
		for j in range(0,64):
				B = []
				B.append(j)
				print(B)
				d_j = in_d +'\n'+ self.generate_Out(r, B)
				print (d_j)
				R = pymzn.minizinc(temp_model, data = d_j, solver=pymzn.Chuffed(solver_id='chuffed'), parallel ='4')
				if(str(R) == 'UNSATISFIABLE'):
					print ("Balance ", C ,"->>", B)
					balanced_bits.append(j)
				else:
					print ("Unknown ", C ,"->>", B)
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (balanced_bits)
def get_row(t):
	C = []
	for i in range(4):
		C.append((4*t+i))
	return (C)
if __name__ == '__main__':
	sbox = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
	cipher_name = "Present"
	block_size = 64
	number_of_sbox = 16
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	
	for i in range(15,16):
		C = [0] #get_row(i)
		print(C)
		res = A.check_with_const_col(9,C)
		print (res)
	
	
	"""
	C = get_row(0)
	print(C)
	print (A.generate_In(C))
	print (A.generate_Out(9, C))
	"""
	#B = A.get_balanced_bits(10)
	#print(B)	
