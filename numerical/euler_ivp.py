import numpy as np
from tqdm import tqdm

flt = np.float64

# Initial value problem:
# y' = y^2 - g(x) ; y(0) = 2
def g(x):
    x2 = x*x
    x3 = x*x2
    x4 = x*x3
    return (x4 - 6*x3 + 12*x2 - 14*x + 9)/(1 + 2*x + x2)

# Analytical solution
def f(x):
    return (1 - x)*(2 - x)/(1 + x)

def forward_euler(xf, N):
    h = xf / (N-1)
    X = np.linspace(0.0, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x = X[i-1]
        y_ = Y[i-1]
        Y[i] = y_ + h * (y_*y_ - g(x))

    # Error values for log-log plot
    #E = np.abs(Y - Y_true)
    return X, Y

def backward_euler(xf, N):
    h = xf / (N-1)
    X = np.linspace(0.0, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x = X[i-1]
        y_ = Y[i-1]
        Y[i] = y_ + h * (y_*y_ - g(x))
    return X, Y

dx = 0.0001
xf = 1.6
N = int(xf / dx)
X, Y = forward_euler(xf, N)
Y_true = f(X)

# Generate plot
import matplotlib.pyplot as plt
plt.plot(X, Y, 'r-')
plt.plot(X, Y_true, 'b-')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.legend(["Numerical", "Analytical"], loc="upper right")
plt.show()
