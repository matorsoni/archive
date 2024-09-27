import numpy as np

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

# Forward Euler solver for N points including initial 0.0
def forward_euler(xf, N):
    h = xf / (N-1)
    X = np.linspace(0.0, xf, N, dtype=flt)
    Y = np.zeros(shape=(N,), dtype=flt)
    Y[0] = 2.0
    Y_true = f(X)
    for i in range(1, N):
        x = X[i]
        y_ = Y[i-1]
        Y[i] = y_ + h * (y_*y_ - g(x))

    # Error values for log-log plot
    E = np.abs(Y - Y_true)

    # Generate plot
    import matplotlib.pyplot as plt
    plt.plot(X, Y, 'ro-')
    plt.plot(X, Y_true, 'bs-')
    #plt.plot(X, D_3_error, 'g^-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(False)
    plt.legend(["Numerical", "Analytical"], loc="lower right")
    plt.show()

dx = 0.1
xf = 1.6
N = int(xf / dx)
forward_euler(xf, N)