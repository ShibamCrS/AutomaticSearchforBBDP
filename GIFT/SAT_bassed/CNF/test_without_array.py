import time 
from GIFT import *
import subprocess
from itertools import *
class autometic_search:
	def __init__(self, cipher_name, sbox_list, block_size, number_of_sbox):
		self.__model_file = cipher_name + '.cvc'
		self.__model_w_init = cipher_name + 'init' + '.cvc'
		File_model = open(self.__model_file, "w")
		File_model.close()
		File_model_w_init = open(self.__model_w_init, "w")
		File_model_w_init.close()
		self.__sbox_object = Sbox(sbox_list)
		self.__block_size = block_size
		self.__ns = number_of_sbox
		
	def generate_In(self, C):
		temp = [ ]
		for i in range(0,64):
			temp.append('ASSERT X_0_%d = 0bin1;'%(i))		
		for c in C:
			temp[c] = 'ASSERT X_0_%d = 0bin0;'%(c)
		s = '\n'.join(temp) + '\n'			
		return (s)			
	def generate_Out(self, R, C):
		temp = [ ]
		for i in range(0,64):
			if(i == C[0]):
				temp.append('ASSERT X_%d_%d = 0bin1;'%(R,i))
			else:
				temp.append('ASSERT X_%d_%d = 0bin0;'%(R,i))
		s = '\n'.join(temp) + '\n'			
		return (s)		
		
	def get_balanced_bits(self, r):
		Present = CIPHER_MODEL(self.__sbox_object, self.__block_size, r, self.__ns)
		model = '\n'.join(Present.get_full_constraints() )
		query = '\n' + 'QUERY FALSE;'+'\n'#+'COUNTEREXAMPLE;'
		temp_model = model + query
		File_model = open(self.__model_file, "a")
		File_model.write(temp_model)
		File_model.close()
		balanced_bits = [ ]
		time_start = time.time()
		for i in range(0,64):
			S = []
			C = [ ]
			C.append(i)
			print (C)
			in_d = self.generate_In(C) 
			TM = []
			time_start_j = time.time()
			for j in range(0,64):	
				B = []
				B.append(j)
				d_j = in_d +'\n'+ self.generate_Out(r, B)
				model_update = model + '\n' + d_j
				model_update += query
				#print (d_j)
				File_model_w_init= open(self.__model_w_init, "w")
				File_model_w_init.write(model_update)
				File_model_w_init.close()
				stp_parameters = ["stp", "GIFTinit.cvc", "--cryptominisat", "--threads", "4"]
				R = subprocess.check_output(stp_parameters)
				#R = R.decode("utf-8")
				#R = R.encode('ascii','ignore')
				print (R)
				if(str(R)[2] == 'V'):
					print ("Balance i %d j %d"%(i , j))
					S.append(j)
					random = input("continue?")
				elif(str(R)[2] == 'I'):
					print ("Unknown i %d j %d"%(i , j))
			time_end_j = time.time()
			TM.append(str(time_end_j - time_start_j))
			balanced_bits.append(S)
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (balanced_bits)
		
	def check_with_const_col(self,r,C):
		Present = CIPHER_MODEL(self.__sbox_object, self.__block_size, r, self.__ns)
		model = '\n'.join(Present.get_full_constraints() )
		query = '\n' + 'QUERY FALSE;'+'\n'#+'COUNTEREXAMPLE;'
		temp_model = model + query
		File_model = open(self.__model_file, "a")
		File_model.write(temp_model)
		File_model.close()
		in_d = self.generate_In(C) 
		
		TM = []
		balanced_bits =[]
		time_start = time.time()
		for j in range(0,64):	
			B = []
			B.append(j)
			d_j = in_d +'\n'+ self.generate_Out(r, B)
			model_update = model + '\n' + d_j
			model_update += query
			#print (d_j)
			File_model_w_init= open(self.__model_w_init, "w")
			File_model_w_init.write(model_update)
			File_model_w_init.close()
			stp_parameters = ["stp", "GIFTinit.cvc", "--cryptominisat", "--threads", "4"]
			R = subprocess.check_output(stp_parameters)
			#R = R.decode("utf-8")
			#R = R.encode('ascii','ignore')
			print (R)
			if(str(R)[2] == 'V'):
				print ("Balance ", C ," j %d"%(j))
				balanced_bits.append(j)
				#random = input("continue?")
			elif(str(R)[2] == 'I'):
				print ("Unknown ", C ," j %d"%(j))
		time_end = time.time()
		print("Time used = " + str(time_end - time_start))
		return (balanced_bits)
def get_combination(t):
	res = []
	S = [x for x in range(16)]
	combinations_list = list(combinations(S,t))
	#print(combinations_list)
	
	for touple in combinations_list:
		C = [[] for x in range(3+t)]
		for i in range(4):
			C[i].append(i)
			C[i].append(touple[0])
		C[4].append
		res.append(C)
	return (res)
def get_row(t):
	C = []
	for i in range(4):
		C.append((4*t+i))
	return (C)
if __name__ == '__main__':
	sbox = [0x1, 0xa, 0x4, 0xc, 0x6, 0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe]
	cipher_name = "GIFT"
	block_size = 64
	number_of_sbox = 16
	A = autometic_search(cipher_name, sbox, block_size, number_of_sbox)
	"""
	temp = get_combination(2)
	for C in temp:
		print(C)
		res = A.check_with_const_col(9,C)
		print (res)
	"""
	for i in range(15,16):
		C = [0,1] #get_row(i)
		print(C)
		res = A.check_with_const_col(9,C)
		print (res)
	"""
	C = get_row(0)
	print(C)
	print (A.generate_In(C))
	print (A.generate_Out(9, C))
	#B = A.get_balanced_bits(10)
	#print(B)	
	"""	
