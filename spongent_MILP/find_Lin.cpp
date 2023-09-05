#include "utility.h"
#include "model_utility.h"

void sbox(GRBModel& model, vector<GRBVar>& x, vector<GRBVar>& y)
{    
    //found by sage
    int Ineq[][9] = {
        {0,1 ,1 ,1 ,1 ,-1 ,-1 ,-1 ,-1 },
{1,0 ,-1 ,-1 ,-2 ,2 ,1 ,1 ,1 },
{1,0 ,0 ,0 ,3 ,-1 ,-1 ,-1 ,-1 },
{4,-1 ,1 ,0 ,0 ,-3 ,3 ,-2 ,-2 },
{4,-1 ,0 ,1 ,0 ,-3 ,-2 ,3 ,-2 },
{0,-2 ,-1 ,-1 ,-2 ,5 ,4 ,4 ,2 },
{2,-1 ,0 ,0 ,0 ,-1 ,-1 ,-1 ,2 },
{3,-1 ,0 ,1 ,0 ,1 ,-2 ,-1 ,-1 },
{1,0 ,-1 ,-1 ,0 ,0 ,1 ,1 ,1 },
{2,3 ,1 ,1 ,1 ,-3 ,-2 ,-2 ,-1 }
};

for ( auto it : Ineq )
    model.addConstr( it[0] + it[1] * x[3] + it[2] * x[2] + it[3] * x[1] + it[4] * x[0] + it[5] * y[3] + it[6] * y[2] + it[7] * y[1] + it[8] * y[0] >= 0 );
}

void substitution(GRBModel& model, vector<GRBVar>& X, vector<GRBVar>& Y){

	for(int sbox_nr = 0 ; sbox_nr< SB; sbox_nr++){
		vector<GRBVar> tmpx (vector<GRBVar>(4)) ;
		vector<GRBVar> tmpy (vector<GRBVar>(4)) ;

		tmpx[3] = X[(sbox_nr*4)] ; 
		tmpx[2] = X[(sbox_nr*4) + 1] ;
		tmpx[1] = X[(sbox_nr*4) + 2] ;
		tmpx[0] = X[(sbox_nr*4) + 3 ] ;
		
		tmpy[3] = Y[(sbox_nr*4)] ; 
		tmpy[2] = Y[(sbox_nr*4) + 1] ;
		tmpy[1] = Y[(sbox_nr*4) + 2] ;
		tmpy[0] = Y[(sbox_nr*4) + 3 ] ;
        sbox(model, tmpx, tmpy) ;
	}
}

void linear_layer(vector<GRBVar>& X, vector<GRBVar>& Y){
    int P[STATE];
    for (int j=0; j<STATE-1; j++){
        P[((STATE>>2) * j) % (STATE-1)] = j;
    }
    P[STATE-1] = STATE-1;

    for (int i=0; i<STATE; i++){
        Y[i] = X[P[i]];
    }
}

void division_property(int rounds, vector<int> &active, vector<int> &not_balanced){
	GRBEnv env = GRBEnv();
    env.set(GRB_IntParam_LogToConsole, 0);
    env.set(GRB_IntParam_Threads, THREAD );
    //env.set(GRB_IntParam_PoolSolutions, 0);
    
    //initialize the variables
	GRBModel model = GRBModel(env);
	vector<vector<GRBVar>> X(rounds+1, vector<GRBVar>(STATE));
	for( int r = 0 ; r<rounds+1; r++){
		for( int i = 0; i<STATE; i++){
			X[r][i] = model.addVar(0, 1, 0, GRB_BINARY); 
		}
	}

	vector<GRBVar> Y(STATE);
	for( int r = 0; r<rounds; r++){
        linear_layer(X[r+1], Y) ;
        substitution(model, X[r], Y) ;  
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
        nv += X[rounds][i];
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
                /* print_trail(rounds, X, model); */
                for ( int x=0; x<STATE; x++){
                    if ( round( X[rounds][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                        counter++;
                        not_balanced.push_back(x);
                        //model.addConstr(X[rounds][x] == 0);
                        X[rounds][x].set(GRB_DoubleAttr_UB, 0);
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
void set_input_from_int(vector<int> &X, int v, int sb){
    for(int i=0; i<STATE; i++){
       X[i] = 1;
    }
    for(int i=0; i<4; i++){
        int j = (v >> i) & 0x01;
        if (j == 1){
            X[(4*sb) + i] = 0;
        }
    }
}
void linear_layer_2(vector<int>& X, vector<int>& Y){
    int P[STATE];
    for (int j=0; j<STATE-1; j++){
        P[((STATE>>2) * j) % (STATE-1)] = j;
    }
    P[STATE-1] = STATE-1;
    for (int i=0; i<STATE; i++){
            Y[P[i]] = X[i];
    }
}
void test(){
    int rounds = 9;
    FILE *fp = fopen("./data/Lin_K.txt", "w");
    vector<int > not_balanced;
    vector<int > balanced;
    
    //X -> L -> Y
    vector<int > X(STATE);
    vector<int > Y(STATE);

    vector<int > V;
    for (int i=0; i<SB; i++){
        for(int j=1; j<16; j++){
            set_input_from_int(X, j, i);
            linear_layer_2(X, Y);
            not_balanced.clear();
            balanced.clear();
            
            printf("running sbox = %d com = %d \n",i,j);
            print_prop(X, stdout);
            print_prop(Y, stdout);

            division_property(rounds, Y, not_balanced);
            printf("Balanced Bits: \n");
            for(int k=0; k<STATE; k++){
                if (std::find(not_balanced.begin(), not_balanced.end(), k) != not_balanced.end()){
                    continue;
                }
                else{
                    balanced.push_back(k);
                }
            }
            print_prop(X, fp);
            print_prop(Y, fp);
            print_vec(balanced, fp);
            fprintf(fp, "*******************************************************\n");
            
            print_vec(balanced, stdout);

        }
    }
    fclose(fp);
}
int main(){
    test();    
}
