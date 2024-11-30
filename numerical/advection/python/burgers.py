import numpy as np
import matplotlib.pyplot as plt

# Parameters
ax = 0
bx = 1
m = 100  # Number of spatial points (excluding boundaries)
tfinal = 0.2

h = (bx - ax) / (m + 1)  # Spatial step size
k = 0.4 * h             # Time step size
x = np.linspace(ax, bx, m + 2)  # Grid points, including boundaries

I = np.arange(1, m + 1)  # Indices for interior points
nsteps = int(np.round(tfinal / k))  # Number of time steps

# Initial condition
def eta(x):
    return 2.0 - 1. * (x >= 0.2).astype(float)  # Heaviside step function

u = eta(x)

# Main time-stepping loop
for n in range(nsteps):
    u[I] = u[I] - (k / (2 * h)) * (u[I]**2 - u[I-1]**2)  # Corrected Upwind flux

    # Dirichlet boundary conditions (reflective)
    u[0] = u[1]
    u[-1] = u[-2]

# Save data for plotting
output_file = "output.dat"
np.savetxt(output_file, np.c_[x, eta(x - k*nsteps), u], header="X FTRUE U", comments="")
print(f"File '{output_file}' generated.")
