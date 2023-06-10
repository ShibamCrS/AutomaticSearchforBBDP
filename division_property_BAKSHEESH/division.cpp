/*
 g++ -Ofast -std=c++11 division.cpp -lcryptominisat5 -o division
	*/

#include <cryptominisat5/cryptominisat.h>
#include <assert.h>
#include <vector>
#include <time.h>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <fstream>
#include <math.h>
#include <cstring>

#define THREADS 8
#define BLOCK 128
#define CELL 4
#define N_SBOX 32

#define ROUNDS 13
 
using std::vector;
using namespace CMSat;
using namespace std;

#include "constraints_div_sbox.h"

void set_initial_conditions(uint32_t *INV, uint32_t *OUTV,
                            uint8_t *input_div, uint8_t *output_div,
                            SATSolver &solver){
    for(int i=0; i<BLOCK; i++){
        vector<Lit> clause;
        clause.clear();
        if(input_div[i] == 1){
            clause.push_back(Lit(INV[i], false));
        }
        else{
            clause.push_back(Lit(INV[i], true));
        }
        solver.add_clause(clause);
    }
    for(int i=0; i<BLOCK; i++){
        vector<Lit> clause;
        clause.clear();
        if(output_div[i] == 1){
            clause.push_back(Lit(OUTV[i], false));
        }
        else{
            clause.push_back(Lit(OUTV[i], true));
        }
        solver.add_clause(clause);
    }
}

//Returns the number of variables declared so far
int declearVariables(uint32_t **X){
    //declare array of variables
    for(int r=0; r<ROUNDS+1; r++){
        X[r]  = new uint32_t [BLOCK];
    }
    
    int sx = 0;
    for(int r=0; r<ROUNDS+1; r++){
        //Input to the sboxes
        for(int i=0; i<BLOCK; i++){
            X[r][i] = sx++;
        }
    }
    return sx;
}

void SB(uint32_t *A, uint32_t *B, SATSolver &solver){
    vector<Lit> clause;
    for(int s=0; s<N_SBOX; s++){
        //4 input varr
        //4 output vars
        int X[8];
        for(int i=0; i<CELL; i++){
            X[i] = A[CELL*s + i];
            X[i+CELL] = B[CELL*s + i];
        }
        //Add CNF on variables X[0],.., X[3],X[4],...,X[7]
        for (int restriction = 0; restriction < sbox_cnflen; restriction++){
            clause.clear();
            for (int i=0; i<8; i++){
                if (Constraint_sbox[restriction][i] == 1){
                    clause.push_back(Lit(X[i], false)); //X[i]
                }
                if (Constraint_sbox[restriction][i] == 0){
                    clause.push_back(Lit(X[i], true)); //~X[i]
                }
            }
            solver.add_clause(clause);
        }
    }
}
void generateOneRound(uint32_t **X, SATSolver & solver){
    vector<Lit> clause;
    clause.clear();
    int P[128] = {0,33,66,99,96,1,34,67,64,97,2,35,32,65,98,3,4,37,70,103,100,5,38,71,68,101,6,39,36,69,102,
7,8,41,74,107,104,9,42,75,72,105,10,43,40,73,106,11,12,45,78,111,108,13,46,79,76,109,14,47,
44,77,110,15,16,49,82,115,112,17,50,83,80,113,18,51,48,81,114,19,20,53,86,119,116,21,54,87,84,
117,22,55,52,85,118,23,24,57,90,123,120,25,58,91,88,121,26,59,56,89,122,27,28,61,94,127,124,29,
62,95,92,125,30,63,60,93,126,31};

    for(int r=0; r<ROUNDS; r++){
        uint32_t Y[BLOCK];
        for (int i=0; i<BLOCK; i++){
            Y[i] = X[r+1][P[i]];
        }    
        SB(X[r], Y, solver);
    }
}

/*
Convention For Variables
X_0 -> S -> Y -> L -> X_1
X_1 -> S -> Y -> L -> X_2
...
*/

//returns if satisfiable
int analysis(uint8_t *input_div = NULL, uint8_t *output_div = NULL){
    //declare array of variables for each round

    uint32_t ** X = new uint32_t * [ROUNDS+1];
    int sx = declearVariables(X);
    
    printf("Number Of Variables = %d\n", sx);
    SATSolver solver;
    solver.set_num_threads(THREADS);
    solver.new_vars(sx);
    
    set_initial_conditions(X[0], X[ROUNDS], input_div, output_div, solver);
    
    //Function given in model_differential.h
    generateOneRound(X, solver);

    //Solve the system
    lbool ret = solver.solve();
    /* cout << ret << endl; */
    /* if (ret == l_True){ */
    /*     analyzeResults(Z, X, Y, solver); */
    /* } */   

    //Free Variables
    for (int r=0; r<ROUNDS+1; r++){
        delete [] X[r];
    }

    delete [] X;

    if(ret == l_True){
        return 1;
    }
    else{
        return 0;
    }
}
void print_bit(uint8_t *A){
    for(int i=0; i<BLOCK; i++){
        printf("%d",A[i]);
    }
    printf("\n");
}

void test(){
    uint8_t input_div[BLOCK];
    memset(input_div, 0x01, BLOCK);

    uint8_t output_div[BLOCK];
    memset(output_div, 0x00, BLOCK);

    uint8_t temp[BLOCK];
    memcpy(temp, input_div, BLOCK);
    for(int i=0; i<1; i++){
        memcpy(input_div, temp, BLOCK);
        input_div[i] = 0x00;
        print_bit(input_div);
        vector<int> balanced;

        uint32_t nr_of_balanced = 0;
        for(int j=0; j<1; j++){
            memset(output_div, 0x00, BLOCK);
            output_div[j] = 0x01;
            print_bit(output_div);
            int res = analysis(input_div, output_div);
            if(res == 1){
                printf("UNKNOWN\n");
            }
            else{
                printf("BALANCED\n");
                balanced.push_back(j);
                nr_of_balanced++;
            }
        }
        printf("-----%d-----------Total Balanced Bits = %d--------------\n", i, nr_of_balanced);
        for(auto b: balanced){
            cout<<b<<" ";
        }
        cout <<"\n";
    }
}

int main(){
    test();
}

