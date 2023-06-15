void linear_layer(GRBModel& model, vector<GRBVar>& X, vector<GRBVar>& Y, const int rot1, const int rot2){
    int i;
        
    //variables to copy iputs in three  X_i -> (A_0i, A_1i, A_2i)
    vector<vector<GRBVar>> A(3, vector<GRBVar>(64));
    for(i = 0; i<64;i++){
        A[0][i] = model.addVar(0, 1, 0, GRB_BINARY);
        A[1][i] = model.addVar(0, 1, 0, GRB_BINARY);
        A[2][i] = model.addVar(0, 1, 0, GRB_BINARY);
    }
    //COPY
    for(i = 0; i<64; i++){
        model.addConstr(X[i] == A[0][i] + A[1][i] + A[2][i]) ;
    }

    //XOR three variables Y_i = A_0i + A_1i + A_2i
    for(i = 0; i<64; i++){
        model.addConstr(Y[i] == A[0][i] + A[1][(64-rot1 + i) % 64] + A[2][(64- rot2 + i) % 64]);
    }
}

// [x0, x1, x2, x3, x4] --> [y0, y1, y2, y3, y4]
void sbox(GRBModel& model, vector<GRBVar>& x, vector<GRBVar>& y) {

    int i ;
    
    //x0 coppied 7 times
    vector<GRBVar> x0(vector<GRBVar>(7)) ;
    for( i = 0 ; i<7; i++) x0[i] = model.addVar(0, 1, 0, GRB_BINARY);

    //x1 coppied 12 times
    vector<GRBVar> x1(vector<GRBVar>(12)) ;
    for( i = 0 ; i<12; i++) x1[i] = model.addVar(0, 1, 0, GRB_BINARY);

    //x2 coppied 7 times
    vector<GRBVar> x2(vector<GRBVar>(7)) ;
    for( i = 0 ; i<7; i++) x2[i] = model.addVar(0, 1, 0, GRB_BINARY);

    //x3 coppied 8 times
    vector<GRBVar> x3(vector<GRBVar>(8)) ;
    for( i = 0 ; i<8; i++) x3[i] = model.addVar(0, 1, 0, GRB_BINARY);

    //x4 coppied 8 times 
    vector<GRBVar> x4(vector<GRBVar>(8)) ;
    for( i = 0 ; i<8; i++) x4[i] = model.addVar(0, 1, 0, GRB_BINARY);

    //To compute 11 and operation (a_k = xixj)
    vector<GRBVar> a(vector<GRBVar>(11)) ;
    for( i = 0 ; i<11; i++) a[i] = model.addVar(0, 1, 0, GRB_BINARY);


    //copy 
    model.addConstr(x0[0] + x0[1] + x0[2] + x0[3] + x0[4] + x0[5] + x0[6] == x[0]) ;
    model.addConstr(x1[0] + x1[1] + x1[2] + x1[3] + x1[4] + x1[5] + x1[6] + x1[7] + x1[8] + x1[9] + x1[10] + x1[11] == x[1]);
    model.addConstr(x2[0] + x2[1] + x2[2] + x2[3] + x2[4] + x2[5] + x2[6] == x[2]);
    model.addConstr(x3[0] + x3[1] + x3[2] + x3[3] + x3[4] + x3[5] + x3[6] + x3[7] == x[3]);
    model.addConstr(x4[0] + x4[1] + x4[2] + x4[3] + x4[4] + x4[5] + x4[6] + x4[7] == x[4]);

    //y0 = x4*x1 + x2+x1 + x1x0 + x3 + x2 + x1 + x0
    model.addConstr(a[0] >= x4[0]); model.addConstr(a[0] >= x1[0]); model.addConstr(x4[0] + x1[0] >= a[0]); //  x4 * x1
    model.addConstr(a[1] >= x2[0]); model.addConstr(a[1] >= x1[1]); model.addConstr(x2[0] + x1[1] >= a[1]); //  x2 * x1
    model.addConstr(a[2] >= x0[0]); model.addConstr(a[2] >= x1[2]); model.addConstr(x0[0] + x1[2] >= a[2]); //  x0 * x1
    model.addConstr(y[0] == a[0] + a[1] + a[2] + x3[0] + x2[1] + x1[3] + x0[1]) ;

    //y1 = x3x2 + x3x1 + x2x1 + x4 + x3 + x2 + x1 + x0
    model.addConstr(a[3] >= x3[1]); model.addConstr(a[3] >= x2[2]);  model.addConstr(x3[1] + x2[2] >= a[3]); // x3 * x2
    model.addConstr(a[4] >= x3[2]); model.addConstr(a[4] >= x1[4]);  model.addConstr(x3[2] + x1[4] >= a[4]); // x3 * x1
    model.addConstr(a[5] >= x2[3]); model.addConstr(a[5] >= x1[5]);  model.addConstr(x2[3] + x1[5] >= a[5]); // x2 * x1
    model.addConstr(y[1] == a[3] + a[4] + a[5] + x4[1] + x3[3] + x2[4] + x1[6] + x0[2]);

    //y2 = x4x3 + x4 + x2 + x1 + 1
    model.addConstr(a[6] >= x4[2]); model.addConstr(a[6] >= x3[4]); model.addConstr(x4[2] + x3[4] >= a[6]); // x4 * x3
    model.addConstr(y[2] == a[6] + x4[3] + x2[5] + x1[7]) ;

    //y3 = x4x0 + x3x0 + x4 + x3 + x2 + x1 + x0
    model.addConstr(a[7] >= x4[4]); model.addConstr(a[7] >= x0[3]); model.addConstr(x4[4] + x0[3] >= a[7]);//  x4 * x0
    model.addConstr(a[8] >= x3[5]); model.addConstr(a[8] >= x0[4]); model.addConstr(x3[5] + x0[4] >= a[8]);//  x3 * x0
    model.addConstr(y[3] == a[7] + a[8] + x4[5] + x3[6] + x2[6] + x1[8] + x0[5]) ;

    //y4 = x4x1 + x0x1 + x4 + x3 + x1
    model.addConstr(a[9] >= x4[6]); model.addConstr(a[9] >= x1[9]); model.addConstr(x4[6] + x1[9] >= a[9]);   //  x4 * x1
    model.addConstr(a[10] >= x0[6]); model.addConstr(a[10] >= x1[10]); model.addConstr(x0[6] + x1[10] >= a[10]);//  x0 * x1
    model.addConstr(y[4] == a[9] + a[10] + x4[7] + x3[7] + x1[11] );
}


