import numpy as np

N = 51
a = 1.0
h = 1.0 / (N-1)
k = 0.8 * h
#epsilon = a**2 * k / 2  # Lax–Wendroff method
#epsilon = h**2 / (2*k)  # Lax–Friedrichs method
epsilon = a * h / 2      # Upwind Method

print(f"Epsilon = {epsilon}")

# Build first and second difference matrices
M1 = np.diag(np.ones(N - 1), 1) - np.diag(np.ones(N - 1), -1)
M2 = np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1) - 2 * np.eye(N)

# Apply periodic boundary conditions
M1[0, -1] = -1
M1[-1, 0] = 1
M2[0, -1] = 1
M2[-1, 0] = 1

# Compose matrix A_epsilon
A_epsilon = (-a / (2 * h)) * M1 + (epsilon / h**2) * M2

# Compute scaled eigenvalues
eigenvalues = np.linalg.eigvals(A_epsilon) * k

# Save eigenvalues to a file for GNUplot
gnufilename = "eigenvalues.dat"
with open(gnufilename, "w") as file:
    for ev in eigenvalues:
        file.write(f"{ev.real}\t{ev.imag}\n")
print(f"Eigenvalues saved to {gnufilename}.")

# Save region of stability data (unit circle for Euler Explicit)
theta = np.linspace(0, 2 * np.pi, 1000)
unit_circle_x = np.cos(theta) - 1
unit_circle_y = np.sin(theta)
with open("stability_region.dat", "w") as file:
    for x, y in zip(unit_circle_x, unit_circle_y):
        file.write(f"{x}\t{y}\n")
print("Stability region saved to 'stability_region.dat'.")
