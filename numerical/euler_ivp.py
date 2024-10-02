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
        x_ = X[i-1]
        y_ = Y[i-1]
        Y[i] = y_ + h * f(y_, x_)
    return X, Y

def backward_euler(xi, xf, N):

    def zero_by_newton(y_init, y_prev, x, h):
        def G(y, y_, x, h): return y - h*f(y,x) - y_
        def dG(y, y_, x, h): return 1 - h*2*y
        tol = 1e-4
        max_iter = 100
        y = y_init
        for _ in range(max_iter):
            update = G(y, y_prev, x, h)/dG(y, y_prev, x, h)
            y = y - update
            if np.abs(update) < tol:
                break
        return y

    h = (xf - xi) / (N-1)
    X = np.linspace(xi, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x_ = X[i]
        y_ = Y[i-1]
        Y[i] = zero_by_newton(y_, y_, x_, h)
    return X, Y

def runge_kutta_4(xi, xf, N):
    h = (xf - xi) / (N-1)
    X = np.linspace(xi, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    for i in tqdm(range(1, N)):
        x_ = X[i-1]
        y_ = Y[i-1]
        k1 = h * f(y_, x_)
        k2 = h * f(y_ + 0.5 * k1, x_ + 0.5 * h)
        k3 = h * f(y_ + 0.5 * k2, x_ + 0.5 * h)
        k4 = h * f(y_ + k3, x_ + h)
        Y[i] = y_ + (k1 + 2*k2 + 2*k3 + k4) / 6
    return X, Y

def generate_plot(X, Y, Y_true):
    import matplotlib.pyplot as plt
    pad = 0.1
    minx = min(X) - pad
    maxx = max(X) + pad
    miny = min(Y_true) - pad
    maxy = max(Y_true) + pad
    plt.plot(X, Y, 'r-')
    plt.plot(X, Y_true, 'b-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(minx, maxx)
    plt.ylim(miny, maxy)
    plt.grid(True)
    plt.legend(["Numerical", "Analytical"], loc="upper right")
    plt.show()

h = 0.01
xi = 0.0
xf = 4.6
N = int((xf-xi) / h)

X, Y = forward_euler(xi, xf, N)
Y_true = ytrue(X)
generate_plot(X, Y, Y_true)

X, Y = backward_euler(xi, xf, N)
Y_true = ytrue(X)
generate_plot(X, Y, Y_true)

X, Y = runge_kutta_4(xi, xf, N)
Y_true = ytrue(X)
generate_plot(X, Y, Y_true)
