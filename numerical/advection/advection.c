#include <stdio.h>
#include <math.h>

#define PI 3.141592653589793
#define NX 100
#define NT 100
#define XMIN 0.0
#define XMAX 2.0
#define H ((XMAX - XMIN) / (NX - 1))
#define K 0.01
#define A 1.0
#define COURANT ((A)*(K)/(H))

double U[NT][NX];
double X[NX];

double eta(double x) {
    const int cond = x > 1.0;
    return cond * 1.0 + !cond * 2.0;
}

void apply_explicit_scheme(int n, double alpha) {
    for (int i = 1; i < NX; ++i) {
        const double UW = U[n-1][i] - U[n-1][i-1];
        const double DW = U[n-1][i+1] - U[n-1][i];
        U[n][i] = U[n-1][i] - COURANT * (alpha * DW + (1.0-alpha) * UW);
    }
    // Boundary conditions
    U[n][0] = U[n-1][0];
    U[n][NX-1] = U[n-1][NX-1];
}

void upwind(int n) {
    apply_explicit_scheme(n, 0.0);
}

void downwind(int n) {
    apply_explicit_scheme(n, 1.0);
}

int main() {

    // Fill X values
    X[0] = XMIN;
    for (int i = 1; i < NX; i++) {
        X[i] = X[i-1] + H;
    }
    // Fill initial condition u(x, t=0)
    for (int i = 0; i < NX; i++) {
        U[0][i] = eta(X[i]);
    }

    // Run simulation
    for (int n = 1; n < NT; ++n) {
        upwind(n);
    }

    // Write results to file
    const char* filename = "output.dat";
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening the file");
        return -1;
    }

    fprintf(file, "X\tU[n=0]\tU[n=10]\tU[n=20]\tU[n=30]\tU[n=40]\n");
    for (int i = 0; i < NX; i++) {
        fprintf(file, "%lf\t%lf\t%lf\t%lf\t%lf\t%lf\n", X[i], U[0][i], U[10][i], U[20][i], U[30][i], U[40][i]);
    }

    fclose(file);
    printf("File '%s' generated successfully.\n", filename);


    return 0;
}

