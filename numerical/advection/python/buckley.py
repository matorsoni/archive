import numpy as np

# Parameters
ax = 0
bx = 1
m = 100
h = (bx - ax) / (m + 1)
k = 0.4 * h
tfinal = 0.2
nsteps = int(np.round(tfinal / k))

# Constant vectors
X = np.linspace(ax, bx, m + 2)
I = np.arange(1, m + 1)
I_ = np.arange(1, m)

def step(X):
    return 0.8 - 0.5 * (X >= 0.2).astype(float)

def gauss(X):
    var = 400
    return np.exp(-var*(X-0.2)**2) + 1

# Buckley-Leverett function for water flux wrt saturation
a = 0.5
def f_water(X):
    return X**2 / (X**2 + a*(1-X)**2)

def df_water(X):
    return (2*a*X*(1-X)) / (X**2 + a*(1-X)**2)**2

# Initial condition
eta = step
U_lax = eta(X)
U = eta(X)

# Run simulation with Dirichlet boundary conditions (reflective)
for n in range(nsteps):

    # Regular upwind
    U[I] = U[I] - (k/h)*df_water(U[I])*(U[I] - U[I-1])

    # Delayed upwind
    #U[I] = U[I] - (k/h)*df_water(U[I-1])*(U[I] - U[I-1])

    # Conservative Upwind
    #U[I] = U[I] - (k/h) * (f_water(U[I]) - f_water(U[I-1]))

    U[0] = U[1]
    U[-1] = U[-2]

    # Lax-Friedrichs
    U_lax[I_] = 0.5 * (U_lax[I_-1] + U_lax[I_+1]) - (k/(2*h)) * (f_water(U_lax[I_+1]) - f_water(U_lax[I_-1]))
    U_lax[0] = U_lax[1]
    U_lax[-1] = U_lax[-2]

# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[X, U_lax, U], header="X Lax-Friedrichs U", comments="")
print(f"File '{output_file}' generated.")
