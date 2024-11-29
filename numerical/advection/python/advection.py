import numpy as np

# Constants
NX = 100
NT = 1000
XMIN = 0.0
XMAX = 2.0
H = (XMAX - XMIN) / (NX - 1)
K = 0.4 * H
A = 1.0
COURANT = A * K / H

print(f"h = {H}, k = {K}, a = {A}, Courant = {COURANT}")

# Arrays
U = np.zeros((NT, NX))
X = np.linspace(XMIN, XMAX, NX)
FTRUE = np.zeros((NT, NX))

# Step function
def step(x):
    return 1.0 if x > 0.25 else 2.0

eta = np.vectorize(step)

def apply_explicit_scheme(n: int, alpha):
    for i in range(1, NX-1):
        UW = (U[n-1,i] - U[n-1,i-1]) / H
        DW = (U[n-1,i+1] - U[n-1,i]) / H
        U[n, i] = U[n-1,i] - A * K * (alpha * DW + (1.0-alpha) * UW)
    # Boundary conditions
    U[n,0] = U[n-1,0]
    U[n,NX-1] = U[n-1,NX-1]


# Numerical schemes

def upwind(n: int):
    apply_explicit_scheme(n, alpha=0.0)


def burgers_2(n):
    for i in range(1, NX):
        U[n, i] = U[n - 1, i] - 0.5 * K / H * (U[n - 1, i] ** 2 - U[n - 1, i - 1] ** 2)
    U[n, 0] = U[n - 1, 0]

# Initial condition
U[0, :] = eta(X)

# Exact solution
for t in range(NT):
    FTRUE[t, :] = eta(X - A * t * K)

# Simulation
for n in range(1, NT):
    upwind(n)

# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[X, FTRUE[40, :], U[40, :]], header="X FTRUE U", comments="")

print(f"File '{output_file}' generated.")
