#include "utility.h"
#include "model_utility.h"
#include "inputs.h"

void sbox_h(GRBModel& model, vector<GRBVar>& x, vector<GRBVar>& y)
{
    //found by sage
    int Ineq[][11] = {
        {4,6 ,3 ,3 ,3 ,6 ,-6 ,-7 ,-4 ,-4 ,-4 },
{0,-2 ,0 ,-2 ,-1 ,-1 ,2 ,3 ,2 ,3 ,2 },
{7,0 ,3 ,3 ,1 ,2 ,2 ,-4 ,-4 ,-6 ,-4 },
{8,2 ,-1 ,4 ,5 ,2 ,-6 ,1 ,-4 ,-5 ,-6 },
{8,0 ,-1 ,-1 ,-1 ,-1 ,-2 ,-2 ,-2 ,-3 ,5 },
{0,-1 ,-2 ,-2 ,-1 ,-1 ,4 ,4 ,2 ,2 ,3 },
{1,-3 ,-1 ,-1 ,-1 ,-3 ,3 ,2 ,4 ,5 ,3 },
{20,-5 ,-6 ,-6 ,-5 ,-5 ,-1 ,4 ,3 ,3 ,-2 },
{7,0 ,-2 ,1 ,1 ,0 ,3 ,-3 ,-2 ,-2 ,-3 },
{5,3 ,3 ,3 ,0 ,0 ,-2 ,-3 ,-5 ,-2 ,-2 },
{14,-4 ,-2 ,-2 ,-1 ,-1 ,-4 ,3 ,4 ,-1 ,-5 },
{14,-6 ,-3 ,-3 ,-1 ,-2 ,3 ,-1 ,-4 ,1 ,2 },
{0,-1 ,0 ,-2 ,-1 ,-1 ,2 ,3 ,2 ,2 ,1 },
{4,2 ,1 ,3 ,4 ,2 ,-5 ,-3 ,-3 ,-4 ,-1 },
{0,0 ,-1 ,-1 ,-2 ,-1 ,2 ,3 ,3 ,2 ,2 },
{0,1 ,1 ,1 ,1 ,1 ,-1 ,-1 ,-1 ,-1 ,-1 },
{4,2 ,0 ,1 ,3 ,2 ,-4 ,0 ,-3 ,-3 ,-2 },
{4,0 ,-1 ,-3 ,-3 ,-2 ,2 ,4 ,3 ,1 ,1 },
{4,0 ,3 ,5 ,1 ,1 ,-2 ,-2 ,-3 ,-4 ,-2 },
{9,-1 ,-1 ,-2 ,-2 ,0 ,1 ,-1 ,-3 ,2 ,-2 },
{7,2 ,-1 ,3 ,2 ,-1 ,-4 ,1 ,-3 ,-2 ,-4 },
{0,-3 ,-1 ,-2 ,-1 ,-1 ,4 ,3 ,2 ,4 ,4 }
};

/* for ( auto it : Ineq ) */
/*     model.addConstr( it[0] + it[1] * x[3] + it[2] * x[2] + it[3] * x[1] + it[4] * x[0] + it[5] * y[3] + it[6] * y[2] + it[7] * y[1] + it[8] * y[0] >= 0 ); */
for ( auto it : Ineq )
    model.addConstr( it[0] + it[1]*x[0] + it[2]*x[1] + it[3]*x[2] + it[4]*x[3] + it[5]*x[4]
                           + it[6]*y[0] + it[7]*y[1] + it[8]*y[2] + it[9]*y[3] + it[10]*y[4] >= 0 );

}
//L(Y) = X
void diffusion(GRBModel& model, vector<GRBVar>& Y, vector<GRBVar>& X) {
    vector<GRBVar> Y0 (vector<GRBVar>(64)) ;
    vector<GRBVar> Y1 (vector<GRBVar>(64)) ;
    vector<GRBVar> Y2 (vector<GRBVar>(64)) ;
    vector<GRBVar> Y3 (vector<GRBVar>(64)) ;
    vector<GRBVar> Y4 (vector<GRBVar>(64)) ;

    vector<GRBVar> X0 (vector<GRBVar>(64)) ;
    vector<GRBVar> X1 (vector<GRBVar>(64)) ;
    vector<GRBVar> X2 (vector<GRBVar>(64)) ;
    vector<GRBVar> X3 (vector<GRBVar>(64)) ;
    vector<GRBVar> X4 (vector<GRBVar>(64)) ;

    for(int i = 0 ; i<64; i++){
        Y0[i] = Y[i] ;
        Y1[i] = Y[64 + i] ;
        Y2[i] = Y[128 + i] ;
        Y3[i] = Y[192 + i] ;
        Y4[i] = Y[256 + i] ;

        X0[i] = X[i] ;
        X1[i] = X[64 + i] ;
        X2[i] = X[128 + i] ;
        X3[i] = X[192 + i] ;
        X4[i] = X[256 + i] ;
    }
    
    linear_layer(model, Y0, X0, 19, 28) ;
    linear_layer(model, Y1, X1, 61, 39) ;
    linear_layer(model, Y2, X2, 1, 6) ;
    linear_layer(model, Y3, X3, 10, 17) ;
    linear_layer(model, Y4, X4, 7, 41) ;
}

//S(X) = Y
void substitution(GRBModel& model, vector<GRBVar>& X, vector<GRBVar>& Y) {
    for(int i = 0 ; i< 64; i++){
        vector<GRBVar> tmpx (vector<GRBVar>(5)) ;
        vector<GRBVar> tmpy (vector<GRBVar>(5)) ;

        tmpx[0] = X[i]; 
        tmpx[1] = X[64 + i] ;
        tmpx[2] = X[128 + i] ;
        tmpx[3] = X[192 + i ] ; 
        tmpx[4] = X[256 + i] ;

        tmpy[0] = Y[i] ; 
        tmpy[1] = Y[64 + i] ;
        tmpy[2] = Y[128 + i] ;
        tmpy[3] = Y[192 + i] ;
        tmpy[4] = Y[256 + i] ;
        
        /* sbox(model, tmpx, tmpy) ; */ 
        sbox_h(model, tmpx, tmpy) ; 
    }   
}
void division_property(int rounds, vector<int> &active, vector<int> &not_balanced){
	GRBEnv env = GRBEnv();
    env.set(GRB_IntParam_LogToConsole, 0);
    env.set(GRB_IntParam_Threads, THREAD );
    
    GRBModel model = GRBModel(env);
    //X0 - > SB -> Y0 -> L -> X1 -> SB -> Y1   
    vector<vector<GRBVar>> X(rounds, vector<GRBVar>(STATE));
    vector<vector<GRBVar>> Y(rounds, vector<GRBVar>(STATE));
    for( int r = 0 ; r<rounds; r++){
        for( int i = 0; i<STATE; i++){
            X[r][i] = model.addVar(0, 1, 0, GRB_BINARY);
            Y[r][i] = model.addVar(0, 1, 0, GRB_BINARY);
        }
    }
    
    for( int r = 0; r<rounds; r++){
        substitution(model, X[r], Y[r]) ;
        if(r != (rounds-1))
            diffusion(model, Y[r], X[r+1]) ;
    }
	
    //input constraint
    for ( int i = 0; i < STATE; i++ ){
        if ( active[i] == 0 ){
            model.addConstr( X[0][i] == 0 );
        }
        else{
            model.addConstr( X[0][i] == 1 );
        }
    }

    GRBLinExpr nv = 0;
    for ( int i = 0; i < STATE; i++ ){
        nv += Y[rounds-1][i];
    }
    // minimize the objective function
    model.setObjective(  nv, GRB_MINIMIZE );
    
    model.write("./data/model.lp");
    bool flag;
    int counter = 0;
    cout << "Not Balanced:\n" << endl;
    while(counter < STATE){
        model.update();
        model.optimize();
        if ( model.get( GRB_IntAttr_Status ) == GRB_OPTIMAL ){
            double obj_value = round(model.get(GRB_DoubleAttr_ObjVal));
            cout << "OBJ " << obj_value <<"=>";
            if (obj_value > 1){
                break;
            }
            else{
                print_trail(rounds, X, Y, model);
                for ( int x=0; x<STATE; x++){
                    if ( round( Y[rounds-1][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                        counter++;
                        not_balanced.push_back(x);
                        //model.addConstr(X[rounds][x] == 0);
                        Y[rounds-1][x].set(GRB_DoubleAttr_UB, 0);
                        cout << counter << ":" << x <<"--";
                        break;
                    }
                }
            }
        }
        else if( model.get( GRB_IntAttr_Status ) == GRB_INFEASIBLE ){
            flag = true;
            break;
        }
        else{
            cout << "Other status " << GRB_IntAttr_Status <<  endl;
            exit(-1);
        }
    }
    cout<<endl;
}
void set_input(vector<int> &active, int s, int e){
    for(int i=0; i<STATE; i++){
       active[i] = 1;
    }
    for(int i=s; i<e; i++){
        active[constant_bits[i]] = 0;   
    }
}
void test(){
    int rounds = 5;
    vector<int > not_balanced;
    vector<int > active(STATE);
    set_input(active, 15, 320);
    print_prop(active);
    
    division_property(rounds, active, not_balanced);
    printf("Balanced Bits: \n");
    for(int i=0; i<STATE; i++){
        if (std::find(not_balanced.begin(), not_balanced.end(), i) != not_balanced.end())
            continue;
        else 
           cout << i << " ";
    }
    cout<<endl;
}
int main(){
    test();    
    /* test_good_input(); */
    /* test_poly(); */    
}
