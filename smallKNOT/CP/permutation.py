class Permutation:
	def __init__(self, block_size):
		self.__block_size = block_size
		self.__row_size = block_size >> 2
		
		self.__rotation = self.set_rotation()
		
	def set_rotation(self):
		if(self.__block_size == 256):
			rotation = [0,1,8,25]
		elif(self.__block_size == 384):
			rotation = [0,1,8,55]
		elif(self.__block_size == 512):
			rotation = [0,1,16,25]
		elif(self.__block_size == 32):
			rotation = [0,1,5,7]
		elif(self.__block_size == 8):
		    rotation = [0,1,0,1] 
		elif(self.__block_size == 8):
		    rotation = [0,0,0,0]
		else:
			print("Invalid_block_size")
			exit();
		return rotation
	def gen_permutation(self):
		states = [[x for x in range(self.__row_size)] for i in range(4)]
		output_states = [[] for i in range(4)]
		output_states[0] = states[0]
		for row in range(1,4):
			temp = states[row][self.__rotation[row]:] + states[row][:self.__rotation[row]]
			output_states[row] = temp
		return output_states
