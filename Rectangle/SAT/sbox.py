from quine_mccluskey.qm import QuineMcCluskey
class Sbox:
	def __init__(self,sbox):
		self.sbox = sbox
		self.size = self.SboxSize() #size = n mean sbox is a map from F_2^n to F_2^n
		self.len = len(sbox) #length of sbox, if size=n then len=2^n
		self.trails = dict()
		self.C_trails= dict()
		self.sop = []
		self.pos = []
		self.set_SOP()
		self.set_POS()
		self.possible_pattern = [ ]
		self.Impossible_pattern = [ ]
	def SboxSize(self):
		"""
		This function returns size of the sbox
		size = n mean sbox is a map from F_2^n to F_2^n
		"""
		l = format(len(self.sbox),"b")
		return (len(l) - 1)
	def BitProduct(self,u,x):
		"""
		Returns pi_u(x)
		"""
		if (u & x) == u:
			return 1 # u belongs to Prec(x) 
		else:
			return 0 
		
	def TruthTable(self,u):
		"""
		Returns truth table of pi_u
		note that pi_u(y)=y^u is a boolean function
		""" 
		temp =[u for i in range(0,self.len)]
		table = list(map(self.BitProduct,temp,self.sbox))
		return table
	def ProcessTable(self, table):
		"""
		Process the truth table to get the ANF of the boolean function
		we use table size to calculate the SBOXSIZE
		"""
		for i in range(0, self.size):
			for j in range(0, 2**i):
				for k in range(0, 2**(self.size - 1 - i)):
					table[k + 2**(self.size - 1 - i) + j*(2**(self.size - i))] =\
	                table[k + 2**(self.size - 1 - i) + j*(2**(self.size - i))] ^\
	                table[k + j*(2**(self.size - i))]
	
	def ANF_bit_product_function(self):
		"""
		Returns ANF of pi_u(y) for all u
		Returns a list of lists
		where uth list is ANF of pi_u(y)
		"""
		
		ANF = [[] for u in range(0,self.len)]
		for u in range(1,self.len):
			table = self.TruthTable(u)
			self.ProcessTable(table)
			temp = []
			for j in range(0,self.len):
				if table[j] != 0:
					temp.append(j)
			ANF[u] = temp
		return ANF
		
	
	def DivisionTrails(self):
		ANF = self.ANF_bit_product_function()
		self.trails[0] = [0]
		
		for i in range(1,self.len):
			"""
			Will check for all possible non-zero 
			input property.
			for example, if i = 5, then 
			input division property = (0,1,0,1)
			"""
			output_vectors = []
			for j in range(1,self.len):
				flag = False
				for k in ANF[j]:
					if (i | k) == k: 
						"""k is in Succ(i)"""
						flag = True
						"""pi_j(y) contains a monomial x^k where k is in Succ(i)
					   	So we need to add (i,j) in CBDP."""
						break
				if flag:
					redundant = []
					add_j = True
					"""
				   	But j maybe redundant i.e there is (i,j1) in CBDP 
				   	s.t. j1 is in Succ(j1)
				   	Next few lines will check that
					"""
					for t in output_vectors:
						if (t|j) == j:
							"""
							If already there is a vector t in output_vectors
							so that j is in Succ(t), no need to add j
							"""
							add_j = False
							break
						elif (t|j)==t:
							"""
							If t is in Succ(j), then no need to keep t.
							So adding a new j may remove some t.
							"""
							redundant.append(t)
					if add_j:
						for r in redundant:
							output_vectors.remove(r)
						output_vectors.append(j)
			output_vectors.sort()
			self.trails[i] = output_vectors
			
	def get_trails(self):
		if not self.trails:
			self.DivisionTrails()
		return self.trails
	def get_C_trails(self):
		if not self.C_trails:
			T = self.get_trails()
			All = [x for x in range(self.len)]
			for in_DP in range(self.len):
				self.C_trails[in_DP] = [x for x in All if x not in T[in_DP]]
		return self.C_trails
	def construct_binary_format(self, i):
		return bin(i)[2:].zfill(self.size)
	def set_POS(self):
		if not self.pos:
			T = self.get_C_trails()
			ones = [ ]
			for in_DP in range(self.len):
				in_DP_vec = self.construct_binary_format(in_DP)
				for out_DP in T[in_DP]:
					out_DP_vec = self.construct_binary_format(out_DP)
					ones.append(in_DP_vec + out_DP_vec)
			#print (len(ones))
			qm = QuineMcCluskey(use_xor=False)
			self.pos = qm.simplify_los(ones,dc = [ ], num_bits = 8)
	def set_SOP(self):
		if not self.sop:
			T = self.get_trails()
			ones = [ ]
			for in_DP in range(self.len):
				in_DP_vec = self.construct_binary_format(in_DP)
				for out_DP in T[in_DP]:
					out_DP_vec = self.construct_binary_format(out_DP)
					ones.append(in_DP_vec + out_DP_vec)
			#print (len(ones))
			qm = QuineMcCluskey(use_xor=False)
			self.sop = qm.simplify_los(ones,dc = [ ], num_bits = 8)
	def get_sbox_constraints(self,X,Y):
		POS = self.pos
		fun = [ ]
		for maxterm in POS:
			temp = [ ]
			for i in range(4):
				if(maxterm[i] == '1'):
					temp.append ('('+'~'+X[i]+')')
				elif(maxterm[i] == '0'):
					temp.append (X[i])
			for i in range(4,8):
				if(maxterm[i] == '1'):
					temp.append ('('+'~ '+Y[i-4]+')')
				elif(maxterm[i] == '0'):
					temp.append (Y[i-4])
			fun.append('('+"|".join(temp)+')')
		sbox_main ='ASSERT ' + '&'.join(fun)+'=0bin1'+';'
		return (sbox_main)
