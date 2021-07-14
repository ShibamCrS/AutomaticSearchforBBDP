from quine_mccluskey.qm import QuineMcCluskey
def construct_binary_format(size, i):
		return bin(i)[2:].zfill(size)
class FUN:
	def __init__(self, out_size = 3):
		self.out_size = out_size
		#self.all_vectors = get_all_vectors(size)
		self.Points = dict()
		self.C_Points = dict()
		self.pos = []
		self.set_POS()
		
	def gen_T(self):
		if not self.Points:
			for a in range(2):
				P = []
				C_P = []
				for b in range(2**self.out_size):
					s = a
					for i in range(self.out_size):
						s = s - ((b >> i) & 1)
					if s == 0:
						P.append(b)
				self.Points[a] = P
	def get_T(self):
		if not self.Points:
			self.gen_T()
		return self.Points
		
	def get_C_T(self):
		if not self.C_Points:
			T = self.get_T()
			All = [x for x in range(2**self.out_size)]
			#print (All)
			for a in range(2):
				self.C_Points[a] = [x for x in All if x not in T[a]]
		return self.C_Points
		
	
	def set_POS(self):
		if not self.pos:
			T = self.get_C_T()
			ones = [ ]
			for a in range(2):
				a_vec = construct_binary_format(1,a)
				for b in T[a]:
					b_vec = construct_binary_format(self.out_size,b)
					ones.append(a_vec + b_vec)
			#print (ones)
			qm = QuineMcCluskey(use_xor=False)
			nb = self.out_size + 1
			self.pos = qm.simplify_los(ones,dc = [ ], num_bits = nb)
			#print (self.pos)
	def get_constraints(self,X,Y):
		POS = self.pos
		fun = [ ]
		nb = 1 + self.out_size
		for maxterm in POS:
			temp = [ ]
			for i in range(1):
				if(maxterm[i] == '1'):
					temp.append ('('+'~'+X[i]+')')
				elif(maxterm[i] == '0'):
					temp.append (X[i])
			for i in range(1,nb):
				if(maxterm[i] == '1'):
					temp.append ('('+'~ '+Y[i-1]+')')
				elif(maxterm[i] == '0'):
					temp.append (Y[i-1])
			fun.append('('+"|".join(temp)+')')
		f_main ='ASSERT ' + '&'.join(fun)+'=0bin1'+';'
		return (f_main)
if __name__ == "__main__":
	Cp = FUN(3)
	print (Cp.get_T())
	print("\n")
	print (Cp.get_C_T())
	X = ['a']
	Y = []
	for i in range(4):
		Y.append('%s_%d'%('u',i))
	print (Cp.get_constraints_CNF(X,Y))
