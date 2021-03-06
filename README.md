This repository contains the supporting material of the paper "Automatic Search for Bit-based Division Property", accepted on Latincrypt 2021. 

Each directory with a cipher name contains a file named test.py. This file contains the necessary program to run a test with some initial division property. To start a test, we need to provide the following command:
> python3 test.py <block_size> <targeted_round> <initial_division_property>

For example, we want to test for KNOT. As KNOT has a two-dimensional (matrix) structure, we can refer to any bit in the state with i,j. Suppose we want to test 17-round KNOT-384 with initial division property K={k} such that k sets the first column as constant, i.e., 
									0,0 1,0 2,0 and 3,0 
positions are constants in the state matrix. To run this test, we use the following command:
> python3 test.py 384 17 0,0 1,0 2,0 3,0

NOTE: For the Ascon cipher, no need to provide division properties in the command line argument. 
We found that the Ascon has division property with almost 308 constants; we put those in a different file named input_division_property.py. 
To test with Ascon, we need to the following command
> python3 test.py 320 <round number>

/KNOT/KNOT_Extended Directory contains a program to test extended integral attack on KNOT. To test a monomial is even or not we have to provide integer representation of the monomial. For example, to test the monomial x_1x_0, we need to provide 3. So suppose we want to test for x_1x_0 (integer representation 3) and x_2x_1 (integer representation 6) we run the following command

> python3 full_test.py 256 17 3,6
