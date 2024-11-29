import numpy as np

# Constants
NX = 150
NT = 1000
XMIN = 0.0
XMAX = 1.0
H = (XMAX - XMIN) / (NX - 1)
K = 0.4 * H
A = 1.0
COURANT = A * K / H
TF = 40

print(f"h = {H}, k = {K}, a = {A}, Courant = {COURANT}, TFinal = {TF * K}")

# Global arrays
U = np.zeros((NT, NX))
X = np.linspace(XMIN, XMAX, NX)
FTRUE = np.zeros((NT, NX))

# Step function
def step(x):
    return 1.0 if x > 0.25 else 2.0

# Initial condition
eta = np.vectorize(step)
U[0, :] = eta(X)

# Numerical schemes
def upwind_1():
    for n in range(1, NT):
        for i in range(1, NX-1):
            U[n, i] = U[n-1,i] - (K / H) * U[n-1,i] * (U[n-1,i] - U[n-1,i-1])
    # Periodic boundary conditions
    U[n, 0] = U[n-1, 0] - (K / H) * (U[n-1, 0] * (U[n-1, 0] - U[n-1, NX-2]))
    U[n, NX-1] = U[n, 0]

# Exact solution
for t in range(NT):
    FTRUE[t, :] = eta(X - A * t * K)

### Run simulation
upwind_1()
#upwind_2()
#conservative_upwind()
#conservative_lax_friedrichs()


# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[X, FTRUE[TF, :], U[TF, :]], header="X FTRUE U", comments="")

print(f"File '{output_file}' generated.")
