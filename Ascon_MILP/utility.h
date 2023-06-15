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
#define STATE 320
#define SB 64

void PRINT_VEC(vector<int> &term)
{
    auto b = term.begin();
    auto e = term.end();   
    int counter = 0;
    for (auto it = b; it != e; it++ )
    {
        cout <<*it;
        counter ++;
        if(counter%5 == 0){
            cout << " ";
        }
    }
    /* cout << "Total Number of elements: "<<term.size()<<endl; */ 
}
/* void linear_layer_1(vector<int>& X, vector<int>& Y){ */
/*     int P[STATE]; */
/*     for (int j=0; j<STATE-1; j++){ */
/*         P[((STATE>>2) * j) % (STATE-1)] = j; */
/*     } */
/*     P[STATE-1] = STATE-1; */
/*     for (int i=0; i<STATE; i++){ */
/*             Y[i] = X[P[i]]; */
/*     } */
/* } */
void print_prop(vector<int> &A, FILE *fp=stdout){
    for (int i=0; i<STATE; i++){
        fprintf(fp, "%d",A[i]);
        if((i%64) == 63){
            fprintf(fp, "\n");
        }
    }
    fprintf(fp, "\n");
}
void print_vec(vector<int> &A, FILE *fp=stdout){
    for (int i: A){
        fprintf(fp, "%d, ",i);
    }
    fprintf(fp, "\n");
}
void print_trail(int rounds, vector<vector<GRBVar>> &X, vector<vector<GRBVar>> &Y, GRBModel& model){    
    cout<<"\n";
    vector<int> term;
    vector<int> termy(STATE);
    for (int r=0; r< rounds; r++){
        term.clear();
        for ( int x=0; x<STATE; x++){
            if ( round( X[r][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                term.push_back(1);
            }
            else{
                term.push_back(0);
            }
        }
        printf("X%2d: \n",r);
        print_prop(term);
        cout <<"\n";

        term.clear();
        for ( int x=0; x<STATE; x++){
            if ( round( Y[r][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                term.push_back(1);
            }
            else{
                term.push_back(0);
            }
        }
        printf("Y%2d: \n",r);
        print_prop(term);
        cout <<"\n";
    }
}
void print_balanced(vector<int> NB){
    for(int i=0; i<STATE; i++){
        if (std::find(NB.begin(), NB.end(), i) != NB.end())
            printf("?");
        else
            printf("0");
        if(i%64 == 63)
            printf("\n");
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
