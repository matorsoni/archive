import numpy as np

'''
Solve the non-linear pendulum EDO, where k = g/L, with Dirichlet conditions.
    u''(t) + k sin(u(t)) = 0 ; u(0) = alpha , u(T) = beta

'''



alpha = 0.7
beta = 0.7
T = 2*np.pi

# List of mesh sizes m to consider.
# The recurrence m' = 2m+1 makes sure we are able to sample the exact same position for different m:
#   U'_2i = U_i => 2i h' = ih => 2T/(m'+1) = T/(m+1) => m' = 2m+1
M = [50]

for i in range(8):
    M.append(2 * M[-1] + 1)

m=M[0]
h=T/(m+1)
h2 = h*h

# Define matrix A
A = np.zeros(shape=(m,m), dtype=np.float64)
A[0,0:2] = np.array([-2,1])
A[m-1,m-2:m] = np.array([1,-2])
for r in range(1,m-1):
    A[r,r-1:r+2] = np.array([1,-2,1])
A /= h2

F = np.zeros(shape=(m,1), dtype=np.float64)
F[0] = alpha / h2
F[m-1] = beta / h2

def G(u):
    return A@u + np.sin(u) + F

def J(u):
    return A + np.diag(h2*np.cos(u))

t = h*(1.+np.array(range(m), dtype=np.float64))
u0 = 0.7*np.cos(t) + 0.5*np.sin(t)
U = [u0]
for i in range(m):
    u = U[-1]
    delta = np.linalg.solve(J(u), -G(u))
    U.append(u + delta)

# Generate plot
import matplotlib.pyplot as plt
for i in range(m):
    plt.plot(t, U[i], 'ro-')
#plt.plot(H, D_0_error, 'bs-')
#plt.plot(H, D_3_error, 'g^-')
plt.xlabel('h')
plt.ylabel('Aproximation error')
#plt.xscale('log')
#plt.yscale('log')
plt.grid(False)
#plt.legend(["D+", "D0", "D3"], loc="lower right")
plt.show()