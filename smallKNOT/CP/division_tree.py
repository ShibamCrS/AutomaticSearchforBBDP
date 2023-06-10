from sbox import *
from permutation import *
def PRINT_DICT(T):
    for k in T.keys():
        print(k , " => ", T[k])
class CIPHER_MODEL(object):
    def __init__(self, sbox_list, block_size, number_of_rounds, number_of_sbox):
        self.__sbox = Sbox(sbox_list)
        self.__sbox_size = self.__sbox.size	
        self.__sbox.DivisionTrails()
        self.__sbox_trails = self.bin_table(self.__sbox.trails)
        PRINT_DICT(self.__sbox_trails)
        self.__block_size = block_size
        self.__permutation = [2, 3, 0, 1]
        self.__rounds = number_of_rounds
        self.__number_of_sbox = number_of_sbox
        self.__row_size = block_size >> 2
        self.__nrow = int(self.__block_size/self.__row_size)

        self.tree = [[] for _ in range(self.__rounds+1)]
    
    def construct_binary_format(self, i):
        return bin(i)[2:].zfill(self.__sbox_size)
		    
    def bin_table(self, int_table):
        bin_table = dict()
        for k in int_table.keys():
            input_bin =  self.construct_binary_format(k)
            output_bin = [self.construct_binary_format(kk) for kk in int_table[k]]
            bin_table[input_bin] = output_bin
        return bin_table 
    def permute(self,inputs):
        outputs = ""
        for i in range(len(inputs)):
            outputs += inputs[self.__permutation[i]]
        return outputs
    def gen_tree(self, in_K):
        self.tree[0].append(in_K)
        self.tree[1].extend(self.__sbox_trails[in_K])				
        if self.__rounds > 1:
            for r in range(1, self.__rounds):
                L = self.tree[r]
                #print (L)
                for i in range(len(L)):
                    inputs = L[i]
                    if(inputs != "----"):
                        inputs = self.permute(inputs)
                        self.tree[r+1].extend(self.__sbox_trails[inputs])
                        if (i != len(L) - 1):
                            self.tree[r+1].append("----")
        return self.tree      
    
    def len_nodes(L):
        length = 0
        for l in L:
            length +=len(l) 
            length += 1
        return length
        
    def PRINT_TREE(self,tree):
        print ("================DIVISION TREE==================")
        for nodes in tree:
            s = " ".join(nodes)
            length = len(s)
            print(s.center(80))
            print("\n")
if __name__ == "__main__":
    sbox_list = [0x4,0x0,0xA,0x7,0xB,0xE,0x1,0xD,0x9,0xF,0x6,0x8,0x5,0x2,0xC,0x3]
    KNOT = CIPHER_MODEL( sbox_list, 4, 2,1)
    T = KNOT.gen_tree("1110")
    KNOT.PRINT_TREE(T)
