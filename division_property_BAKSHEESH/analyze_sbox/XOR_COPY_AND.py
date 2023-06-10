from quine_mccluskey.qm import QuineMcCluskey

def construct_binary_format(i, n):
    return bin(i)[2:].zfill(n)
        
class Model:
    def __init__(self, sop, n):
        self.pos = self.sop_to_pos(sop, n)
        self.n = n  #length input+output

    def sop_to_pos(self, SOP, n):
        ones = []
        for i in range(2**n):
            bin_i = construct_binary_format(i, n)
            if bin_i not in SOP:
                ones.append(bin_i)
        print(ones)
        qm = QuineMcCluskey(use_xor=False)
        POS = qm.simplify_los(ones,dc = [ ], num_bits = n)
        return POS
        
    def get_function_constraints_CNF(self):
        pos = self.pos
        pos = list(pos)
        fun = [ ]
        l = self.n
        for maxterm in pos:
            temp = [ ]
            if '0' in maxterm or '1' in maxterm:
                for i in range(l):
                    if(maxterm[i] == '1'):
                        temp.append ("0")
                    elif(maxterm[i] == '0'):
                        temp.append ("1")
                    elif(maxterm[i] == '-'):
                        temp.append ("2")

                c_format = "{" + ", ".join(temp) + "}"
                fun.append(c_format)

        return (l, fun)
    
def print_c_formated(cnf, l, fun_name):
    f = open("../constraints_"+fun_name+".h", "w")
    SOP_xor =  ['000','011','101']
    s = "#define "+ fun_name + "_cnflen " +str(len(cnf)) + "\n"
    s += "const int Constraint_" + fun_name + "[" + str(len(cnf)) + "]["+ str(l) + "] = {\n"
    s = s + ", \n".join(cnf) + "};"
    f.write(s)
    f.write("\n")
    f.close()

def test_div(sop, n, fun_name):
    model_div = Model(sop, n)
    l, CNF  = model_div.get_function_constraints_CNF()
    print_c_formated(CNF, l, fun_name)

if __name__ == '__main__':
    SOP =  ['000','011','101']
    test_div(SOP, 3, "xor")
