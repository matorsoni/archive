import numpy as np

# Constants
NX = 150
NT = 1000
XMIN = 0.0
XMAX = 2.0
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

def apply_explicit_scheme(n: int, alpha):
    for i in range(1, NX-1):
        UW = (U[n-1,i] - U[n-1,i-1]) / H
        DW = (U[n-1,i+1] - U[n-1,i]) / H
        U[n, i] = U[n-1,i] - A * K * (alpha * DW + (1.0-alpha) * UW)
    # Boundary conditions
    U[n,0] = U[n-1,0]
    U[n,NX-1] = U[n-1,NX-1]

# Numerical schemes
def upwind():
    for n in range(1, NT):
        apply_explicit_scheme(n, alpha=0.0)

def downwind():
    for n in range(1, NT):
        apply_explicit_scheme(n, alpha=1.0)

def centered():
    for n in range(1, NT):
        apply_explicit_scheme(n, alpha=0.5)

def lax_friedrich():
    alpha = 0.5*(1.0 - 1.0/COURANT)
    for n in range(1, NT):
        apply_explicit_scheme(n, alpha)

def lax_wendroff():
    alpha = 0.5*(1.0 - COURANT)
    for n in range(1, NT):
        apply_explicit_scheme(n, alpha)

def wendroff():
    # Construct Ae and Ad using sparse diagonal matrices
    e = np.ones(NX)
    I = np.arange(NX)
    Ae = np.eye(NX) + (COURANT / 2) * np.diag(-1 * e[:-1], -1) + (COURANT / 2) * np.diag(e[:-1], 1)
    Ad = np.eye(NX) + (COURANT / 2) * np.diag(e[:-1], -1) + (COURANT / 2) * np.diag(-1 * e[:-1], 1)

    for n in range(1, NT):
        u = U[n-1, :]
        rhs = Ad @ u[I]
        rhs[0] += COURANT
        rhs[-1] -= (1 / 2) * COURANT
        # Solve for u(I)
        u[I] = np.linalg.solve(Ae, rhs)
        U[n, :] = u[I]


#
#def burgers_2(n):
#    for i in range(1, NX):
#        U[n, i] = U[n - 1, i] - 0.5 * K / H * (U[n - 1, i] ** 2 - U[n - 1, i - 1] ** 2)
#    U[n, 0] = U[n - 1, 0]
#

# Exact solution
for t in range(NT):
    FTRUE[t, :] = eta(X - A * t * K)

### Run simulation
#upwind()
#lax_friedrich()
#lax_wendroff()
wendroff()

# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[X, FTRUE[TF, :], U[TF, :]], header="X FTRUE U", comments="")

print(f"File '{output_file}' generated.")
