from sage.crypto.sbox import SBox
from sage.crypto.boolean_function import BooleanFunction
import sys
from multiset import *
from toposort import toposort, toposort_flatten
import copy
def frombin(v) :
	y = 0x00
	for i in range(0,len(v)):
		y = (y << 1) | int(v[i])
	return y
def tobin(i):
	return bin(i)[2:].zfill(4)
class Sbox:
	def __init__(self,sbox):
		self.sbox = sbox
		self.size = self.SboxSize() #size = n mean sbox is a map from F_2^n to F_2^n
		self.len = len(sbox) #length of sbox, if size=n then len=2^n
		self.ANF = []
		self.set_anf()
		self.R = self.ANF[0].ring()
		#print (self.R)
	def SboxSize(self):
		"""
		This function returns size of the sbox
		size = n mean sbox is a map from F_2^n to F_2^n
		"""
		l = format(len(self.sbox),"b")
		return (len(l) - 1)	  
	def ANF_to_num_rep(self,C):
		ANF_list = []
		K = str(C)
		K_split = K.split(" + ")
		#print (K_split)
		
		for k in K_split:
			#print (len(k))
			if(len(k) == 1):
				ANF_list.append(0)
			else:
				temp =[ 0 for i in range(0,self.size)]
				for i in range(0,len(k)):
					if(48 <= ord(k[i]) <= 57):
						temp[self.size - 1 - int(k[i])] = 1 #MSB (x_3,x_2,x_1,x_0) LSB
				y = frombin(temp)
				ANF_list.append(y)
			#ANF_list.sort()
		
		#print (C,"=>",ANF_list)			
		return ANF_list
		
	def linear_combination(self,u):
		 u_vec = tobin(u)
		 com = self.R(0)
		 for c in range(len(u_vec)):
		 	if (int(u_vec[c]) == 1):
		 		com = com + self.ANF[3-c]
		 return (com)
	def product(self,u):
		u_vec = tobin(u)
		com = self.R(1)
		#print (com)
		for c in range(len(u_vec)):
			if (int(u_vec[c]) == 1):
				com = com*self.ANF[3-c]
		return (com)	
	def set_anf(self) :
		s = SBox(self.sbox)
		for i in range(0,s.m) :
			self.ANF.append(s.component_function(1 << i).algebraic_normal_form())
		print ("The ANF of the given Sbox is ")
		for i in range(0,self.size):
			print ("y_%d = "%(i),self.ANF[i])
	def num_to_poly(self,L):
		P_list = []
		for l in L:
			#print (l)
			if (l == 0):
				P_list.append("1")
			else:
				l_vec = tobin(l)
				#print (l_vec)
				temp = ""
				for i in range(len(l_vec)):
					if(l_vec[i] == '1'):
						temp = temp + "x_%d"%(3-i)
				P_list.append(temp)
		
		return (" + ".join(P_list))
def order_poly(L1,L2):
	for l1 in L1:
		Flag = False
		for l2 in L2:
			if l1 & l2 == l1:
				Flag = True
				break
		if Flag == False:
			return (Flag)
	return (Flag)	
def simple_depen(ANF_dict):
	D = dict()
	for k in ANF_dict.keys():
		kth_list = []
		for k1 in ANF_dict.keys():
			if order_poly(ANF_dict[k],ANF_dict[k1]): #if k < k1, then k1 is dependent on k
				kth_list.append(k1)
		D[k] = kth_list
	return (D)
def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
    return visited	
def check_result(L,D):
	for l in L:
		Flag = True
		least = l[0]
		for x in l:
			res = order_poly(D[least],D[x])
			print(x,"=>",res," ",end="")
			if res == False:
				return (False)
		print(" \n")
	return (True)
		
if __name__ == '__main__':
	KNOT_sbox= [0x4,0x0,0xA,0x7,0xB,0xE,0x1,0xD,0x9,0xF,0x6,0x8,0x5,0x2,0xC,0x3]
	KNOT_sbox_model = Sbox(KNOT_sbox)
	ANF = KNOT_sbox_model.ANF
	for y in ANF:
		y_list = KNOT_sbox_model.ANF_to_num_rep(y)
	ANF_dict = dict()
	for i in range (1,16):
		test = KNOT_sbox_model.linear_combination(i)
		i_vec = tobin(i)
		#print (i,"=>",end=" ")
		test1 = KNOT_sbox_model.ANF_to_num_rep(test)
		ANF_dict[i] = (tuple(test1))
	#print (ANF_dict)
	keep_ANF = copy.deepcopy(ANF_dict)
	D = simple_depen(ANF_dict)
	keep = copy.deepcopy(D)
	final_dict = dict()
	for k in D.keys():
		V = dfs(D,k,[])
		final_dict[k] = V
	#print(final_dict)
	K = [i for i in final_dict.keys()]
	#print(K)
	K_sort = sorted(K,key=lambda x:len(final_dict[x]),reverse = True)
	final_list = []
	for i in K_sort:
		k = i
		V = dfs(D,k,[])
		#print ("V=>",V)
		final_list.append(V)
		for v in V:
			del ANF_dict[v]
		D = simple_depen(ANF_dict)
		if (len(D) == 0):
			break	
	
	for k in keep_ANF.keys():
		P = KNOT_sbox_model.num_to_poly(keep_ANF[k])
	print ("The final list of polynomials that we need to consider ")
	for k in final_list:
		P = KNOT_sbox_model.num_to_poly(keep_ANF[k[0]])
		k_vec = tobin(k[0])
		y_list = []
		for i in range(4):
			if (k_vec[i] == '1'):
				y_list.append("y_%d(x)"%(3-i))
		y = " + ".join(y_list)
		print (y," = ",P)
