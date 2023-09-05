from sage.crypto.sbox import SBox

def frombin(v) :
	y = 0x00
	for i in range(0,len(v)):
		y = (y << 1) | int(v[i])
	return y

class SBOX:
	def __init__(self,sbox):
		self.sbox = sbox
		self.size = self.SboxSize() #size = n mean sbox is a map from F_2^n to F_2^n
		self.len = len(sbox) #length of sbox, if size=n then len=2^n
	def SboxSize(self):
		"""
		This function returns size of the sbox
		size = n mean sbox is a map from F_2^n to F_2^n
		"""
		l = format(len(self.sbox),"b")
		return (len(l) - 1)	   	
	def anf(self) :
		s = SBox(self.sbox)
		print (s)
		ANF = []
		for i in range(0,s.m) :
			ANF.append(s.component_function(1 << i).algebraic_normal_form())
		for i in range(0,self.size):
			print (ANF[i])
		ANF_list = [[] for i in range(0,self.size)]
		
		for r,C in enumerate(ANF) :
			#R = BooleanPolynomialRing(8,'x')
			C_new = BooleanPolynomialRing(self.size,'x')(0)	#Takng 0 as a polynomial
			for M in C :
				#if M.degree() == 2 :
				C_new = C_new + M
			
			K = str(C_new)
			K_split = K.split(" + ")
			print (K_split)
			temp_1 = []
			for k in K_split:
				#print (len(k))
				if(len(k) == 1):
					temp_1.append(0)
				else:
					temp =[ 0 for i in range(0,self.size)]
					for i in range(0,len(k)):
						if(48 <= ord(k[i]) <= 57):
							print (int(k[i]),end= " ")
							temp[self.size - 1 - int(k[i])] = 1
					y = frombin(temp)
					temp_1.append(y)
				temp_1.sort()
				ANF_list[r] = temp_1
					
		for i in range(0,self.size):
			print ((ANF[i]),ANF_list[i])	
					
		return ANF

if __name__ == '__main__':
	sbox = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd, 0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]
	KNOT_sbox_model = SBOX(sbox)
	ANF = KNOT_sbox_model.anf()
	
