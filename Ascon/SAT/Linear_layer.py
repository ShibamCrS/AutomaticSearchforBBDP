from function_to_POS import *
class Linear_layer:
	def __init__(self):
		self.size = 3
		self.nrow = 5
		self.ncol = 64
		self.F = FUN(self.size)
		
	def gen_P(self,rotation):
		states = [x for x in range(self.ncol)]
		output_states = states[-rotation:]+states[:-rotation]
		return (output_states)
		
	def gen_row_constraints(self, row_number, rotation,round_number):
		C = []
		r1 = rotation[0]
		r2 = rotation[1]
		P1 = self.gen_P(r1)
		P2 = self.gen_P(r2)
		next_round = round_number + 1
		for col in range(self.ncol):
			X = []
			Y = []
			X.append('Y_%d_%d_%d'%(round_number,row_number,col))
			Y.append('U_%d_%d_%d'%(round_number,row_number,col))
			Y.append('V_%d_%d_%d'%(round_number,row_number,col))
			Y.append('W_%d_%d_%d'%(round_number,row_number,col))
			C.append(self.F.get_constraints(X,Y))
			X1 = []
			Y1 = []
			
			X1.append('X_%d_%d_%d'%(next_round,row_number,col))
			Y1.append('U_%d_%d_%d'%(round_number,row_number,col))
			Y1.append('V_%d_%d_%d'%(round_number,row_number,P1[col]))
			Y1.append('W_%d_%d_%d'%(round_number,row_number,P2[col]))
			C.append(self.F.get_constraints(X1,Y1))
		constraints = "\n".join(C)
		return (constraints)
		
	def gen_constraints_linear_layer(self,round_number):
		rotation = [[19,28],[61,39],[1,6],[10,17],[7,41]]
		constraints_list = []
		for row_number in range(self.nrow):
			C = self.gen_row_constraints(row_number, rotation[row_number],round_number)
			constraints_list.append(C)
		constraints = "\n".join(constraints_list)
		return (constraints)
