import numpy as np
from tqdm import tqdm

flt = np.float64

def g(x):
    x2 = x*x
    x3 = x*x2
    x4 = x*x3
    return (x4 - 6*x3 + 12*x2 - 14*x + 9)/(1 + 2*x + x2)

# Initial value problem:
# y' = f(y,x) = y^2 - g(x) ; y(0) = 2
def f(y, x):
    return y*y - g(x)

# Analytical solution
def ytrue(x):
    return (1 - x)*(2 - x)/(1 + x)

def forward_euler(xi, xf, N):
    h = (xf - xi) / (N-1)
    X = np.linspace(xi, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x = X[i-1]
        y_ = Y[i-1]
        Y[i] = y_ + h * f(y_, x)

    # Error values for log-log plot
    #E = np.abs(Y - Y_true)
    return X, Y

def backward_euler(xi, xf, N):
    def zero_by_newton(y, y_, x, h):
        def G(y, y_, x, h): return y - h*f(y,x) - y_
        def dG(y, y_, x, h): return 1 - h*2*y
        yi = y
        while np.abs(G(yi, y_, x, h)/dG(yi, y_, x, h)) >= 0.0001:
            yi = yi - G(yi, y_, x, h)/dG(yi, y_, x, h)
        return yi
    h = (xf - xi) / (N-1)
    X = np.linspace(xi, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x = X[i]
        y_ = Y[i-1]
        Y[i] = zero_by_newton(y_, y_, x, h)
    return X, Y

dx = 0.01
xi = 0.0
xf = 1.6
N = int(xf / dx)
X, Y = forward_euler(xi, xf, N)
Y_true = ytrue(X)
#print(X)
print(Y)
#print(Y_true)

X, Y = backward_euler(xi, xf, N)
Y_true = ytrue(X)
#print(X)
print(Y)
#print(Y_true)

# Generate plot
#import matplotlib.pyplot as plt
#plt.plot(X, Y, 'r-')
#plt.plot(X, Y_true, 'b-')
#plt.xlabel('X')
#plt.ylabel('Y')
#plt.grid(True)
#plt.legend(["Numerical", "Analytical"], loc="upper right")
#plt.show()
