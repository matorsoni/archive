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

# Initial condition
def eta(X):
    return 2.0 - 1. * (X >= 0.2).astype(float)  # Heaviside step function

U = eta(X)

# Main time-stepping loop
for n in range(nsteps):

    # Regular upwind
    #U[I] = U[I] - (k/h)*U[I]*(U[I] - U[I-1])

    # Delayed upwind
    #U[I] = U[I] - (k/h)*U[I-1]*(U[I] - U[I-1])

    # Conservative Upwind
    #U[I] = U[I] - (k/(2*h)) * (U[I]**2 - U[I-1]**2)

    # Lax-Friedrichs
    U[I_] = 0.5 * (U[I_-1] + U[I_+1]) - (k/(4*h)) * (U[I_+1]**2 - U[I_-1]**2)

    # Dirichlet boundary conditions (reflective)
    U[0] = U[1]
    U[-1] = U[-2]

# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[X, eta(X - k*nsteps), U], header="X FTRUE U", comments="")
print(f"File '{output_file}' generated.")
