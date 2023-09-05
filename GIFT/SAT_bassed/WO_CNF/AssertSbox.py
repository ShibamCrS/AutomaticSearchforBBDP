from sbox import *
class AssertSbox(object):
	def __init__(self, sbox_name, sbox_list, rounds, number_of_sbox):
		self.rounds = rounds
		self.number_of_sbox = number_of_sbox
		self.sbox_name = sbox_name
		self.sbox_object = Sbox(sbox_list)
		self.sbox_size = self.sbox_object.size
		self.sbox_len = self.sbox_object.len
		self.declares = []
		self.asserts = []
		self.sbox_names = self.get_sbox_names()

	def get_sbox_names(self):
		names = []
		for r in range(self.rounds):
			temp = []
			for p in range(self.number_of_sbox):
				temp.append("%s_%d_%d"%(self.sbox_name,r,p))
			names.append(temp)
		return names

	def construct_binary_format_for_CVC(self, i):
		return '0bin'+bin(i)[2:].zfill(self.sbox_size)

	def declare_conditions_sbox(self, round_number, position_of_sbox):
		#create conditions for each sbox

		T = self.sbox_object.get_trails()
		temp = '%s:ARRAY BITVECTOR(%d) OF BITVECTOR(%d);' %(
			self.sbox_names[round_number][position_of_sbox],
			self.sbox_size, self.sbox_size)
		self.declares.append(temp)
		for in_DP in range(self.sbox_len):
			temp1 = '%s_%d:BITVECTOR(%d);' %(self.sbox_names[round_number][position_of_sbox],
				in_DP, self.sbox_size)
			self.declares.append(temp1)
			condition = [ ]
			for out_DP in T[in_DP]:
				condition.append('%s_%d = %s' %(self.sbox_names[round_number][position_of_sbox],
					in_DP, self.construct_binary_format_for_CVC(out_DP)))
			self.declares.append('ASSERT %s;' % ' OR '.join(condition))

			temp2 = 'ASSERT %s[%s] = %s_%d;' %(self.sbox_names[round_number][position_of_sbox],
				self.construct_binary_format_for_CVC(in_DP),
				self.sbox_names[round_number][position_of_sbox],
				in_DP)
			self.asserts.append(temp2)
	
	def get_constraints(self, in_vec, out_vec, r, p):
		s = 'ASSERT %s = %s[%s];' % (
                '@'.join(out_vec),
                self.sbox_names[r][p],
                '@'.join(in_vec)
                )
		return (s)
	def get_conditions(self):
		for r in range(self.rounds):
			for p in range(self.number_of_sbox):
				self.declare_conditions_sbox(r,p)
		return (self.declares + self.asserts)

if __name__ == "__main__":
	cipher = "LED"
	sbox_list = [0x4,0x0,0xA,0x7,0xB,0xE,0x1,0xD,0x9,0xF,0x6,0x8,0x5,0x2,0xC,0x3]
	rounds = 2
	number_of_sbox = 64
	a = AssertSbox('sbox', sbox_list, 2, number_of_sbox)
	print('\n'.join(a.get_conditions()))
	v1 = ['x0', 'x1', 'x2', 'x3']
	v2 = ['y0', 'y1', 'y2', 'y3']
	print (a.get_constraints(v1, v2, 1,15))
