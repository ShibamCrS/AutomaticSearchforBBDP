

# This file was *autogenerated* from the file test_ANF.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0x00 = Integer(0x00); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_48 = Integer(48); _sage_const_57 = Integer(57); _sage_const_0xc = Integer(0xc); _sage_const_0x5 = Integer(0x5); _sage_const_0x6 = Integer(0x6); _sage_const_0xb = Integer(0xb); _sage_const_0x9 = Integer(0x9); _sage_const_0x0 = Integer(0x0); _sage_const_0xa = Integer(0xa); _sage_const_0xd = Integer(0xd); _sage_const_0x3 = Integer(0x3); _sage_const_0xe = Integer(0xe); _sage_const_0xf = Integer(0xf); _sage_const_0x8 = Integer(0x8); _sage_const_0x4 = Integer(0x4); _sage_const_0x7 = Integer(0x7); _sage_const_0x1 = Integer(0x1); _sage_const_0x2 = Integer(0x2)
from sage.crypto.sbox import SBox

def frombin(v) :
	y = _sage_const_0x00 
	for i in range(_sage_const_0 ,len(v)):
		y = (y << _sage_const_1 ) | int(v[i])
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
		return (len(l) - _sage_const_1 )	   	
	def anf(self) :
		s = SBox(self.sbox)
		print (s)
		ANF = []
		for i in range(_sage_const_0 ,s.m) :
			ANF.append(s.component_function(_sage_const_1  << i).algebraic_normal_form())
		for i in range(_sage_const_0 ,self.size):
			print (ANF[i])
		ANF_list = [[] for i in range(_sage_const_0 ,self.size)]
		
		for r,C in enumerate(ANF) :
			#R = BooleanPolynomialRing(8,'x')
			C_new = BooleanPolynomialRing(self.size,'x')(_sage_const_0 )	#Takng 0 as a polynomial
			for M in C :
				#if M.degree() == 2 :
				C_new = C_new + M
			
			K = str(C_new)
			K_split = K.split(" + ")
			print (K_split)
			temp_1 = []
			for k in K_split:
				#print (len(k))
				if(len(k) == _sage_const_1 ):
					temp_1.append(_sage_const_0 )
				else:
					temp =[ _sage_const_0  for i in range(_sage_const_0 ,self.size)]
					for i in range(_sage_const_0 ,len(k)):
						if(_sage_const_48  <= ord(k[i]) <= _sage_const_57 ):
							print (int(k[i]),end= " ")
							temp[self.size - _sage_const_1  - int(k[i])] = _sage_const_1 
					y = frombin(temp)
					temp_1.append(y)
				temp_1.sort()
				ANF_list[r] = temp_1
					
		for i in range(_sage_const_0 ,self.size):
			print ((ANF[i]),ANF_list[i])	
					
		return ANF

if __name__ == '__main__':
	sbox = [_sage_const_0xc , _sage_const_0x5 , _sage_const_0x6 , _sage_const_0xb , _sage_const_0x9 , _sage_const_0x0 , _sage_const_0xa , _sage_const_0xd , _sage_const_0x3 , _sage_const_0xe , _sage_const_0xf , _sage_const_0x8 , _sage_const_0x4 , _sage_const_0x7 , _sage_const_0x1 , _sage_const_0x2 ]
	KNOT_sbox_model = SBOX(sbox)
	ANF = KNOT_sbox_model.anf()
	

