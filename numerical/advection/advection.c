#include <stdio.h>
#include <math.h>

#define PI 3.141592653589793
#define NX 100
#define NT 100
#define XMIN 0.0
#define XMAX 2.0
#define H ((XMAX - XMIN) / (NX - 1))
#define K 0.01
const double a = 1.0;

double U[NT][NX];
double X[NX];

double eta(double x) {
    const int cond = x > 1.0;
    return cond * 1.0 + !cond * 2.0;
}

void upwind(int n) {
    const double courant = a*K/H;
    U[n][0] = U[n-1][0];
    for (int i = 1; i < NX; ++i) {
        U[n][i] = U[n-1][i] - courant * (U[n-1][i] - U[n-1][i-1]);
    }
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

    // Write results to files
    for (int n = 0; n < NT; ++n) {
        char filename[50];
        snprintf(filename, 49, "output_%d.dat", n);
        FILE *file = fopen(filename, "w");
        if (file == NULL) {
            perror("Error opening the file");
            return -1;
        }

        fprintf(file, "# X\tU[n=%d]\n", n);
        for (int i = 0; i < NX; i++) {
            fprintf(file, "%lf\t%lf\n", X[i], U[n][i]);
        }

        fclose(file);
        printf("File '%s' generated successfully.\n", filename);
    }


    return 0;
}

