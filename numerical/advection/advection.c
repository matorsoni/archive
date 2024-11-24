#include <stdio.h>
#include <math.h>

#define PI 3.141592653589793
#define NX 100
#define NT 100

double U[NT][NX];
double X[NX];

double eta(double x) {
    const int cond = x > 1.0;
    return cond * 1.0 + !cond * 2.0;
}

int main() {
    const char *filename = "output.dat";
    const double x_min = 0.0;
    const double x_max = 2.0;
    const double h = (x_max - x_min) / (NX - 1);
    const double k = 0.01;

    // Fill X values
    X[0] = x_min;
    for (int i = 1; i < NX; i++) {
        X[i] = X[i-1] + h;
    }
    // Fill initial condition u(x, t=0)
    for (int i = 0; i < NX; i++) {
        U[0][i] = eta(X[i]);
    }


    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        perror("Error opening the file");
        return -1;
    }

    // Write results to file
    fprintf(file, "# X\tU\n");
    for (int i = 0; i < NX; i++) {
        fprintf(file, "%lf\t%lf\n", X[i], U[0][i]);
    }

    fclose(file);

    printf("File '%s' generated successfully.\n", filename);

    return 0;
}

