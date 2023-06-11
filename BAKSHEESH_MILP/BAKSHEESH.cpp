#include "utility.h"

void sbox(GRBModel& model, vector<GRBVar>& x, vector<GRBVar>& y)
{    
    //found by sage
    int Ineq[][9] = {
        {0,1 ,1 ,1 ,1 ,-1 ,-1 ,-1 ,-1 },
        {0,-2 ,-1 ,-1 ,-1 ,2 ,2 ,2 ,2 },
        {4,-1 ,-2 ,-3 ,-3 ,2 ,1 ,1 ,1 },
        {4,1 ,-1 ,-1 ,3 ,-1 ,-2 ,-2 ,-1},
        {3,2 ,-1 ,3 ,-1 ,-1 ,-1 ,-2 ,-1},
        {2,1 ,2 ,0 ,0 ,-2 ,-1 ,-1 ,-1},
        {5,-2 ,-3 ,-2 ,-3 ,1 ,1 ,2 ,1},
        {4,-1 ,-3 ,-3 ,-2 ,1 ,2 ,2 ,1}
    };
    
    //given in paper
    /* int Ineq[][9] = { */
    /*     {0,-2 ,-1 ,-1 ,-1 ,2 ,2 ,2 ,2 }, */
    /*     {4,-1 ,-2 ,-3 ,-3 ,2 ,1 ,1 ,1 }, */
    /*     {5,-2 ,-3 ,-2 ,-3 ,1 ,1 ,2 ,1}, */
    /*     {4,-1 ,-3 ,-3 ,-2 ,1 ,2 ,2 ,1}, */
    /*     {3, -1, -1, -2, -1, 1,0,0,1}, */
    /*     {0,-2,-1,-1,-2,3,3,2,3} */
    /* }; */

for ( auto it : Ineq )
    model.addConstr( it[0] + it[1] * x[3] + it[2] * x[2] + it[3] * x[1] + it[4] * x[0] + it[5] * y[3] + it[6] * y[2] + it[7] * y[1] + it[8] * y[0] >= 0 );
}

void substitution(GRBModel& model, vector<GRBVar>& X, vector<GRBVar>& Y){

	for(int sbox_nr = 0 ; sbox_nr< 32; sbox_nr++){

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

	/* for(i=0; i<STATE; i++){ */
	/*     Y[P[i]] = X[i]; */
	/* } */
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
    
    model.write("./data/baksheesh.lp");
    
    bool flag;
    int counter = 0;
    cout << "Not Balanced:\n" << endl;
    while(counter < STATE){
    	model.update();
        model.optimize();
        if ( model.get( GRB_IntAttr_Status ) == GRB_OPTIMAL ){
            double obj_value = round(model.get(GRB_DoubleAttr_ObjVal));
            cout << "Obj " << obj_value << endl; 
            /* scanf("continue?"); */
            if (obj_value > 1){
                flag = true;
                break;
            }
            
            else{
                for ( int x=0; x<STATE; x++){
                    if ( round( X[rounds][x].get( GRB_DoubleAttr_Xn ) ) == 1 ){
                        counter++;
                        not_balanced.push_back(x);
                        //model.addConstr(X[rounds][x] == 0);
                        X[rounds][x].set(GRB_DoubleAttr_UB, 0);
                        cout << x << " " << counter << endl;
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
    if (flag == true){
        cout << "Integral Distinguisher Found\n";
    }
}
int even_polynomial(int rounds, vector<int> &input, vector<int> &output){
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
        if ( input[i] == 0 ){
            model.addConstr( X[0][i] == 0 );
        }
        else{
            model.addConstr( X[0][i] == 1 );
        }
    }
    
    //output constrait
    for ( int i = 0; i < STATE; i++ ){
        if ( output[i] == 1 ){
            model.addConstr( X[rounds][i] == 1 );
        }
        else{
            model.addConstr( X[rounds][i] == 0 );
        }
    }

    model.write("./data/baksheesh.lp");
    model.optimize();
    int balanced = 0;
    if( model.get( GRB_IntAttr_Status ) == GRB_OPTIMAL){
    	double time = model.get(GRB_DoubleAttr_Runtime );
        cout << "Time Used: " << time << "sec" << endl;
        /* print_trail(rounds, X, model); */
    }
    else if( model.get( GRB_IntAttr_Status ) == GRB_INFEASIBLE ){
        cout << "Integral Distinguisher Found\n";
        balanced = 1;
    }
    else{
        cout << "Other status " << GRB_IntAttr_Status <<  endl;
        exit(-1);
    }

    return balanced;
}

void set_input(vector<int> &active, int i){
    for(int i=0; i<STATE; i++){
       active[i] = 1;
    }
    active[i] = 0;
}
void set_output(vector<int> &active, int *V, int sbox_no){
    for(int i=0; i<STATE; i++){
       active[i] = 0;
    }
    for(int i=0; i<2; i++){
        active[(4*sbox_no) + i] = 1;
    }
}
void print_prop(vector<int> &A){
    for (int i=0; i<STATE; i++){
        printf("%d",A[i]);
    }
    printf("\n");
}
void test_poly(){
    int rounds = 13;
    vector<int> input(STATE);
    vector<int> output(STATE);

    set_input(input,  0);
    int V[6][2] = {{0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3}}; 
    
    for(int j=0; j<STATE; j++){
        for(int s=0; s<32; s++){
            for(int i=0; i<6; i++){
                set_output(output, V[i], s);
                print_prop(input);
                print_prop(output);
                int balanced = even_polynomial(rounds, input, output);
                cout << j << " " << V[i][0] << " " << V[i][1] << ":";
                if (balanced == 1){
                    cout << "balanced" << endl;
                    scanf("continue?");
                }
                else{
                    cout << "unknown" << endl;
                }
            }
        }
    }
}
void test(){
    int rounds = 13;
    vector<int > not_balanced;
    vector<int > active(STATE);
    set_input(active, 0);
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
    /* test(); */    
    test_poly();    
}
