def gen_permutation1():
	"""
	Linear layer of Present.
	"""
	variable = [x for x in range(64)]
	array = [0 for i in range(0,64)]
	for i in range(0,63):
		array[(16 * i) % 63] = variable[i]
	array[63] = variable[63]
	return (array)
def LinearLaryer(variable):
	"""
	Linear layer of Present.
	"""
	array = ["" for i in range(0,64)]
	for i in range(0,63):
		array[(16 * i) % 63] = variable[i]
	array[63] = variable[63]
	return array
	
def CreateVariables(n):
	"""
	Generate the variables used in the model.
	"""
	array = []
	for i in range(0,64):
		array.append(("x" + "_" + str(n) + "_" + str(i)))
	return array
if __name__ == "__main__":
	X = CreateVariables(1)
	PX = LinearLaryer(X)
	P = gen_permutation1()
	print(X)
	print(PX)
	print(P)
