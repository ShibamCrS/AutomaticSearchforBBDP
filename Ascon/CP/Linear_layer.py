#from function_to_POS import *
class Linear_layer:
	def __init__(self):
		self.size = 3
		self.nrow = 5
		self.ncol = 64

	def gen_P(self,rotation):
		states = [x for x in range(self.ncol)]
		output_states = states[-rotation:]+states[:-rotation]
		return (output_states)
		
	def gen_row_constraints_copy(self, row_number,round_number):
		C = []
		for col in range(self.ncol):
			in_vec = []
			out_vec = []
			temp = 'constraint F('
			in_vec.append('round_%d_Y[%d,%d]'%(round_number,row_number,col))
			out_vec.append('round_%d_U[%d,%d]'%(round_number,row_number,col))
			out_vec.append('round_%d_V[%d,%d]'%(round_number,row_number,col))
			out_vec.append('round_%d_W[%d,%d]'%(round_number,row_number,col))
			temp = temp + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
			C.append(temp)
		constraints = "\n".join(C)
		return (constraints)
	def gen_row_constraints_xor(self, row_number, rotation,round_number):
		C = []
		r1 = rotation[0]
		r2 = rotation[1]
		P1 = self.gen_P(r1)
		P2 = self.gen_P(r2)
		next_round = round_number + 1
		for col in range(self.ncol):
			in_vec = []
			out_vec = []
			temp = 'constraint F('
			in_vec.append('round_%d_X[%d,%d]'%(next_round,row_number,col))
			out_vec.append('round_%d_U[%d,%d]'%(round_number,row_number,col))
			out_vec.append('round_%d_V[%d,%d]'%(round_number,row_number,P1[col]))
			out_vec.append('round_%d_W[%d,%d]'%(round_number,row_number,P2[col]))
			temp = temp + ', '.join(in_vec) + ',  ' +', '.join(out_vec) + ');'
			C.append(temp)
		constraints = "\n".join(C)
		return (constraints)
		
	def gen_constraints_linear_layer(self,round_number):
		rotation = [[19,28],[61,39],[1,6],[10,17],[7,41]]
		constraints_list = []
		for row_number in range(self.nrow):
			C = self.gen_row_constraints_copy(row_number,round_number)
			constraints_list.append(C)
		for row_number in range(self.nrow):
			C = self.gen_row_constraints_xor(row_number, rotation[row_number],round_number)
			constraints_list.append(C)
		constraints = "\n".join(constraints_list)
		return (constraints)
if __name__ == "__main__":
	L = Linear_layer()
	print(L.gen_P(10))
	print (L.gen_constraints_linear_layer(0))
