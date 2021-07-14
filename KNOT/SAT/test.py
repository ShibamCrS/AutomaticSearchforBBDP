import time 
from KNOT import *
import subprocess
import sys

class autometic_search:
	def __init__(self, cipher_name, sbox_list, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.cvc'
		self.__model_w_init = cipher_name + 'init' + '.cvc'
		File_model = open(self.__model_file, "w")
		File_model.close()
		File_model_w_init = open(self.__model_w_init, "w")
		File_model_w_init.close()
		self.__sbox_list = sbox_list
		self.__block_size = block_size
		self.__ns = number_of_sbox
		
	def generate_In(self, C):
		temp = [ ]
		for row in range(0,4):
			for col in range(0,self.__ns):
				temp.append('ASSERT X_0_%d_%d = 0bin1;'%(row,col))		
		for c in C:
			row = c[0]
			col = c[1]
			temp[row*self.__ns + col] = 'ASSERT X_0_%d_%d = 0bin0;'%(row,col)
		s = '\n'.join(temp) + '\n'			
		return (s)		
	def generate_Out(self, R, C):
		temp = [ ]
		for row in range(0,4):
			for col in range(0,self.__ns):
				if(row == C[0] and col == C[1]):
					temp.append('ASSERT X_%d_%d_%d = 0bin1;'%(R,row,col))
				else:
					temp.append('ASSERT X_%d_%d_%d = 0bin0;'%(R,row,col))
		s = '\n'.join(temp) + '\n'			
		return (s)		
		
	def get_balanced_bits(self,Round,C):
		KNOT = CIPHER_MODEL(self.__sbox_list, self.__block_size, Round, self.__ns)
		model = '\n'.join(KNOT.get_full_constraints() )
		query = '\n' + 'QUERY FALSE;'
		temp_model = model + query
		File_model = open(self.__model_file, "a")
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
				input_data = input_property +'\n'+ self.generate_Out(Round, B)
				model_update = model + '\n' + input_data
				model_update += query
				File_model_w_init= open(self.__model_w_init, "w")
				File_model_w_init.write(model_update)
				File_model_w_init.close()
				stp_parameters = ["stp", "KNOTinit.cvc", "--cryptominisat", "--threads", "4"]
				R = subprocess.check_output(stp_parameters)
				print(R[:5])
				if(str(R)[2] == 'V'):
				    result.append(B)
				    print ("Input=> ", C, " Output=> ",B, "***Balanced***")
				elif(str(R)[2] == 'I'):
					print ("Input=> ", C, " Output=> ",B, "***Unknown***")
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (result)

if __name__ == '__main__':
	sbox = [0x4,0x0,0xA,0x7,0xB,0xE,0x1,0xD,0x9,0xF,0x6,0x8,0x5,0x2,0xC,0x3]
	cipher_name = "KNOT"
	
	n = len(sys.argv)
	block_size = int(sys.argv[1])
	number_of_sbox = block_size >> 2
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	number_of_rounds = int(sys.argv[2])
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
