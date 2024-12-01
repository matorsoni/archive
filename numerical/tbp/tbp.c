#include <stdio.h>
#include <math.h>

// Physical parameters
double m1 = 1.0;  // Mass of first body
double m2 = 1.0;  // Mass of second body
double m3 = 1.0;  // Mass of third body

double x1 = 0.0;  // Initial x-position of first body
double y_1 = 0.0;  // Initial y-position of first body
double vx1 = 0.5; // Initial x-velocity of first body
double vy1 = 0.0; // Initial y-velocity of first body

double x2 = 1.0;  // Initial x-position of second body
double y2 = 0.0;  // Initial y-position of second body
double vx2 = -0.5;// Initial x-velocity of second body
double vy2 = 0.0; // Initial y-velocity of second body

double x3 = 0.0;  // Initial x-position of third body
double y3 = 1.0;  // Initial y-position of third body
double vx3 = 0.0; // Initial x-velocity of third body
double vy3 = -0.5;// Initial y-velocity of third body

double G = 1.0;   // Gravitational constant

// Simulation parameters
#define t_final 10.0 // Final simulation time
#define dt 0.01      // Time step
#define n_steps (int)((t_final) / (dt)) // Number of time steps

// Function to compute the force between two bodies
void compute_force(double x1, double y_1, double x2, double y2, double m1, double m2, double *fx, double *fy) {
    double dx = x2 - x1;
    double dy = y2 - y_1;
    double r = sqrt(dx * dx + dy * dy);
    *fx = -G * m1 * m2 * dx / (r * r * r);
    *fy = -G * m1 * m2 * dy / (r * r * r);
}

// Euler integration method
void euler_integration() {
    FILE *fp = fopen("three_body_euler.dat", "w");
    fprintf(fp, "# time x1 y_1 x2 y2 x3 y3\n");

    for (int i = 0; i < n_steps; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(x1, y_1, x2, y2, m1, m2, &fx1, &fy1);
        compute_force(x1, y_1, x3, y3, m1, m3, &fx2, &fy2);
        compute_force(x2, y2, x3, y3, m2, m3, &fx3, &fy3);

        x1 += vx1 * dt;
        y_1 += vy1 * dt;
        vx1 += (fx1 / m1 + fx2 / m1) * dt;
        vy1 += (fy1 / m1 + fy2 / m1) * dt;

        x2 += vx2 * dt;
        y2 += vy2 * dt;
        vx2 += (fx1 / m2 + fx3 / m2) * dt;
        vy2 += (fy1 / m2 + fy3 / m2) * dt;

        x3 += vx3 * dt;
        y3 += vy3 * dt;
        vx3 += (fx2 / m3 + fx3 / m3) * dt;
        vy3 += (fy2 / m3 + fy3 / m3) * dt;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * dt, x1, y_1, x2, y2, x3, y3);
    }

    fclose(fp);
}

// Leapfrog integration method
void leapfrog_integration() {
    FILE *fp = fopen("three_body_leapfrog.dat", "w");
    fprintf(fp, "# time x1 y_1 x2 y2 x3 y3\n");

    double vx1_half = vx1, vy1_half = vy1, vx2_half = vx2, vy2_half = vy2, vx3_half = vx3, vy3_half = vy3;

    for (int i = 0; i < n_steps; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(x1, y_1, x2, y2, m1, m2, &fx1, &fy1);
        compute_force(x1, y_1, x3, y3, m1, m3, &fx2, &fy2);
        compute_force(x2, y2, x3, y3, m2, m3, &fx3, &fy3);

        x1 += vx1_half * dt;
        y_1 += vy1_half * dt;
        vx1_half += (fx1 / m1 + fx2 / m1) * dt;
        vy1_half += (fy1 / m1 + fy2 / m1) * dt;
        vx1 = vx1_half;
        vy1 = vy1_half;

        x2 += vx2_half * dt;
        y2 += vy2_half * dt;
        vx2_half += (fx1 / m2 + fx3 / m2) * dt;
        vy2_half += (fy1 / m2 + fy3 / m2) * dt;
        vx2 = vx2_half;
        vy2 = vy2_half;

        x3 += vx3_half * dt;
        y3 += vy3_half * dt;
        vx3_half += (fx2 / m3 + fx3 / m3) * dt;
        vy3_half += (fy2 / m3 + fy3 / m3) * dt;
        vx3 = vx3_half;
        vy3 = vy3_half;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * dt, x1, y_1, x2, y2, x3, y3);
    }

    fclose(fp);
}

// Runge-Kutta 4th order integration method
void rk4_integration() {
    FILE *fp = fopen("three_body_rk4.dat", "w");
    fprintf(fp, "# time x1 y_1 x2 y2 x3 y3\n");

    for (int i = 0; i < n_steps; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(x1, y_1, x2, y2, m1, m2, &fx1, &fy1);
        compute_force(x1, y_1, x3, y3, m1, m3, &fx2, &fy2);
        compute_force(x2, y2, x3, y3, m2, m3, &fx3, &fy3);

        // Runge-Kutta 4th order steps
        double k1vx1 = (fx1 / m1 + fx2 / m1) * dt;
        double k1vy1 = (fy1 / m1 + fy2 / m1) * dt;
        double k1vx2 = (fx1 / m2 + fx3 / m2) * dt;
        double k1vy2 = (fy1 / m2 + fy3 / m2) * dt;
        double k1vx3 = (fx2 / m3 + fx3 / m3) * dt;
        double k1vy3 = (fy2 / m3 + fy3 / m3) * dt;

        double k2vx1 = (fx1 / m1 + fx2 / m1) * dt;
        double k2vy1 = (fy1 / m1 + fy2 / m1) * dt;
        double k2vx2 = (fx1 / m2 + fx3 / m2) * dt;
        double k2vy2 = (fy1 / m2 + fy3 / m2) * dt;
        double k2vx3 = (fx2 / m3 + fx3 / m3) * dt;
        double k2vy3 = (fy2 / m3 + fy3 / m3) * dt;

        double k3vx1 = (fx1 / m1 + fx2 / m1) * dt;
        double k3vy1 = (fy1 / m1 + fy2 / m1) * dt;
        double k3vx2 = (fx1 / m2 + fx3 / m2) * dt;
        double k3vy2 = (fy1 / m2 + fy3 / m2) * dt;
        double k3vx3 = (fx2 / m3 + fx3 / m3) * dt;
        double k3vy3 = (fy2 / m3 + fy3 / m3) * dt;

        double k4vx1 = (fx1 / m1 + fx2 / m1) * dt;
        double k4vy1 = (fy1 / m1 + fy2 / m1) * dt;
        double k4vx2 = (fx1 / m2 + fx3 / m2) * dt;
        double k4vy2 = (fy1 / m2 + fy3 / m2) * dt;
        double k4vx3 = (fx2 / m3 + fx3 / m3) * dt;
        double k4vy3 = (fy2 / m3 + fy3 / m3) * dt;

        x1 += (vx1 + (k1vx1 + 2 * k2vx1 + 2 * k3vx1 + k4vx1) / 6) * dt;
        y_1 += (vy1 + (k1vy1 + 2 * k2vy1 + 2 * k3vy1 + k4vy1) / 6) * dt;
        vx1 += (k1vx1 + 2 * k2vx1 + 2 * k3vx1 + k4vx1) / 6;
        vy1 += (k1vy1 + 2 * k2vy1 + 2 * k3vy1 + k4vy1) / 6;

        x2 += (vx2 + (k1vx2 + 2 * k2vx2 + 2 * k3vx2 + k4vx2) / 6) * dt;
        y2 += (vy2 + (k1vy2 + 2 * k2vy2 + 2 * k3vy2 + k4vy2) / 6) * dt;
        vx2 += (k1vx2 + 2 * k2vx2 + 2 * k3vx2 + k4vx2) / 6;
        vy2 += (k1vy2 + 2 * k2vy2 + 2 * k3vy2 + k4vy2) / 6;

        x3 += (vx3 + (k1vx3 + 2 * k2vx3 + 2 * k3vx3 + k4vx3) / 6) * dt;
        y3 += (vy3 + (k1vy3 + 2 * k2vy3 + 2 * k3vy3 + k4vy3) / 6) * dt;
        vx3 += (k1vx3 + 2 * k2vx3 + 2 * k3vx3 + k4vx3) / 6;
        vy3 += (k1vy3 + 2 * k2vy3 + 2 * k3vy3 + k4vy3) / 6;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * dt, x1, y_1, x2, y2, x3, y3);
    }

    fclose(fp);
}

int main() {
    euler_integration();
    leapfrog_integration();
    rk4_integration();
    return 0;
}
