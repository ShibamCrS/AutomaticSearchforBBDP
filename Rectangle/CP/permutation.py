class Permutation:
	def __init__(self, block_size):
		self.__block_size = block_size
		self.__row_size = block_size >> 2
		
		self.__rotation = rotation = [0,1,12,13]
		
	def gen_permutation(self):
		states = [[x for x in range(self.__row_size)] for i in range(4)]
		output_states = [[] for i in range(4)]
		output_states[0] = states[0]
		for row in range(1,4):
			temp = states[row][self.__rotation[row]:] + states[row][:self.__rotation[row]]
			output_states[row] = temp
		return output_states
