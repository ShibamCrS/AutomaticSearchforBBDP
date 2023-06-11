#include<iostream>
#include<cstdio>
#include<bitset>
#include<vector>
#include<set>
#include<map>
#include<cmath>
#include<fstream>
#include<chrono>
#include<string>
#include<algorithm>
#include"gurobi_c++.h" 

using namespace std;
#define THREAD 8
#define STATE 128
#define PUBVAR 128
#define KEYVAR 128
typedef bitset<STATE> Monomial;
typedef bitset<STATE> Monomial_pub;
int depth = 0;
const int MAX = 200000000; // the maximum value of PoolSearchMode, P625


void PRINT_VEC(vector<int> &term)
{
    auto b = term.begin();
    auto e = term.end();   
    int counter = 0;
    for (auto it = b; it != e; it++ )
    {
        cout <<*it;
        counter ++;
        if(counter%4 == 0){
            cout << " ";
        }
    }
    /* cout << "Total Number of elements: "<<term.size()<<endl; */ 
}
void linear_layer_1(vector<int>& X, vector<int>& Y){
    int P[128] = {0,33,66,99,96,1,34,67,64,97,2,35,32,65,98,3,4,37,70,103,100,5,
                  38,71,68,101,6,39,36,69,102,7,8,41,74,107,104,9,42,75,72,105,10,43,40,
                  73,106,11,12,45,78,111,108,13,46,79,76,109,14,47,
                  44,77,110,15,16,49,82,115,112,17,50,83,80,113,18,51,48,81,114,19,20,
                  53,86,119,116,21,54,87,84,
                  117,22,55,52,85,118,23,24,57,90,123,120,25,58,91,88,121,26,59,
                  56,89,122,27,28,61,94,127,124,29,
                  62,95,92,125,30,63,60,93,126,31};
    for (int i=0; i<STATE; i++){
            Y[i] = X[P[i]];
    }
}

void print_trail(int rounds, vector<vector<GRBVar>> &X, GRBModel& model){    
    vector<int> term;
    vector<int> termy(STATE);
    for (int r=0; r< rounds+1; r++){
        term.clear();
        for ( int x=0; x<STATE; x++){
            if ( round( X[r][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                term.push_back(1);
            }
            else{
                term.push_back(0);
            }
        }
        if(r > 0){
            linear_layer_1(term, termy);
            printf("Y%2d: ",r);
            PRINT_VEC(termy);
            cout <<"\n";
        }
        printf("X%2d: ",r);
        PRINT_VEC(term);
        cout <<"\n";
    }
}
string getCurrentSystemTime()
{
    auto tt = chrono::system_clock::to_time_t(std::chrono::system_clock::now());
    struct tm* ptm = localtime(&tt);
    char date[60] = { 0 };
    sprintf(date, "%d-%02d-%02d-%02d:%02d:%02d", (int)ptm->tm_year + 1900, (int)ptm->tm_mon + 1, (int)ptm->tm_mday,
                                        (int)ptm->tm_hour, (int)ptm->tm_min, (int)ptm->tm_sec);
    return string(date);
}
