import numpy as np

# Define constants
a = 1.0  # wave speed
h = 1.0 / 50  # spatial step
k = 0.8 * h  # time step (CFL condition)
CFL = a * k / h  # Courant number
epsilon = a * h / 2  # direct computation of epsilon
N = 50  # number of grid points (dimension of matrix A)

# Check stability
print(f"Courant Number (CFL): {CFL:.2f}")
if CFL > 1:
    print(f"Warning: The method might be unstable. CFL = {CFL:.2f} (should be <= 1)")

# Build matrices M1 and M2
M1 = np.diag(np.ones(N - 1), 1) - np.diag(np.ones(N - 1), -1)  # First difference matrix
M2 = np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1) - 2 * np.eye(N)  # Second difference matrix

# Apply periodic boundary conditions
M1[0, -1] = -1
M1[-1, 0] = 1
M2[0, -1] = 1
M2[-1, 0] = 1

# Matrix A_epsilon
A_epsilon = (-a / (2 * h)) * M1 + (epsilon / h**2) * M2

# Compute scaled eigenvalues
eigenvalues = np.linalg.eigvals(A_epsilon) * k

# Save eigenvalues to a file for GNUplot
with open("eigenvalues.dat", "w") as file:
    for ev in eigenvalues:
        file.write(f"{ev.real}\t{ev.imag}\n")
print("Eigenvalues saved to 'eigenvalues.dat'.")

# Save region of stability data (unit circle for Euler Explicit)
theta = np.linspace(0, 2 * np.pi, 1000)
unit_circle_x = np.cos(theta) - 1
unit_circle_y = np.sin(theta)
with open("stability_region.dat", "w") as file:
    for x, y in zip(unit_circle_x, unit_circle_y):
        file.write(f"{x}\t{y}\n")
print("Stability region saved to 'stability_region.dat'.")
