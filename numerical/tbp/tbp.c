#include <stdio.h>
#include <math.h>

// Physical parameters
double ma = 1.0;  // Mass of first body
double mb = 1.0;  // Mass of second body
double m3 = 1.0;  // Mass of third body

double xa = 0.0;  // Initial x-position of first body
double ya = 0.0;  // Initial y-position of first body
double vx1 = 0.5; // Initial x-velocity of first body
double vy1 = 0.0; // Initial y-velocity of first body

double xb = 1.0;  // Initial x-position of second body
double yb = 0.0;  // Initial y-position of second body
double vx2 = -0.5;// Initial x-velocity of second body
double vy2 = 0.0; // Initial y-velocity of second body

double x3 = 0.0;  // Initial x-position of third body
double y3 = 1.0;  // Initial y-position of third body
double vx3 = 0.0; // Initial x-velocity of third body
double vy3 = -0.5;// Initial y-velocity of third body

// Simulation parameters
#define TFINAL 10.0
#define DT 0.01
#define NSTEPS (int)((TFINAL) / (DT))
#define G 1.0

struct particle
{
    double m;
    double x, y;
    double vx, vy;
};
typedef struct particle particle_t;

void compute_energy();
void set_initial_state(particle_t* pa, particle_t* pb, particle_t* pc)
{
    *pa = (particle_t){.m = 1.0, .x = 0.0, .y = 0.0, .vx = 0.5, .vy = 0.0};
    *pb = (particle_t){.m = 1.0, .x = 1.0, .y = 0.0, .vx = -0.5, .vy = 0.0};
    *pc = (particle_t){.m = 1.0, .x = 0.0, .y = 1.0, .vx = 0.0, .vy = -0.5};
}

// Function to compute the force between two bodies
void compute_force(double xa, double ya, double xb, double yb, double ma, double mb, double *fx, double *fy) {
    double dx = xb - xa;
    double dy = yb - ya;
    double r = sqrt(dx * dx + dy * dy);
    *fx = -G * ma * mb * dx / (r * r * r);
    *fy = -G * ma * mb * dy / (r * r * r);
}

void compute_force2(particle_t* pa, particle_t* pb, double *fx, double *fy)
{
    compute_force(pa->x, pa->y, pb->x, pb->y, pa->m, pb->m, fx, fy);
}

void euler_integration2(particle_t* pa, particle_t* pb, particle_t* pc)
{
    for (int i = 1; i < NSTEPS; i++) {
        double fxa, fya, fxb, fyb, fxc, fyc;
        compute_force2(&pb[i-1], &pc[i-1], &fxa, &fya);
        compute_force2(&pa[i-1], &pc[i-1], &fxb, &fyb);
        compute_force2(&pa[i-1], &pb[i-1], &fxc, &fyc);
    }
}

// Euler integration method
void euler_integration() {
    FILE *fp = fopen("three_body_euler.dat", "w");
    fprintf(fp, "# time xa ya xb yb x3 y3\n");

    for (int i = 0; i < NSTEPS; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(xa, ya, xb, yb, ma, mb, &fx1, &fy1);
        compute_force(xa, ya, x3, y3, ma, m3, &fx2, &fy2);
        compute_force(xb, yb, x3, y3, mb, m3, &fx3, &fy3);

        xa += vx1 * DT;
        ya += vy1 * DT;
        vx1 += (fx1 / ma + fx2 / ma) * DT;
        vy1 += (fy1 / ma + fy2 / ma) * DT;

        xb += vx2 * DT;
        yb += vy2 * DT;
        vx2 += (fx1 / mb + fx3 / mb) * DT;
        vy2 += (fy1 / mb + fy3 / mb) * DT;

        x3 += vx3 * DT;
        y3 += vy3 * DT;
        vx3 += (fx2 / m3 + fx3 / m3) * DT;
        vy3 += (fy2 / m3 + fy3 / m3) * DT;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * DT, xa, ya, xb, yb, x3, y3);
    }

    fclose(fp);
}

// Leapfrog integration method
void leapfrog_integration() {
    FILE *fp = fopen("three_body_leapfrog.dat", "w");
    fprintf(fp, "# time xa ya xb yb x3 y3\n");

    double vx1_half = vx1, vy1_half = vy1, vx2_half = vx2, vy2_half = vy2, vx3_half = vx3, vy3_half = vy3;

    for (int i = 0; i < NSTEPS; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(xa, ya, xb, yb, ma, mb, &fx1, &fy1);
        compute_force(xa, ya, x3, y3, ma, m3, &fx2, &fy2);
        compute_force(xb, yb, x3, y3, mb, m3, &fx3, &fy3);

        xa += vx1_half * DT;
        ya += vy1_half * DT;
        vx1_half += (fx1 / ma + fx2 / ma) * DT;
        vy1_half += (fy1 / ma + fy2 / ma) * DT;
        vx1 = vx1_half;
        vy1 = vy1_half;

        xb += vx2_half * DT;
        yb += vy2_half * DT;
        vx2_half += (fx1 / mb + fx3 / mb) * DT;
        vy2_half += (fy1 / mb + fy3 / mb) * DT;
        vx2 = vx2_half;
        vy2 = vy2_half;

        x3 += vx3_half * DT;
        y3 += vy3_half * DT;
        vx3_half += (fx2 / m3 + fx3 / m3) * DT;
        vy3_half += (fy2 / m3 + fy3 / m3) * DT;
        vx3 = vx3_half;
        vy3 = vy3_half;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * DT, xa, ya, xb, yb, x3, y3);
    }

    fclose(fp);
}

// Runge-Kutta 4th order integration method
void rk4_integration() {
    FILE *fp = fopen("three_body_rk4.dat", "w");
    fprintf(fp, "# time xa ya xb yb x3 y3\n");

    for (int i = 0; i < NSTEPS; i++) {
        double fx1, fy1, fx2, fy2, fx3, fy3;
        compute_force(xa, ya, xb, yb, ma, mb, &fx1, &fy1);
        compute_force(xa, ya, x3, y3, ma, m3, &fx2, &fy2);
        compute_force(xb, yb, x3, y3, mb, m3, &fx3, &fy3);

        // Runge-Kutta 4th order steps
        double k1vx1 = (fx1 / ma + fx2 / ma) * DT;
        double k1vy1 = (fy1 / ma + fy2 / ma) * DT;
        double k1vx2 = (fx1 / mb + fx3 / mb) * DT;
        double k1vy2 = (fy1 / mb + fy3 / mb) * DT;
        double k1vx3 = (fx2 / m3 + fx3 / m3) * DT;
        double k1vy3 = (fy2 / m3 + fy3 / m3) * DT;

        double k2vx1 = (fx1 / ma + fx2 / ma) * DT;
        double k2vy1 = (fy1 / ma + fy2 / ma) * DT;
        double k2vx2 = (fx1 / mb + fx3 / mb) * DT;
        double k2vy2 = (fy1 / mb + fy3 / mb) * DT;
        double k2vx3 = (fx2 / m3 + fx3 / m3) * DT;
        double k2vy3 = (fy2 / m3 + fy3 / m3) * DT;

        double k3vx1 = (fx1 / ma + fx2 / ma) * DT;
        double k3vy1 = (fy1 / ma + fy2 / ma) * DT;
        double k3vx2 = (fx1 / mb + fx3 / mb) * DT;
        double k3vy2 = (fy1 / mb + fy3 / mb) * DT;
        double k3vx3 = (fx2 / m3 + fx3 / m3) * DT;
        double k3vy3 = (fy2 / m3 + fy3 / m3) * DT;

        double k4vx1 = (fx1 / ma + fx2 / ma) * DT;
        double k4vy1 = (fy1 / ma + fy2 / ma) * DT;
        double k4vx2 = (fx1 / mb + fx3 / mb) * DT;
        double k4vy2 = (fy1 / mb + fy3 / mb) * DT;
        double k4vx3 = (fx2 / m3 + fx3 / m3) * DT;
        double k4vy3 = (fy2 / m3 + fy3 / m3) * DT;

        xa += (vx1 + (k1vx1 + 2 * k2vx1 + 2 * k3vx1 + k4vx1) / 6) * DT;
        ya += (vy1 + (k1vy1 + 2 * k2vy1 + 2 * k3vy1 + k4vy1) / 6) * DT;
        vx1 += (k1vx1 + 2 * k2vx1 + 2 * k3vx1 + k4vx1) / 6;
        vy1 += (k1vy1 + 2 * k2vy1 + 2 * k3vy1 + k4vy1) / 6;

        xb += (vx2 + (k1vx2 + 2 * k2vx2 + 2 * k3vx2 + k4vx2) / 6) * DT;
        yb += (vy2 + (k1vy2 + 2 * k2vy2 + 2 * k3vy2 + k4vy2) / 6) * DT;
        vx2 += (k1vx2 + 2 * k2vx2 + 2 * k3vx2 + k4vx2) / 6;
        vy2 += (k1vy2 + 2 * k2vy2 + 2 * k3vy2 + k4vy2) / 6;

        x3 += (vx3 + (k1vx3 + 2 * k2vx3 + 2 * k3vx3 + k4vx3) / 6) * DT;
        y3 += (vy3 + (k1vy3 + 2 * k2vy3 + 2 * k3vy3 + k4vy3) / 6) * DT;
        vx3 += (k1vx3 + 2 * k2vx3 + 2 * k3vx3 + k4vx3) / 6;
        vy3 += (k1vy3 + 2 * k2vy3 + 2 * k3vy3 + k4vy3) / 6;

        fprintf(fp, "%f %f %f %f %f %f %f\n", i * DT, xa, ya, xb, yb, x3, y3);
    }

    fclose(fp);
}

int main() {
    particle_t pa[NSTEPS];
    particle_t pb[NSTEPS];
    particle_t pc[NSTEPS];

    set_initial_state(&pa[0], &pb[0], &pc[0]);


    euler_integration();
    leapfrog_integration();
    rk4_integration();
    return 0;
}
